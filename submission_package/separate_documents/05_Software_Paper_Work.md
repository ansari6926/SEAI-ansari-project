# PART 3: SOFTWARE PAPER PRESENTATION

# RoadSense AI: A Lightweight Road Damage Detection and Civic Repair Planning System

## Abstract

RoadSense AI is an open-source software application for automated road damage inspection and maintenance prioritisation. The system extends a conventional road damage detection pipeline by adding a civic repair planning layer that estimates severity, repair priority, crew size, service-level agreement, lane closure requirement, approximate repair cost, SDG alignment, and a natural-language maintenance alert. The backend is implemented using FastAPI and can serve either a YOLOv8 ONNX model or a deterministic demonstration mode when the model file is unavailable. A lightweight web dashboard allows users to upload road images, view annotated detections, and receive actionable repair recommendations. The software is aligned with Sustainable Development Goals 3, 9, and 11 by supporting safer roads, resilient infrastructure, and sustainable urban maintenance workflows.

## Keywords

Road damage detection; smart cities; civic maintenance; FastAPI; ONNX Runtime; computer vision; sustainable infrastructure

## Code Metadata

| Field | Description |
|---|---|
| Software name | RoadSense AI |
| Version | 1.0.0 |
| Repository | To be updated after GitHub push |
| Docker images | To be updated after Docker Hub push |
| License | MIT |
| Operating system | Windows, Linux, macOS through Docker |
| Programming languages | Python and JavaScript |
| Main dependencies | FastAPI, OpenCV, NumPy, Pillow, ONNX Runtime, OpenAI SDK |
| Input | Road image uploaded through REST API or web dashboard |
| Output | Damage detections, severity, priority, repair plan, annotated image, alert text |

## 1. Motivation and Significance

Road surface defects such as potholes, alligator cracks, transverse cracks, and longitudinal cracks are common causes of vehicle damage, traffic disruption, and road-safety risk. Manual inspection is slow, inconsistent, and difficult to scale across large urban and semi-urban road networks. Computer vision can detect visible pavement damage, but many prototype systems stop at bounding boxes and do not translate detections into decisions useful for municipal engineers.

RoadSense AI addresses this software gap by combining image-based road damage detection with a civic repair planning service. The novelty is not only recognising damage, but converting the detection result into an operational response: repair priority, estimated cost in Indian rupees, crew size, expected service timeline, lane-closure requirement, and a dispatch note.

## 2. Software Description

RoadSense AI follows a modular service-oriented architecture. The frontend sends a road image to a FastAPI backend. The backend decodes the image using OpenCV, runs ONNX inference when `best.onnx` is available, and falls back to deterministic demonstration detections for teaching and offline evaluation.

The detections are then passed through four post-processing services. The `SeverityService` calculates a normalised severity score. The `PriorityService` maps severity and detection count to LOW, MEDIUM, HIGH, or CRITICAL urgency. The `LLMAlertService` produces a concise maintenance note using an LLM API when an API key is present, with a rule-based fallback. The `CivicRepairPlanner` estimates repair cost, crew size, SLA hours, risk zone, SDG alignment, lane closure, and dispatch guidance.

## 2.1 Software Architecture

```text
Road image upload
        |
        v
FastAPI ingestion and OpenCV decoding
        |
        v
YOLOv8 ONNX inference or deterministic demo mode
        |
        v
Bounding boxes and class labels
        |
        v
Severity scoring and repair priority
        |
        v
Civic repair planner and LLM/rule-based alert
        |
        v
Web dashboard, REST JSON, annotated image
```

## 3. Illustrative Example

If an uploaded image contains pothole and crack detections, RoadSense AI returns detection count, bounding boxes, confidence values, a severity score, and a repair priority. The civic planning layer recommends lane closure, crew size, response window, and approximate repair cost. The dashboard presents these outputs in a compact operational view.

## 4. Impact and Future Developments

The software has direct relevance to SDG 9 by supporting resilient infrastructure maintenance, SDG 11 by enabling safer and more sustainable cities, and SDG 3 by reducing road-safety risk. Its CPU-friendly ONNX design and deterministic fallback make it suitable for classroom demonstrations and low-resource environments.

Future work can improve the repair planner by integrating GPS coordinates, road category, traffic density, rainfall history, and verified municipal cost schedules. A future agentic workflow could automatically create maintenance tickets and notify relevant departments.

## 5. Conclusion

RoadSense AI demonstrates how a small AI software project can move from detection output to actionable public-infrastructure intelligence. The application combines computer vision, REST inference, GenAI-style reporting, Docker deployment, and sustainable-development alignment.

## Declaration of Competing Interest

The author declares that there are no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## References

[1] Elsevier, Software Impacts journal author information and manuscript format.  
[2] Ultralytics, YOLOv8 documentation.  
[3] Microsoft, ONNX Runtime documentation.  
[4] FastAPI documentation.  
[5] United Nations, Sustainable Development Goals.
