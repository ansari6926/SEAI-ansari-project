# EXPERIMENT 1

## TITLE

RoadSense AI: Software Application Selection and Customization

## AIM

To select an existing machine learning application, customize it with a novel AI feature, and convert it into a complete Software Engineering in Artificial Intelligence mini project.

## SOFTWARE USED

- Python 3.10
- FastAPI
- OpenCV
- ONNX Runtime
- HTML, CSS, JavaScript
- Git

## BASE PROJECT

The selected project is a road damage detection application inspired by common YOLO-based road inspection repositories. The base idea is to upload a road image, identify visible damage such as potholes and cracks, and return detection results through an API.

## CUSTOMIZATION PERFORMED

The project was customized into RoadSense AI. The backend was built using FastAPI and OpenCV. The system supports ONNX model inference when a trained model file is available and also supports deterministic demo mode for classroom execution without a model file.

The main novelty added is the Civic Repair Planner. Normal detection systems only return bounding boxes and confidence values. RoadSense AI converts detections into civic maintenance decisions such as repair priority, estimated repair cost, crew size, SLA response hours, risk zone, lane closure recommendation, SDG alignment, and dispatch note.

## PROCEDURE

1. A road damage detection use case was selected because it is simple, socially useful, and aligned with SDG 3, SDG 9, and SDG 11.
2. A FastAPI backend was created to receive uploaded road images through REST endpoints.
3. OpenCV was used to decode and annotate images.
4. ONNX Runtime support was added for CPU-only inference.
5. A fallback demo detection function was added so the project can run even without a heavy model file.
6. Severity scoring was implemented using damage class, confidence, and damaged-area ratio.
7. Repair priority classification was implemented using severity and number of detections.
8. The Civic Repair Planner module was added as the novel feature.
9. A lightweight browser dashboard was created to upload images and show results.

## ARCHITECTURE

```text
Road Image Upload
        |
        v
Frontend Dashboard
        |
        v
FastAPI Backend
        |
        v
OpenCV Image Processing
        |
        v
ONNX Inference or Demo Mode
        |
        v
Severity and Priority Services
        |
        v
Civic Repair Planner
        |
        v
Dashboard Output and Maintenance Alert
```

## OUTPUT

The application produces:

- Annotated road image
- Damage type and count
- Severity score
- Repair priority
- Estimated repair cost
- Crew size
- SLA response time
- Lane closure guidance
- Maintenance alert

## FIGURES TO ADD

Figure 1.1: RoadSense AI project folder in VS Code  
Figure 1.2: Backend FastAPI code showing Civic Repair Planner  
Figure 1.3: Frontend dashboard opened in browser  
Figure 1.4: Sample road image analysis result

## RESULT

The base machine learning application was successfully customized into RoadSense AI with a novel civic repair planning module and complete web-based execution flow.
