# RoadSense AI Project Report

## Title

RoadSense AI: Road Damage Detection with Civic Repair Planning

## Aim

To customise an existing road-damage AI application, add LLM/GenAI-inspired reporting and a novel civic repair planning module, containerise the application, and prepare a Software Impacts-style research paper.

## Problem Statement

Road maintenance departments require faster ways to inspect roads and prioritise repairs. Traditional manual inspection can miss defects and often does not provide structured repair decisions. The project solves this by detecting road damage from images and converting results into actionable repair plans.

## Base Project Selected

The project is based on a sample road damage detection application using YOLO-style inference, FastAPI, OpenCV, and Docker. It was customised into a complete mini project named RoadSense AI.

## Novelty Added

The novelty added is a Civic Repair Planner. It estimates:

- Severity score and repair priority
- Approximate repair cost in INR
- Crew size
- SLA response time
- Lane closure or traffic-control requirement
- Risk zone
- SDG alignment
- Dispatch note for maintenance engineers

This makes the project different from a normal detection-only project because it connects AI output to civic maintenance decisions.

## SDG Alignment

- SDG 3: Good Health and Well-Being through safer road conditions
- SDG 9: Industry, Innovation and Infrastructure through automated infrastructure inspection
- SDG 11: Sustainable Cities and Communities through better urban maintenance planning

## System Architecture

```text
User uploads road image
        |
        v
Frontend dashboard
        |
        v
FastAPI backend
        |
        v
Image preprocessing with OpenCV
        |
        v
YOLOv8 ONNX inference or demo mode
        |
        v
Severity and priority services
        |
        v
Civic repair planner
        |
        v
LLM/rule-based maintenance alert
        |
        v
Annotated image and dashboard result
```

## Modules

### Backend

The backend is built using FastAPI. It accepts uploaded road images, performs image decoding, runs model inference or demo detections, calculates analytics, and returns JSON output with an annotated image.

### Frontend

The frontend is a static HTML, CSS, and JavaScript dashboard. It allows the user to upload road images and view severity, repair priority, cost estimate, SLA, dispatch note, and generated maintenance alert.

### Containerisation

The backend uses a Python 3.10 slim Docker image. The frontend uses an Nginx Alpine image. Docker Compose runs backend, frontend, and Redis services together.

### Kubernetes Deployment

The `deployment.yaml` file defines a Kubernetes deployment with the RoadSense backend, Redis sidecar, and BusyBox sidecar. A NodePort service exposes the backend.

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | API root |
| `/api/v1/health` | GET | Check backend and model status |
| `/api/v1/detect` | POST | Upload image and receive detections, analytics, alert, and annotated image |
| `/api/v1/analyze` | POST | Return analytics without annotated image |
| `/api/v1/plan` | POST | Generate repair plan from supplied detections |

## Commands Used

```bash
git init
git add .
git commit -m "Initial RoadSense AI project"
docker compose up --build
docker build -t yourusername/roadsense-ai-backend:latest ./backend
docker build -t yourusername/roadsense-ai-frontend:latest ./frontend
docker push yourusername/roadsense-ai-backend:latest
docker push yourusername/roadsense-ai-frontend:latest
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get services
```

## Expected Output

After uploading a road image, the system displays:

- Annotated image with bounding boxes
- Number and type of road damages
- Severity score
- Repair priority
- Estimated repair budget
- Crew and SLA recommendation
- Maintenance alert

## Conclusion

RoadSense AI is a simple but complete mini project for Software Engineering in Artificial Intelligence. It includes AI inference, GenAI-style reporting, a novel civic planning layer, Docker deployment, Kubernetes configuration, and a research-paper draft in Software Impacts style.
