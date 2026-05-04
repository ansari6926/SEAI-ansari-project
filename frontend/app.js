const API_BASE = window.API_BASE || "http://localhost:8000";

const form = document.querySelector("#uploadForm");
const input = document.querySelector("#imageInput");
const preview = document.querySelector("#preview");
const emptyState = document.querySelector("#emptyState");
const apiStatus = document.querySelector("#apiStatus");
const apiUrl = document.querySelector("#apiUrl");
const button = form.querySelector("button");

apiUrl.textContent = API_BASE;

async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE}/api/v1/health`);
    const data = await response.json();
    apiStatus.textContent = data.model_loaded ? "Model ready" : "Demo mode";
  } catch {
    apiStatus.textContent = "API offline";
  }
}

function setText(id, value) {
  document.querySelector(`#${id}`).textContent = value;
}

function render(data) {
  const analytics = data.analytics || {};
  const plan = analytics.civic_repair_plan || {};

  setText("severity", analytics.severity_score ?? "-");
  setText("priority", analytics.repair_priority ?? "-");
  setText("cost", plan.estimated_cost_inr ? `INR ${plan.estimated_cost_inr}` : "-");
  setText("sla", plan.sla_hours ? `${plan.sla_hours} h` : "-");
  setText("dispatch", plan.dispatch_note || "-");
  setText("risk", plan.risk_zone || "-");
  setText("crew", plan.crew_size ?? "-");
  setText("lane", plan.lane_closure || "-");
  setText("sdg", (plan.sdg_alignment || []).join(", ") || "-");
  setText("alert", analytics.llm_alert || "-");

  const detections = document.querySelector("#detections");
  detections.innerHTML = "";
  if (!data.detections?.length) {
    detections.innerHTML = "<li>No damage detected.</li>";
  } else {
    for (const det of data.detections) {
      const item = document.createElement("li");
      item.textContent = `${det.class_name} with ${(det.confidence * 100).toFixed(1)}% confidence`;
      detections.appendChild(item);
    }
  }

  if (data.annotated_image_b64) {
    preview.src = `data:image/jpeg;base64,${data.annotated_image_b64}`;
    preview.style.display = "block";
    emptyState.style.display = "none";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!input.files.length) return;

  const body = new FormData();
  body.append("file", input.files[0]);
  button.disabled = true;
  button.textContent = "Analyzing...";

  try {
    const response = await fetch(`${API_BASE}/api/v1/detect`, {
      method: "POST",
      body,
    });
    if (!response.ok) throw new Error("Analysis failed");
    render(await response.json());
  } catch (error) {
    setText("alert", error.message);
  } finally {
    button.disabled = false;
    button.textContent = "Run analysis";
  }
});

checkHealth();
