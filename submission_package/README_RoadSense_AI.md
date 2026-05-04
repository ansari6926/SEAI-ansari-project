# RoadSense AI

RoadSense AI is a lightweight road damage intelligence system for SEAI mini project submission. It detects road damage from images, scores severity, assigns repair priority, generates a maintenance alert, and adds a novel civic repair planner for cost, crew, SLA, risk-zone, lane-closure, and SDG guidance.

## Novelty

The base detection workflow has been extended with a `CivicRepairPlanner` that converts AI detections into practical municipal repair decisions. This moves the project beyond bounding-box detection and makes the output useful for infrastructure planning.

## Features

- FastAPI inference backend
- Optional YOLOv8 ONNX model serving through ONNX Runtime
- Deterministic demo mode when `best.onnx` is not available
- Severity scoring and LOW/MEDIUM/HIGH/CRITICAL repair priority
- LLM maintenance alert with rule-based fallback
- Civic repair plan with cost, crew size, SLA, risk zone, lane closure, and SDG alignment
- Static web dashboard
- Docker Compose and Kubernetes deployment files
- Software Impacts-style paper and project report in `docs/`

## SDG Alignment

- SDG 3: Good Health and Well-Being
- SDG 9: Industry, Innovation and Infrastructure
- SDG 11: Sustainable Cities and Communities

## Quickstart

```bash
docker compose up --build
```

Open:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

The application works in demo mode without a model file. To use a real model, place `best.onnx` inside `backend/` or set `MODEL_PATH`.

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/health` | GET | Backend and model health check |
| `/api/v1/detect` | POST | Upload image and receive detections, analytics, alert, plan, and annotated image |
| `/api/v1/analyze` | POST | Upload image and receive analytics without annotated image |
| `/api/v1/plan` | POST | Generate a repair plan from manual detection boxes |

## Project Structure

```text
RoadSense-AI/
  backend/
    main.py
    requirements.txt
    Dockerfile
  frontend/
    index.html
    styles.css
    app.js
    Dockerfile
  docs/
    Architecture.md
    Project_Report.md
    RoadSense_AI_Software_Impacts_Paper.md
  scripts/
    build_and_run.sh
    docker_publish.sh
  docker-compose.yml
  deployment.yaml
```

## Docker Hub Commands

```bash
set DOCKER_USER=yourusername
sh scripts/docker_publish.sh
```

## Kubernetes

```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get services
```

## Paper and Report

- `docs/RoadSense_AI_Software_Impacts_Paper.md`
- `docs/Project_Report.md`
- `docs/Architecture.md`

## License

MIT
