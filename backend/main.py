"""
RoadSense AI — FastAPI Backend
Road damage detection + severity scoring + repair priority + LLM alert generation
Author: Your Name | SRM IST Trichy | SEAI Project 2026
"""

import io
import time
import base64
import os
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
import cv2
from PIL import Image

# ── Try importing ONNX runtime (CPU inference) ───────────────────────────────
try:
    import onnxruntime as ort
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False

# ── Try importing OpenAI (LLM alerts) ────────────────────────────────────────
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

app = FastAPI(
    title="RoadSense AI API",
    description="Road damage detection with severity scoring, repair priority, and LLM-generated alerts",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Class labels (RDD2022 categories) ────────────────────────────────────────
DAMAGE_CLASSES = {
    0: "Longitudinal Crack",
    1: "Transverse Crack",
    2: "Alligator Crack",
    3: "Pothole"
}

# Severity weights per class (higher = more severe)
CLASS_SEVERITY_WEIGHT = {0: 0.4, 1: 0.5, 2: 0.7, 3: 1.0}

# ── Model loading ─────────────────────────────────────────────────────────────
MODEL_PATH = os.getenv("MODEL_PATH", "best.onnx")
session = None

def load_model():
    global session
    if ONNX_AVAILABLE and os.path.exists(MODEL_PATH):
        session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
        print(f"[RoadSense AI] ONNX model loaded from {MODEL_PATH}")
    else:
        print("[RoadSense AI] ONNX model not found — running in DEMO mode")

load_model()


# ══════════════════════════════════════════════════════════════════════════════
# ANALYTICS SERVICES
# ══════════════════════════════════════════════════════════════════════════════

class SeverityService:
    """Compute normalised severity score [0,1] from detections."""

    @staticmethod
    def compute(detections: list, img_w: int, img_h: int) -> float:
        if not detections:
            return 0.0
        img_area = img_w * img_h
        scores = []
        for det in detections:
            cls = int(det["class_id"])
            conf = float(det["confidence"])
            x1, y1, x2, y2 = det["bbox"]
            box_area = abs((x2 - x1) * (y2 - y1))
            area_ratio = min(box_area / img_area, 1.0)
            weight = CLASS_SEVERITY_WEIGHT.get(cls, 0.5)
            score = weight * conf * (0.4 + 0.6 * area_ratio)
            scores.append(score)
        # Aggregate: max + mean blend
        return round(min(0.6 * max(scores) + 0.4 * (sum(scores) / len(scores)), 1.0), 4)


class PriorityService:
    """Classify repair urgency: LOW / MEDIUM / HIGH / CRITICAL."""

    @staticmethod
    def classify(severity: float, num_detections: int) -> str:
        if severity >= 0.75 or num_detections >= 6:
            return "CRITICAL"
        elif severity >= 0.55 or num_detections >= 4:
            return "HIGH"
        elif severity >= 0.30 or num_detections >= 2:
            return "MEDIUM"
        return "LOW"


class CivicRepairPlanner:
    """Translate detections into repair planning details for civic teams."""

    COST_TABLE_INR = {
        "Longitudinal Crack": 1200,
        "Transverse Crack": 1500,
        "Alligator Crack": 4500,
        "Pothole": 3500,
    }

    SLA_HOURS = {"CRITICAL": 24, "HIGH": 72, "MEDIUM": 168, "LOW": 720}
    CREWS = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "LOW": 1}

    @staticmethod
    def plan(detections: list, severity: float, priority: str, img_w: int, img_h: int) -> dict:
        if not detections:
            return {
                "estimated_cost_inr": 0,
                "crew_size": 0,
                "sla_hours": 0,
                "lane_closure": "Not required",
                "risk_zone": "CLEAR",
                "sdg_alignment": ["SDG 9", "SDG 11"],
                "dispatch_note": "No visible road damage was detected; continue routine monitoring.",
            }

        damage_counts = {}
        total_area_ratio = 0.0
        for det in detections:
            name = det["class_name"]
            damage_counts[name] = damage_counts.get(name, 0) + 1
            x1, y1, x2, y2 = det["bbox"]
            total_area_ratio += abs((x2 - x1) * (y2 - y1)) / max(img_w * img_h, 1)

        base_cost = sum(CivicRepairPlanner.COST_TABLE_INR.get(name, 2000) * count for name, count in damage_counts.items())
        severity_multiplier = 1.0 + min(severity, 1.0)
        area_multiplier = 1.0 + min(total_area_ratio * 4.0, 0.75)
        estimated_cost = int(round(base_cost * severity_multiplier * area_multiplier / 100.0) * 100)

        if priority in {"CRITICAL", "HIGH"}:
            lane_closure = "Partial lane closure with warning barricades"
        elif priority == "MEDIUM":
            lane_closure = "Short-duration shoulder control"
        else:
            lane_closure = "Mobile inspection only"

        if severity >= 0.75:
            risk_zone = "RED"
        elif severity >= 0.55:
            risk_zone = "ORANGE"
        elif severity >= 0.30:
            risk_zone = "YELLOW"
        else:
            risk_zone = "GREEN"

        primary_damage = max(damage_counts, key=damage_counts.get)
        return {
            "estimated_cost_inr": estimated_cost,
            "crew_size": CivicRepairPlanner.CREWS[priority],
            "sla_hours": CivicRepairPlanner.SLA_HOURS[priority],
            "lane_closure": lane_closure,
            "risk_zone": risk_zone,
            "sdg_alignment": ["SDG 3", "SDG 9", "SDG 11"],
            "dispatch_note": (
                f"Dispatch {CivicRepairPlanner.CREWS[priority]} crew member(s) for {primary_damage.lower()} "
                f"repair within {CivicRepairPlanner.SLA_HOURS[priority]} hours. Estimated material and labor "
                f"budget is INR {estimated_cost}."
            ),
        }


class LLMAlertService:
    """Generate natural-language maintenance report via LLM API."""

    @staticmethod
    def generate(detections: list, severity: float, priority: str) -> str:
        if not detections:
            return "No road damage detected. No maintenance action required at this time."

        # Build structured summary for the prompt
        damage_summary = {}
        for det in detections:
            cls_name = det["class_name"]
            damage_summary[cls_name] = damage_summary.get(cls_name, 0) + 1

        damage_str = ", ".join([f"{v}x {k}" for k, v in damage_summary.items()])
        prompt = f"""You are a road maintenance engineer AI assistant. Generate a concise, professional maintenance report based on the following road damage detection results.

Detected damage: {damage_str}
Severity score: {severity:.2f} / 1.00
Repair priority: {priority}

Provide a 4-sentence report covering:
1. Brief description of the detected damage
2. Recommended repair action and method
3. Estimated repair timeline
4. Safety advisory for road users

Keep the report professional, actionable, and under 150 words."""

        # Try OpenAI
        api_key = os.getenv("OPENAI_API_KEY", "")
        if OPENAI_AVAILABLE and api_key:
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    temperature=0.4
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"[LLM] OpenAI error: {e}")

        # Fallback: rule-based report
        return LLMAlertService._rule_based_report(damage_summary, severity, priority)

    @staticmethod
    def _rule_based_report(damage_summary: dict, severity: float, priority: str) -> str:
        actions = {
            "Pothole": "immediate cold-patch or hot-mix asphalt filling",
            "Alligator Crack": "full-depth reclamation or overlay resurfacing",
            "Transverse Crack": "crack sealing with rubberized asphalt",
            "Longitudinal Crack": "crack sealing and preventive surface treatment"
        }
        timelines = {"CRITICAL": "within 24–48 hours", "HIGH": "within 1 week",
                     "MEDIUM": "within 2–4 weeks", "LOW": "at next scheduled maintenance"}
        speed = {"CRITICAL": "20 km/h", "HIGH": "40 km/h", "MEDIUM": "60 km/h", "LOW": "normal speed"}

        primary = max(damage_summary, key=damage_summary.get)
        action = actions.get(primary, "standard pavement repair")
        return (
            f"Road damage inspection detected {', '.join(f'{v} instance(s) of {k}' for k,v in damage_summary.items())} "
            f"with an overall severity score of {severity:.2f}. "
            f"Recommended action: {action} as the primary repair method. "
            f"Estimated timeline: repair should be scheduled {timelines[priority]}. "
            f"Safety advisory: road users should reduce speed to {speed[priority]} until repairs are completed."
        )


class ManualDetection(BaseModel):
    class_id: int
    confidence: float
    bbox: list[int]


class PlanRequest(BaseModel):
    image_width: int = 1280
    image_height: int = 720
    detections: list[ManualDetection]


# ══════════════════════════════════════════════════════════════════════════════
# INFERENCE
# ══════════════════════════════════════════════════════════════════════════════

def preprocess(image: np.ndarray, imgsz: int = 640):
    img = cv2.resize(image, (imgsz, imgsz))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    return np.expand_dims(img, axis=0)


def postprocess(outputs, orig_h, orig_w, conf_thresh=0.35, imgsz=640):
    """Parse YOLOv8 output — shape [1, 8, 8400]."""
    predictions = outputs[0]
    if predictions.ndim == 3:
        predictions = predictions[0]  # [8, 8400]
    predictions = predictions.T  # [8400, 8]

    detections = []
    sx = orig_w / imgsz
    sy = orig_h / imgsz

    for pred in predictions:
        cx, cy, w, h = pred[:4]
        class_scores = pred[4:]
        cls_id = int(np.argmax(class_scores))
        conf = float(class_scores[cls_id])
        if conf < conf_thresh:
            continue
        x1 = int((cx - w / 2) * sx)
        y1 = int((cy - h / 2) * sy)
        x2 = int((cx + w / 2) * sx)
        y2 = int((cy + h / 2) * sy)
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(orig_w, x2), min(orig_h, y2)
        detections.append({
            "class_id": cls_id,
            "class_name": DAMAGE_CLASSES.get(cls_id, f"class_{cls_id}"),
            "confidence": round(conf, 4),
            "bbox": [x1, y1, x2, y2]
        })
    return detections


def draw_boxes(image: np.ndarray, detections: list) -> np.ndarray:
    colors = {0: (255, 140, 0), 1: (0, 200, 255), 2: (255, 50, 50), 3: (50, 50, 255)}
    img = image.copy()
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        cls = det["class_id"]
        color = colors.get(cls, (180, 180, 180))
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{det['class_name']} {det['confidence']:.2f}"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - th - 8), (x1 + tw + 4, y1), color, -1)
        cv2.putText(img, label, (x1 + 2, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return img


def demo_detections(orig_h, orig_w):
    """Return plausible demo detections when model is unavailable."""
    import random
    random.seed(42)
    demos = []
    for i in range(random.randint(2, 4)):
        cls = random.randint(0, 3)
        x1 = random.randint(50, orig_w // 2)
        y1 = random.randint(50, orig_h // 2)
        x2 = x1 + random.randint(60, 180)
        y2 = y1 + random.randint(40, 120)
        demos.append({
            "class_id": cls,
            "class_name": DAMAGE_CLASSES[cls],
            "confidence": round(random.uniform(0.55, 0.92), 4),
            "bbox": [x1, y1, min(x2, orig_w), min(y2, orig_h)]
        })
    return demos


# ══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/")
def root():
    return {"message": "RoadSense AI API is running", "version": "1.0.0", "docs": "/docs"}


@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "model_loaded": session is not None,
        "onnx_available": ONNX_AVAILABLE,
        "llm_available": OPENAI_AVAILABLE and bool(os.getenv("OPENAI_API_KEY"))
    }


@app.post("/api/v1/detect")
async def detect(file: UploadFile = File(...)):
    t_start = time.time()

    # Read image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    orig_h, orig_w = image.shape[:2]

    # Run inference
    if session is not None:
        inp = preprocess(image)
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: inp})
        detections = postprocess(outputs, orig_h, orig_w)
    else:
        detections = demo_detections(orig_h, orig_w)

    # Analytics pipeline
    severity = SeverityService.compute(detections, orig_w, orig_h)
    priority = PriorityService.classify(severity, len(detections))
    alert = LLMAlertService.generate(detections, severity, priority)
    civic_plan = CivicRepairPlanner.plan(detections, severity, priority, orig_w, orig_h)

    # Annotated image
    annotated = draw_boxes(image, detections)
    _, buf = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 85])
    annotated_b64 = base64.b64encode(buf.tobytes()).decode()

    t_end = time.time()

    return JSONResponse({
        "success": True,
        "inference_time_ms": round((t_end - t_start) * 1000, 1),
        "image_size": {"width": orig_w, "height": orig_h},
        "num_detections": len(detections),
        "detections": detections,
        "analytics": {
            "severity_score": severity,
            "severity_label": "HIGH" if severity > 0.6 else "MEDIUM" if severity > 0.3 else "LOW",
            "repair_priority": priority,
            "llm_alert": alert,
            "civic_repair_plan": civic_plan
        },
        "annotated_image_b64": annotated_b64,
        "demo_mode": session is None
    })


@app.post("/api/v1/analyze")
async def analyze_only(file: UploadFile = File(...)):
    """Returns only analytics without annotated image (faster)."""
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file")
    orig_h, orig_w = image.shape[:2]
    detections = demo_detections(orig_h, orig_w) if session is None else postprocess(
        session.run(None, {session.get_inputs()[0].name: preprocess(image)}), orig_h, orig_w
    )
    severity = SeverityService.compute(detections, orig_w, orig_h)
    priority = PriorityService.classify(severity, len(detections))
    civic_plan = CivicRepairPlanner.plan(detections, severity, priority, orig_w, orig_h)
    return {
        "num_detections": len(detections),
        "severity_score": severity,
        "repair_priority": priority,
        "civic_repair_plan": civic_plan,
        "damage_breakdown": {
            DAMAGE_CLASSES[i]: sum(1 for d in detections if d["class_id"] == i)
            for i in range(4)
        }
    }


@app.post("/api/v1/plan")
async def repair_plan(payload: PlanRequest):
    """Create a civic repair plan from supplied detection boxes."""
    detections = []
    for item in payload.detections:
        class_id = int(item.class_id)
        detections.append({
            "class_id": class_id,
            "class_name": DAMAGE_CLASSES.get(class_id, f"class_{class_id}"),
            "confidence": round(float(item.confidence), 4),
            "bbox": item.bbox,
        })

    severity = SeverityService.compute(detections, payload.image_width, payload.image_height)
    priority = PriorityService.classify(severity, len(detections))
    return {
        "num_detections": len(detections),
        "severity_score": severity,
        "repair_priority": priority,
        "civic_repair_plan": CivicRepairPlanner.plan(
            detections, severity, priority, payload.image_width, payload.image_height
        ),
    }
