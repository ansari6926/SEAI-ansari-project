from __future__ import annotations

from datetime import datetime
from pathlib import Path
from statistics import mean

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"


app = FastAPI(
    title="RoadGuard AI",
    description="Road damage monitoring, civic analytics, and automated maintenance prioritization.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    location: str = Field(..., min_length=3)
    road_type: str = Field(default="urban arterial")
    traffic_density: int = Field(default=72, ge=0, le=100)
    visual_damage_score: int = Field(default=68, ge=0, le=100)
    citizen_reports: int = Field(default=11, ge=0, le=500)


class Incident(BaseModel):
    id: str
    ward: str
    location: str
    damage_type: str
    severity: int
    traffic_density: int
    citizen_reports: int
    estimated_cost: int
    status: str
    lat: float
    lng: float


INCIDENTS: list[Incident] = [
    Incident(id="RG-101", ward="Central", location="MG Road Flyover", damage_type="Pothole cluster", severity=91, traffic_density=94, citizen_reports=42, estimated_cost=185000, status="Critical", lat=28.6139, lng=77.2090),
    Incident(id="RG-102", ward="North", location="Ring Road Sector 12", damage_type="Longitudinal crack", severity=73, traffic_density=81, citizen_reports=28, estimated_cost=92000, status="High", lat=28.7041, lng=77.1025),
    Incident(id="RG-103", ward="East", location="Civic Hospital Approach", damage_type="Edge break", severity=84, traffic_density=88, citizen_reports=31, estimated_cost=126000, status="Critical", lat=28.6500, lng=77.3150),
    Incident(id="RG-104", ward="South", location="Market Link Road", damage_type="Rutting", severity=67, traffic_density=62, citizen_reports=19, estimated_cost=74000, status="Moderate", lat=28.5355, lng=77.3910),
    Incident(id="RG-105", ward="West", location="School Zone Avenue", damage_type="Surface wear", severity=58, traffic_density=76, citizen_reports=35, estimated_cost=51000, status="High", lat=28.6692, lng=77.4538),
    Incident(id="RG-106", ward="Central", location="Bus Depot Junction", damage_type="Pothole", severity=79, traffic_density=90, citizen_reports=24, estimated_cost=103000, status="High", lat=28.6304, lng=77.2177),
]


def priority_score(severity: int, traffic_density: int, citizen_reports: int) -> int:
    report_pressure = min(citizen_reports * 2, 100)
    return round((severity * 0.5) + (traffic_density * 0.3) + (report_pressure * 0.2))


def priority_label(score: int) -> str:
    if score >= 85:
        return "Emergency repair"
    if score >= 72:
        return "Schedule within 7 days"
    if score >= 55:
        return "Plan in monthly maintenance"
    return "Monitor"


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "service": "RoadGuard AI",
        "status": "running",
        "model": "road-damage-priority-demo-v1",
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


@app.get("/api/incidents")
def incidents() -> list[dict]:
    enriched = []
    for incident in INCIDENTS:
        item = incident.model_dump()
        item["priority_score"] = priority_score(
            incident.severity,
            incident.traffic_density,
            incident.citizen_reports,
        )
        enriched.append(item)
    return sorted(enriched, key=lambda row: row["priority_score"], reverse=True)


@app.get("/api/analytics")
def analytics() -> dict:
    scores = [
        priority_score(item.severity, item.traffic_density, item.citizen_reports)
        for item in INCIDENTS
    ]
    ward_totals: dict[str, dict[str, int]] = {}
    for item in INCIDENTS:
        ward = ward_totals.setdefault(item.ward, {"incidents": 0, "cost": 0, "critical": 0})
        ward["incidents"] += 1
        ward["cost"] += item.estimated_cost
        ward["critical"] += int(item.status == "Critical")

    return {
        "total_incidents": len(INCIDENTS),
        "critical_incidents": sum(1 for item in INCIDENTS if item.status == "Critical"),
        "average_priority": round(mean(scores), 1),
        "estimated_budget": sum(item.estimated_cost for item in INCIDENTS),
        "ward_totals": ward_totals,
        "maintenance_queue": [
            {
                "id": item.id,
                "location": item.location,
                "action": priority_label(priority_score(item.severity, item.traffic_density, item.citizen_reports)),
                "priority_score": priority_score(item.severity, item.traffic_density, item.citizen_reports),
            }
            for item in sorted(INCIDENTS, key=lambda row: priority_score(row.severity, row.traffic_density, row.citizen_reports), reverse=True)
        ],
    }


@app.post("/api/predict")
def predict(payload: PredictionRequest) -> dict:
    score = priority_score(
        payload.visual_damage_score,
        payload.traffic_density,
        payload.citizen_reports,
    )
    damage_type = "Pothole cluster" if payload.visual_damage_score >= 82 else "Crack and surface distress"
    confidence = min(98, 61 + round(payload.visual_damage_score * 0.32) + round(payload.citizen_reports * 0.25))
    return {
        "location": payload.location,
        "road_type": payload.road_type,
        "predicted_damage": damage_type,
        "confidence": confidence,
        "priority_score": score,
        "recommendation": priority_label(score),
        "maintenance_window": "24-48 hours" if score >= 85 else "3-7 days" if score >= 72 else "This month",
    }

