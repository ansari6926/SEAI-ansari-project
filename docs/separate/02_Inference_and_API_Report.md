# EXPERIMENT 2

## TITLE

Inference Engine and REST API Deployment for RoadSense AI

## AIM

To implement an inference API for RoadSense AI using FastAPI and ONNX Runtime and verify that uploaded road images return analytics results.

## SOFTWARE USED

- FastAPI
- Uvicorn
- ONNX Runtime
- OpenCV
- Python Multipart
- Swagger UI

## API ENDPOINTS

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Root API message |
| `/api/v1/health` | GET | Checks backend, ONNX, and LLM availability |
| `/api/v1/detect` | POST | Performs image analysis and returns annotated image |
| `/api/v1/analyze` | POST | Returns analytics without annotated image |
| `/api/v1/plan` | POST | Generates repair plan from manual detection data |

## PROCEDURE

1. FastAPI was selected as the REST inference framework.
2. Required packages were listed in `backend/requirements.txt`.
3. The backend application was implemented in `backend/main.py`.
4. The `/api/v1/health` endpoint was created to confirm service status.
5. The `/api/v1/detect` endpoint was created for full image analysis.
6. The `/api/v1/analyze` endpoint was created for lightweight analytics.
7. The `/api/v1/plan` endpoint was created to test the Civic Repair Planner independently.
8. Swagger UI was used to verify and document the API.

## SAMPLE TEST COMMAND

```bash
curl -F "file=@sample_road.jpg" http://localhost:8000/api/v1/analyze
```

## SAMPLE OUTPUT

```json
{
  "num_detections": 4,
  "severity_score": 0.2129,
  "repair_priority": "HIGH",
  "civic_repair_plan": {
    "estimated_cost_inr": 12100,
    "crew_size": 2,
    "sla_hours": 72,
    "lane_closure": "Partial lane closure with warning barricades",
    "risk_zone": "GREEN"
  }
}
```

## FIGURES TO ADD

Figure 2.1: FastAPI Swagger UI page  
Figure 2.2: Health API response  
Figure 2.3: Analyze endpoint test using Swagger or curl  
Figure 2.4: JSON response containing Civic Repair Planner output

## RESULT

The RoadSense AI backend inference API was successfully implemented and tested. The API returns road damage analytics, severity, priority, and repair planning details.
