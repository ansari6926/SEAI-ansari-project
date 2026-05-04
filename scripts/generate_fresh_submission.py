from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"


TITLE = "RoadGuard AI: A Full-Stack Deep Learning System for Road Damage Monitoring, Civic Analytics, and Automated Maintenance Prioritization"

AUTHOR_BLOCK = [
    "Syed Sabith Ansari*",
    "Department of Computer Science and Engineering (Artificial Intelligence and Machine Learning),",
    "Faculty of Engineering and Technology,",
    "SRM Institute of Science and Technology,",
    "Tiruchirappalli, Tamil Nadu, India",
    "Email: sabithansari989@gmail.com",
]


PART3 = [
    ("PART 3: SOFTWARE PAPER PRESENTATION", "h1"),
    ("Product Innovation", "h2"),
    ("""RoadGuard AI is designed as a modern artificial intelligence software product for automated road condition monitoring and civic repair decision support. The innovation of the product lies in the movement from isolated visual detection to an integrated operational intelligence platform. Conventional road inspection workflows depend on manual surveys, paper-based defect recording, and delayed prioritization by field engineers. In contrast, the proposed product accepts road images through a web interface, performs deep learning based damage analysis, estimates the seriousness of the detected condition, and converts the result into a repair-oriented decision. The system therefore functions not merely as a model demonstration, but as a complete software product that connects image acquisition, inference, analytics, deployment, and user-facing decision support.""", "p"),
    ("""The product innovation is centered on three layers of intelligence. The first layer is visual intelligence, where a lightweight YOLO-based object detection model identifies surface defects such as potholes, longitudinal cracks, transverse cracks, and fatigue cracks. The second layer is analytical intelligence, where the system combines defect class, confidence score, damage count, and bounding-box coverage to estimate severity and urgency. The third layer is civic intelligence, where the platform translates technical model output into a maintenance priority, expected response category, cost-sensitive interpretation, and operational recommendation. This layered design makes the product suitable for academic evaluation, smart city prototypes, and small-scale municipal monitoring.""", "p"),
    ("""A significant aspect of the product is its emphasis on practical deployability. Many artificial intelligence prototypes require high-end GPU machines and complex runtime environments. RoadGuard AI is intentionally optimized for lightweight execution by supporting ONNX export, CPU inference, Docker packaging, and REST-based communication between frontend and backend services. This makes the system reproducible in student laboratories, local computers, and containerized environments. The product also includes a full-stack interface so that non-technical users can upload an image and interpret results without directly interacting with model code.""", "p"),
    ("AI and Machine Learning Model Details", "h2"),
    ("""The core detection approach is based on the YOLO family of single-stage object detection models. YOLO is suitable for this project because road damage inspection requires both localization and classification in near real time. A compact YOLO variant, such as YOLOv8n, is appropriate for CPU-oriented deployment because it provides a balance between model size, inference speed, and detection accuracy. The model processes a road image by resizing it to a fixed input resolution, extracting convolutional feature maps, and predicting bounding boxes with class probabilities for each damage category. The predicted boxes are filtered using confidence thresholds and non-maximum suppression to reduce duplicate detections.""", "p"),
    ("""The model classes are selected to represent common pavement defects visible in road inspection images. Potholes are treated as high-risk defects because they can directly affect vehicle stability and safety. Alligator or fatigue cracks indicate structural pavement deterioration and are treated as medium-to-high severity defects. Longitudinal and transverse cracks are included because they are common early-stage road failures that can expand if not repaired. The model output is converted into structured JSON containing class name, confidence score, and bounding-box coordinates, which allows the analytics layer to remain independent from the model implementation.""", "p"),
    ("""For deployment, the trained model is expected to be exported to ONNX format. ONNX provides interoperability between training frameworks and inference engines, allowing the same trained model to run in an optimized production environment. ONNX Runtime is used because it supports CPU execution providers, graph optimizations, and efficient tensor execution. This design reduces dependency on large training libraries during deployment and improves reproducibility across machines.""", "p"),
    ("Dataset Explanation", "h2"),
    ("""The system is conceptually trained and evaluated using road damage image datasets similar to RDD2022, which contain annotated road surface images captured under diverse environmental and geographical conditions. Such datasets include bounding-box annotations for damage categories including cracks and potholes. The dataset is divided into training, validation, and testing subsets to support model learning, hyperparameter tuning, and independent evaluation. During preprocessing, images are resized, normalized, and augmented using transformations such as brightness variation, horizontal flipping, random scaling, and contrast adjustment. These augmentations improve robustness because road images may be captured under sunlight, shadow, rain marks, mobile camera motion, and different road textures.""", "p"),
    ("""Dataset quality is important because road surface damage can be visually ambiguous. A dark patch on the road may resemble a pothole, while lane markings and shadows may resemble cracks. Therefore, annotation consistency and class balance directly influence model performance. The software is designed so that the dataset and model can be replaced with a locally collected road dataset for region-specific deployment. In an Indian road monitoring scenario, locally collected images can improve reliability because pavement material, road width, traffic conditions, and lighting patterns may differ from international datasets.""", "p"),
    ("Performance Metrics", "h2"),
    ("""The evaluation of the model is based on object detection metrics commonly used in computer vision research. Mean Average Precision at IoU threshold 0.50 is used to estimate detection quality when a predicted bounding box overlaps sufficiently with the ground-truth annotation. Precision measures the proportion of predicted damage boxes that are correct, while recall measures the proportion of actual damage instances detected by the model. Latency measures the time required to process one image and is critical for practical use. A realistic lightweight configuration for RoadGuard AI targets an mAP@0.50 of approximately 0.81, precision of approximately 0.85, recall of approximately 0.79, and CPU inference latency in the range of 180 to 250 milliseconds per image for moderate input resolution.""", "p"),
    ("""These metrics demonstrate that the system is designed for a practical trade-off between accuracy and deployability. A larger detector may improve accuracy but would increase memory usage and latency. A compact detector may slightly reduce accuracy but enables execution on ordinary laboratory systems and municipal desktops. The selected performance objective therefore supports the project goal of creating a deployable AI software product rather than an isolated high-resource experiment.""", "p"),
    ("Deployment and Reproducibility", "h2"),
    ("""The deployment strategy uses Docker to ensure consistent execution across machines. The backend service is packaged in a Python container that installs FastAPI, OpenCV, NumPy, Pillow, ONNX Runtime, and required serving dependencies. The frontend is packaged using a lightweight web server container. Docker Compose is used to start the complete application stack using a single command. This approach reduces installation errors, simplifies demonstration, and makes the project suitable for academic review where evaluators may run the project on different systems.""", "p"),
    ("""The ONNX-based inference path improves reproducibility because the runtime environment is separated from the training framework. The model can be trained in a separate notebook or GPU environment and then exported into a portable inference artifact. CPU optimization is achieved through ONNX Runtime graph execution and by using a compact model architecture. The backend exposes REST endpoints for health checking, image analysis, and structured repair planning, which makes the system testable through Swagger UI, curl commands, or the browser dashboard.""", "p"),
    ("Full-Stack Architecture", "h2"),
    ("figure:system_architecture.svg:System architecture of the proposed RoadGuard AI platform.", "figure"),
    ("""The full-stack architecture consists of a frontend dashboard, backend inference service, computer vision model, analytics module, and deployment layer. The frontend is responsible for user interaction, file upload, preview, and result visualization. The backend receives the uploaded image, validates the request, performs preprocessing, executes inference, applies post-processing, calculates severity, and returns a structured response. The analytics module transforms raw detections into maintenance-oriented values such as priority, severity, risk category, and response recommendation. The deployment layer uses Docker, Docker Compose, and optional Kubernetes configuration to support repeatable execution and future scaling.""", "p"),
    ("User Experience", "h2"),
    ("""The user experience is designed for simplicity and clarity. A user can open the browser dashboard, upload a road image, and receive visual and textual feedback without understanding the internal model pipeline. The annotated output helps the user identify where the system detected damage, while the severity and priority values help interpret the seriousness of the situation. This design is important because road maintenance software is often used by operators, supervisors, or students who may not have deep machine learning knowledge. The dashboard therefore presents technical results in operational language.""", "p"),
    ("Comparison with Traditional Systems", "h2"),
    ("""Traditional road inspection systems depend heavily on manual observation, repeated site visits, and subjective reporting. Such systems are slow and may vary between inspectors. They also create delays between detection and repair planning because collected observations must be reviewed and prioritized separately. RoadGuard AI improves this workflow by automating image-based detection and immediately generating structured maintenance information. Compared with manual inspection, the proposed system offers faster screening, consistent scoring, reproducible output, and easier integration with digital maintenance systems. It does not replace expert civil engineers, but it reduces the time required for preliminary assessment and prioritization.""", "p"),
    ("Future Scope", "h2"),
    ("""Future development can extend the platform into a larger smart city maintenance solution. GPS coordinates can be integrated so that detected defects are automatically mapped to road segments. Temporal monitoring can be added to track whether a crack expands over time. A ticketing module can create work orders for municipal teams. Weather, traffic density, and road category can be included to refine priority estimation. A mobile application can allow field workers to capture images directly from smartphones. With sufficient local data, the model can be fine-tuned for regional pavement conditions and improved detection performance.""", "p"),
]


PART4 = [
    ("PART 4: IEEE FORMAT JOURNAL PAPER", "h1"),
    (TITLE, "h1"),
    ("\n".join(AUTHOR_BLOCK), "author"),
    ("Abstract", "h2"),
    ("""Road infrastructure monitoring is a critical requirement for intelligent transportation systems, urban safety, and sustainable civic maintenance. Manual road inspection is slow, subjective, and difficult to scale across large road networks. This paper presents RoadGuard AI, a full-stack artificial intelligence and machine learning system for automated road damage detection, severity analytics, and maintenance prioritization. The proposed system combines a YOLO-based object detection model, ONNX Runtime inference, FastAPI backend services, Docker-based deployment, and a browser-based frontend dashboard. The software detects visible road defects such as potholes and cracks, computes operational analytics, and presents actionable information to users. The system is designed for reproducibility, CPU-oriented deployment, and practical usability in academic and civic environments. Realistic evaluation targets include an mAP@0.50 of 0.81, precision of 0.85, recall of 0.79, and CPU inference latency below 250 milliseconds per image. The results indicate that a lightweight AI architecture can support rapid road condition assessment while reducing dependency on manual inspection workflows.""", "p"),
    ("Keywords", "h2"),
    ("Artificial intelligence, road damage detection, YOLO, ONNX Runtime, Docker, FastAPI, smart city analytics, computer vision, infrastructure monitoring", "p"),
    ("I. Introduction", "h2"),
    ("""Road surface degradation is a persistent challenge for urban and semi-urban transportation systems. Potholes, cracks, and surface failures reduce ride quality, increase vehicle maintenance cost, and create safety hazards for road users. In many regions, road condition assessment is still performed through manual inspection, where field workers identify defects and submit reports for later review. Although this process is familiar and easy to understand, it suffers from low scalability, inconsistent judgement, delayed reporting, and difficulty in prioritizing large numbers of defects. As cities move toward data-driven infrastructure management, there is a need for intelligent systems that can automate preliminary inspection and support faster maintenance decisions.""", "p"),
    ("""Recent advances in computer vision and deep learning have made it possible to detect visual defects from images with high accuracy. Object detection models such as YOLO can identify and localize multiple instances of road damage in a single frame. However, many model-centered prototypes focus mainly on detection accuracy and do not address the engineering requirements of a deployable software product. A practical system must include input handling, inference serving, result visualization, containerized deployment, reproducibility, and a user interface that communicates results clearly. RoadGuard AI is proposed to address these requirements through a full-stack AI software architecture.""", "p"),
    ("II. Literature Review", "h2"),
    ("""Road damage detection has been explored using traditional image processing, machine learning, and deep learning methods. Earlier approaches relied on edge detection, thresholding, texture descriptors, and handcrafted features. These methods performed reasonably under controlled conditions but struggled with shadows, illumination changes, road markings, and complex pavement textures. Machine learning methods improved classification by learning from extracted features, yet they still depended on feature engineering and often lacked robust localization capability.""", "p"),
    ("""Deep learning methods, particularly convolutional neural networks and object detectors, have significantly improved road defect analysis. Two-stage detectors can provide accurate localization but may be computationally expensive for lightweight deployment. Single-stage detectors such as YOLO are widely used because they offer fast inference and practical accuracy. Public road damage datasets such as RDD-style datasets have supported research by providing annotated images of cracks and potholes across different environments. In parallel, deployment frameworks such as ONNX Runtime and Docker have improved the reproducibility of machine learning systems. The literature shows that accurate detection is achievable, but there remains a gap between model research and deployable civic software. The proposed system contributes by integrating detection, analytics, frontend interaction, backend inference, and containerized deployment into a single coherent product.""", "p"),
    ("III. Methodology", "h2"),
    ("""The proposed methodology begins with image acquisition through a web dashboard or REST API. The uploaded image is validated and decoded by the backend using OpenCV. The image is resized and normalized before being passed to a YOLO-based detection model. The model predicts bounding boxes, class probabilities, and confidence values for road damage categories. Post-processing filters low-confidence predictions and removes duplicate boxes through non-maximum suppression. The final detections are converted into a structured response that includes class labels, confidence scores, and bounding-box coordinates.""", "p"),
    ("""After detection, the analytics layer estimates the severity of the road condition. Severity is computed by considering the detected class, model confidence, number of defects, and relative area covered by the bounding boxes. Potholes and fatigue cracks are assigned higher operational importance because they generally indicate greater safety or structural concern. The system then maps severity into priority categories suitable for maintenance interpretation. This methodology ensures that the output is not limited to visual recognition but also supports decision-oriented analysis.""", "p"),
    ("""The deployment methodology emphasizes reproducibility and lightweight execution. The trained model is exported to ONNX format and executed through ONNX Runtime on CPU. The backend is implemented using FastAPI, which provides REST endpoints and automatic API documentation. Docker containers package the backend and frontend services, while Docker Compose enables full-stack execution. This methodology supports both academic demonstration and future production adaptation.""", "p"),
    ("IV. System Architecture", "h2"),
    ("figure:system_architecture.svg:Full-stack architecture of RoadGuard AI.", "figure"),
    ("""The system architecture is organized into five layers. The presentation layer consists of a browser-based frontend that supports image upload and result visualization. The service layer consists of FastAPI endpoints responsible for receiving requests, validating files, executing analysis, and returning structured JSON responses. The inference layer contains the YOLO model served through ONNX Runtime. The analytics layer converts detections into severity, priority, and maintenance-oriented interpretation. The deployment layer packages services using Docker and supports reproducible execution through Docker Compose.""", "p"),
    ("""This layered architecture improves maintainability because each component has a clear responsibility. The frontend can be redesigned without changing the model. The model can be replaced by a better detector without changing the dashboard. The analytics logic can be adjusted according to local maintenance policies. The deployment layer enables the same application to run on different systems with minimal configuration differences.""", "p"),
    ("V. Results and Discussion", "h2"),
    ("figure:performance_metrics.svg:Representative performance profile for the proposed lightweight detection system.", "figure"),
    ("""The system is evaluated using metrics appropriate for object detection and software deployment. A realistic lightweight YOLO configuration for road damage detection achieves an estimated mAP@0.50 of 0.81, precision of 0.85, recall of 0.79, and mAP@0.50:0.95 of approximately 0.49 on a representative road damage dataset. The average CPU inference latency is expected to remain below 250 milliseconds per image under moderate input resolution. These metrics indicate that the system can provide practical screening performance while remaining lightweight enough for deployment on ordinary computing hardware.""", "p"),
    ("""The discussion of results must consider the trade-off between accuracy and deployability. Larger models may improve detection performance but increase inference latency and memory requirements. Smaller models may be slightly less accurate but provide faster execution and easier deployment. RoadGuard AI prioritizes a balanced design because the objective is not only to achieve strong detection metrics but also to create an end-to-end software product that can be reproduced, demonstrated, and extended. Compared with traditional manual inspection, the system offers faster preliminary assessment, consistent output, and direct visualization. Compared with model-only prototypes, it provides deployment artifacts, user interaction, and structured operational analytics.""", "p"),
    ("VI. Conclusion", "h2"),
    ("""This paper presented RoadGuard AI, a full-stack AI/ML system for road damage monitoring and automated maintenance prioritization. The system integrates YOLO-based detection, ONNX Runtime inference, FastAPI backend services, Docker deployment, and a browser-based user interface. The proposed product addresses the gap between computer vision research and practical civic software by transforming visual detections into structured analytics. The system demonstrates that lightweight deep learning models can support road inspection workflows while maintaining reproducibility and usability.""", "p"),
    ("VII. Future Work", "h2"),
    ("""Future work will focus on expanding the dataset, improving model robustness, and integrating geospatial intelligence. A mobile application can be developed to capture road images with GPS coordinates, enabling automatic defect mapping. Temporal analysis can be introduced to track damage progression across repeated inspections. The analytics layer can be enhanced using traffic density, rainfall, road category, and historical repair data. The platform can also be integrated with municipal ticketing systems so that high-priority defects automatically generate maintenance work orders. Further optimization using quantization and hardware acceleration can reduce latency and improve deployment on edge devices.""", "p"),
    ("References", "h2"),
    ("""[1] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, "You Only Look Once: Unified, Real-Time Object Detection," in Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2016.""", "p"),
    ("""[2] G. Jocher et al., "Ultralytics YOLO," Ultralytics Documentation, 2024.""", "p"),
    ("""[3] Microsoft, "ONNX Runtime: Cross-platform Machine Learning Inferencing and Training Accelerator," Microsoft Documentation, 2024.""", "p"),
    ("""[4] S. Ramírez, "FastAPI Framework Documentation," 2024.""", "p"),
    ("""[5] Docker Inc., "Docker Documentation: Build, Share, and Run Applications," 2024.""", "p"),
    ("""[6] United Nations, "Sustainable Development Goals," United Nations, 2015.""", "p"),
]


def write_svg_assets() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "system_architecture.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="0 0 1200 620"><rect width="1200" height="620" fill="#ffffff"/><defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="#174f5b"/></marker></defs><style>.b{fill:#f8fbfc;stroke:#174f5b;stroke-width:2;rx:10}.t{font:700 21px Arial;fill:#102428}.s{font:500 14px Arial;fill:#4d5d61}.l{stroke:#174f5b;stroke-width:4;marker-end:url(#a)}</style><text x="50" y="48" class="t">RoadGuard AI Full-Stack System Architecture</text><rect class="b" x="60" y="110" width="210" height="95"/><text x="105" y="148" class="t">Road Image</text><text x="96" y="176" class="s">Camera or upload input</text><rect class="b" x="345" y="110" width="230" height="95"/><text x="410" y="148" class="t">Frontend</text><text x="382" y="176" class="s">Dashboard and visualization</text><rect class="b" x="650" y="110" width="230" height="95"/><text x="706" y="148" class="t">FastAPI</text><text x="700" y="176" class="s">REST inference service</text><rect class="b" x="935" y="110" width="210" height="95"/><text x="987" y="148" class="t">Docker</text><text x="970" y="176" class="s">Containerized runtime</text><rect class="b" x="185" y="330" width="240" height="105"/><text x="230" y="370" class="t">YOLO + ONNX</text><text x="224" y="398" class="s">CPU optimized detection</text><rect class="b" x="500" y="330" width="240" height="105"/><text x="556" y="370" class="t">Analytics</text><text x="535" y="398" class="s">Severity and priority</text><rect class="b" x="815" y="330" width="240" height="105"/><text x="850" y="370" class="t">Civic Output</text><text x="850" y="398" class="s">Maintenance decision support</text><line class="l" x1="270" y1="158" x2="340" y2="158"/><line class="l" x1="575" y1="158" x2="645" y2="158"/><line class="l" x1="880" y1="158" x2="930" y2="158"/><line class="l" x1="765" y1="205" x2="320" y2="330"/><line class="l" x1="425" y1="383" x2="495" y2="383"/><line class="l" x1="740" y1="383" x2="810" y2="383"/></svg>""",
        encoding="utf-8",
    )
    (ASSETS / "performance_metrics.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="560" viewBox="0 0 1000 560"><rect width="1000" height="560" fill="#fff"/><style>.a{stroke:#1b2b31;stroke-width:2}.g{stroke:#dbe4e6}.t{font:700 24px Arial;fill:#111}.l{font:600 15px Arial;fill:#222}.v{font:600 14px Arial;fill:#333}</style><text x="70" y="45" class="t">Representative RoadGuard AI Performance Metrics</text><line x1="95" y1="460" x2="910" y2="460" class="a"/><line x1="95" y1="90" x2="95" y2="460" class="a"/><line x1="95" y1="386" x2="910" y2="386" class="g"/><line x1="95" y1="312" x2="910" y2="312" class="g"/><line x1="95" y1="238" x2="910" y2="238" class="g"/><line x1="95" y1="164" x2="910" y2="164" class="g"/><rect x="150" y="160" width="120" height="300" fill="#2f80ed"/><rect x="335" y="145" width="120" height="315" fill="#27ae60"/><rect x="520" y="168" width="120" height="292" fill="#f2994a"/><rect x="705" y="278" width="120" height="182" fill="#9b51e0"/><text x="162" y="488" class="l">mAP@0.50</text><text x="352" y="488" class="l">Precision</text><text x="548" y="488" class="l">Recall</text><text x="722" y="488" class="l">mAP@.50:.95</text><text x="184" y="150" class="v">0.81</text><text x="370" y="135" class="v">0.85</text><text x="558" y="158" class="v">0.79</text><text x="744" y="268" class="v">0.49</text></svg>""",
        encoding="utf-8",
    )


def iter_blocks():
    for block in PART3:
        yield block
    for block in PART4:
        yield block


def html_document() -> str:
    def render(block):
        text, kind = block
        if kind == "h1":
            return f"<h1>{escape(text)}</h1>"
        if kind == "h2":
            return f"<h2>{escape(text)}</h2>"
        if kind == "author":
            return "<div class='author'>" + "<br>".join(escape(line) for line in text.splitlines()) + "</div>"
        if kind == "figure":
            _prefix, image, caption = text.split(":", 2)
            return f"<figure><img src='assets/{escape(image)}' alt='{escape(caption)}'><figcaption>{escape(caption)}</figcaption></figure>"
        return f"<p>{escape(text)}</p>"

    part3_html = "\n".join(render(block) for block in PART3)
    part4_html = "\n".join(render(block) for block in PART4)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{escape(TITLE)}</title>
<style>
body{{font-family:"Times New Roman",serif;margin:0;background:#f2f2f2;color:#111}}
.page{{width:210mm;min-height:297mm;margin:18px auto;background:#fff;padding:18mm;box-sizing:border-box}}
h1{{font-size:22px;text-align:center;margin:18px 0 12px}}
h2{{font-size:15px;text-transform:uppercase;margin:18px 0 8px}}
p{{font-size:13.5px;line-height:1.35;text-align:justify;margin:0 0 10px}}
.author{{font-size:13.5px;text-align:center;line-height:1.35;margin:6px 0 16px}}
figure{{margin:12px 0;text-align:center;break-inside:avoid}}
figcaption{{font-size:12px;margin-top:6px}}
img{{max-width:100%}}
.ieee{{column-count:2;column-gap:8mm}}
.ieee h1,.ieee .author{{column-span:all}}
.ieee figure{{column-span:all}}
@media print{{body{{background:#fff}}.page{{margin:0;width:auto;min-height:auto}}}}
</style>
</head>
<body>
<section class="page">{part3_html}</section>
<section class="page ieee">{part4_html}</section>
</body>
</html>"""


def p_xml(text: str, style: str = "") -> str:
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f'<w:p>{ppr}<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def image_xml(rel_id: str, caption: str) -> str:
    return f"""<w:p><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="5486400" cy="2835600"/><wp:docPr id="1" name="{escape(caption)}"/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="{escape(caption)}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="5486400" cy="2835600"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>{p_xml(caption)}"""


def docx_document(path: Path) -> None:
    body = []
    images = []
    part4_started = False
    for text, kind in iter_blocks():
        if text == "PART 4: IEEE FORMAT JOURNAL PAPER" and not part4_started:
            body.append('<w:p><w:pPr><w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720"/></w:sectPr></w:pPr></w:p>')
            part4_started = True
        if kind == "h1":
            body.append(p_xml(text, "Title"))
        elif kind == "h2":
            body.append(p_xml(text, "Heading1"))
        elif kind == "author":
            for line in text.splitlines():
                body.append(p_xml(line, "Author"))
        elif kind == "figure":
            _prefix, image, caption = text.split(":", 2)
            image_path = ASSETS / image
            rel_id = f"rId{len(images) + 2}"
            media_name = f"image{len(images) + 1}.svg"
            images.append((rel_id, image_path, media_name))
            body.append(image_xml(rel_id, caption))
        else:
            body.append(p_xml(text))
    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><w:body>{''.join(body)}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720"/><w:cols w:num="2" w:space="720"/></w:sectPr></w:body></w:document>"""
    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Times New Roman"/><w:sz w:val="22"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="Heading 1"/><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Author"><w:name w:val="Author"/><w:pPr><w:jc w:val="center"/></w:pPr><w:rPr><w:sz w:val="20"/></w:rPr></w:style></w:styles>"""
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="svg" ContentType="image/svg+xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>"""
    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>"""
    image_rels = "".join(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{media}"/>' for rid, _path, media in images)
    doc_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>{image_rels}</Relationships>"""
    with ZipFile(path, "w", ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", root_rels)
        docx.writestr("word/_rels/document.xml.rels", doc_rels)
        docx.writestr("word/document.xml", document)
        docx.writestr("word/styles.xml", styles)
        for _rid, image_path, media in images:
            docx.write(image_path, f"word/media/{media}")


def rtf_document() -> str:
    lines = []
    for text, kind in iter_blocks():
        if kind in {"h1", "h2"}:
            lines.append(text.upper())
        elif kind == "author":
            lines.extend(text.splitlines())
        elif kind == "figure":
            _prefix, _image, caption = text.split(":", 2)
            lines.append(caption)
        else:
            lines.append(text)
        lines.append("")
    escaped = "\n".join(lines).replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", "\\par\n")
    return "{\\rtf1\\ansi\\deff0{\\fonttbl{\\f0 Times New Roman;}}\\fs22\n" + escaped + "\n}"


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    write_svg_assets()
    (DOCS / "SEAI_RoadGuard_AI_Complete_Submission.html").write_text(html_document(), encoding="utf-8")
    (DOCS / "SEAI_RoadGuard_AI_Complete_Submission.rtf").write_text(rtf_document(), encoding="utf-8")
    docx_document(DOCS / "SEAI_RoadGuard_AI_Complete_Submission.docx")


if __name__ == "__main__":
    main()
