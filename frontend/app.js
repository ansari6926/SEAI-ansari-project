const currency = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 0,
});

const metricConfig = [
  ["total_incidents", "Detected road issues"],
  ["critical_incidents", "Critical repairs"],
  ["average_priority", "Average priority"],
  ["estimated_budget", "Estimated budget"],
];

async function api(path, options) {
  const response = await fetch(path, options);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function renderMetrics(analytics) {
  const metrics = document.querySelector("#metrics");
  metrics.innerHTML = metricConfig
    .map(([key, label]) => {
      const value = key === "estimated_budget" ? currency.format(analytics[key]) : analytics[key];
      return `<article class="metric"><span>${label}</span><strong>${value}</strong></article>`;
    })
    .join("");
}

function renderMap(incidents) {
  const map = document.querySelector("#cityMap");
  const positions = [
    [18, 36],
    [66, 30],
    [75, 58],
    [34, 68],
    [58, 76],
    [45, 44],
  ];
  map.innerHTML = '<div class="road a"></div><div class="road b"></div><div class="road c"></div>';
  incidents.forEach((incident, index) => {
    const [left, top] = positions[index % positions.length];
    const pin = document.createElement("div");
    pin.className = `pin ${incident.status.toLowerCase()}`;
    pin.style.left = `${left}%`;
    pin.style.top = `${top}%`;
    pin.dataset.label = `${incident.id} · ${incident.priority_score}`;
    map.appendChild(pin);
  });
  document.querySelector("#incidentCount").textContent = `${incidents.length} reports`;
}

function renderQueue(incidents) {
  document.querySelector("#queueBody").innerHTML = incidents
    .map(
      (incident) => `
        <tr>
          <td>${incident.id}</td>
          <td>${incident.location}</td>
          <td>${incident.damage_type}</td>
          <td><strong>${incident.priority_score}</strong></td>
          <td><span class="badge ${incident.status}">${incident.status}</span></td>
          <td>${currency.format(incident.estimated_cost)}</td>
        </tr>
      `,
    )
    .join("");
}

function renderPrediction(prediction) {
  document.querySelector("#predictionResult").innerHTML = `
    <strong>${prediction.predicted_damage}</strong><br />
    Confidence: ${prediction.confidence}%<br />
    Priority score: ${prediction.priority_score}<br />
    Recommendation: ${prediction.recommendation}<br />
    Maintenance window: ${prediction.maintenance_window}
  `;
}

async function loadDashboard() {
  const [health, analytics, incidents] = await Promise.all([
    api("/api/health"),
    api("/api/analytics"),
    api("/api/incidents"),
  ]);
  document.querySelector("#serviceStatus").textContent = `${health.status} · ${health.model}`;
  renderMetrics(analytics);
  renderMap(incidents);
  renderQueue(incidents);
}

document.querySelector("#predictForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const payload = Object.fromEntries(form.entries());
  payload.traffic_density = Number(payload.traffic_density);
  payload.visual_damage_score = Number(payload.visual_damage_score);
  payload.citizen_reports = Number(payload.citizen_reports);
  renderPrediction(await api("/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }));
});

loadDashboard().catch((error) => {
  document.querySelector("#serviceStatus").textContent = "API unavailable";
  console.error(error);
});

