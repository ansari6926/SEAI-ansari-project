# RoadSense AI Project Report

## PART 1: MINI PROJECT

## TITLE

RoadSense AI: Road Damage Detection with Civic Repair Planning

## AIM

To select a simple machine learning based road damage detection project, customize it with a novel AI-powered civic repair planning feature, deploy it through an inference API, containerize it, and prepare complete project documentation.

## PROBLEM STATEMENT

Road damage such as potholes and cracks creates safety risks for drivers, increases vehicle maintenance cost, and makes city infrastructure harder to manage. Manual road inspection requires time, manpower, and repeated field visits. A normal computer vision model can detect damage, but detection alone is not enough for municipal decision making. The maintenance team also needs priority, repair cost, crew planning, response time, and traffic control guidance.

RoadSense AI solves this by converting road image analysis into an operational repair plan.

## BASE PROJECT SELECTED

The base idea is taken from common open-source road damage detection projects that use YOLO-based object detection for pavement defects. The selected use case is intentionally simple compared with heavy projects such as face recognition or PPE kit analysis, but it has strong social impact and clear SDG alignment.

The customized project is named RoadSense AI.

## NOVELTY ADDED

The novelty added to the base project is the Civic Repair Planner.

Most detection projects stop after showing bounding boxes. RoadSense AI goes further by generating:

- Severity score
- Repair priority
- Estimated repair cost in INR
- Crew size recommendation
- SLA response time
- Risk zone
- Lane closure requirement
- SDG alignment
- Maintenance dispatch note

This makes the project a full software product rather than only a model demo.

## SDG ALIGNMENT

RoadSense AI is aligned with:

- SDG 3: Good Health and Well-Being, because better road maintenance reduces accident risk.
- SDG 9: Industry, Innovation and Infrastructure, because the project supports intelligent infrastructure inspection.
- SDG 11: Sustainable Cities and Communities, because it helps cities maintain safer roads.

## SOFTWARE AND TOOLS USED

| Category | Tools |
|---|---|
| Programming language | Python, JavaScript |
| Backend | FastAPI, Uvicorn |
| Image processing | OpenCV, Pillow |
| Inference engine | ONNX Runtime |
| Frontend | HTML, CSS, JavaScript |
| Containerization | Docker, Docker Compose |
| Deployment | Kubernetes YAML |
| Version control | Git and GitHub |
| Documentation | Markdown, DOCX, SVG diagrams |

## SYSTEM ARCHITECTURE

![RoadSense AI Architecture](assets/roadsense_architecture.svg)

Figure 1: RoadSense AI system architecture showing image upload, backend inference, analytics, civic repair planner, and final output.

## MODULE DESCRIPTION

### 1. Frontend Dashboard

The frontend is a lightweight browser application built using HTML, CSS, and JavaScript. It allows the user to upload a road image and view the final output in a clear dashboard. The dashboard displays severity, priority, cost estimate, SLA, damage breakdown, dispatch note, and annotated image.

### 2. FastAPI Backend

The backend receives image uploads through REST API endpoints. It performs image decoding, inference routing, analytics calculation, and response generation. FastAPI also provides Swagger UI for API testing.

### 3. Inference Layer

The inference layer is designed for YOLOv8 ONNX model execution using ONNX Runtime. If `best.onnx` is not available, the system runs in deterministic demo mode. This makes the project easy to demonstrate in class without needing a large trained model file.

### 4. Severity Service

The severity service calculates a normalized score using class type, confidence, and bounding-box area. More dangerous classes such as potholes and alligator cracks receive higher weights.

### 5. Priority Service

The priority service converts severity and number of detections into LOW, MEDIUM, HIGH, or CRITICAL repair priority.

### 6. Civic Repair Planner

This is the main novelty module. It generates cost, crew, SLA, lane closure, risk zone, SDG alignment, and dispatch note.

### 7. LLM Alert Service

The alert service generates a natural-language maintenance recommendation. If an LLM API key is unavailable, a rule-based fallback is used so the project still works.

## PRIORITY GRAPH

![Priority SLA Graph](assets/roadsense_priority_graph.svg)

Figure 2: Repair priority and SLA mapping used by RoadSense AI.

## COST GRAPH

![Repair Cost Graph](assets/roadsense_cost_graph.svg)

Figure 3: Relative base repair cost weights used by the Civic Repair Planner.

## API ENDPOINTS

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Root API response |
| `/api/v1/health` | GET | Checks backend and model status |
| `/api/v1/detect` | POST | Upload image and receive full result |
| `/api/v1/analyze` | POST | Upload image and receive analytics only |
| `/api/v1/plan` | POST | Generate repair plan from manual detections |

## PROCEDURE

1. A road damage detection use case was selected for the mini project.
2. A FastAPI backend was created.
3. Image upload support was added using `python-multipart`.
4. OpenCV was used for image decoding and annotation.
5. ONNX Runtime was added as the model serving engine.
6. Demo mode was added to make the project runnable without a trained model file.
7. Severity scoring and repair priority classification were implemented.
8. Civic Repair Planner was added as the novelty component.
9. A frontend dashboard was created for image upload and result display.
10. Dockerfiles were created for backend and frontend.
11. Docker Compose was configured for full-stack execution.
12. Kubernetes deployment YAML was prepared.
13. Git was used for version control.
14. The project was pushed to GitHub.

## LOCAL RUNNING COMMANDS

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_local.ps1
```

Frontend:

```text
http://localhost:3000
```

Backend API:

```text
http://localhost:8000/docs
```

## DOCKER COMMANDS

```bash
docker compose up --build
docker build -t yourusername/roadsense-ai-backend:latest ./backend
docker build -t yourusername/roadsense-ai-frontend:latest ./frontend
```

## GIT COMMANDS

```bash
git init
git add .
git commit -m "Build RoadSense AI mini project"
git remote add origin https://github.com/ansari6926/SEAI-ansari-project.git
git branch -M main
git push -u origin main
```

## SAMPLE OUTPUT

When a sample road image is analyzed, the system returns:

```json
{
  "num_detections": 4,
  "severity_score": 0.2129,
  "repair_priority": "HIGH",
  "estimated_cost_inr": 12100,
  "crew_size": 2,
  "sla_hours": 72,
  "lane_closure": "Partial lane closure with warning barricades"
}
```

## FIGURES TO PLACE IN FINAL WORD FILE

Figure 1: RoadSense AI architecture  
Figure 2: Priority and SLA graph  
Figure 3: Repair cost graph  
Figure 4: FastAPI Swagger UI  
Figure 5: Frontend dashboard running in browser  
Figure 6: GitHub repository page  
Figure 7: Docker Compose file or Docker build output

## RESULT

RoadSense AI was successfully developed as a complete mini project. It includes AI inference, REST API, frontend dashboard, novelty module, documentation, Docker files, Kubernetes deployment file, and GitHub repository.

## CONCLUSION

RoadSense AI demonstrates how a simple road damage detection project can be converted into a full-fledged AI software product. The novelty lies in transforming model detections into practical civic repair decisions. The project is simple enough for academic demonstration but complete enough to satisfy SEAI requirements.
