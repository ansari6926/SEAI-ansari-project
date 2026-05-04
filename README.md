# RoadGuard AI

RoadGuard AI is a full-stack demo system for road damage monitoring, civic analytics, and automated maintenance prioritization. It provides a localhost dashboard with AI-style damage inference, incident mapping data, ward analytics, budget impact estimates, and a prioritized maintenance queue.

## Features

- FastAPI backend with REST endpoints for road incident data, analytics, and image-style damage prediction.
- Interactive dashboard for civic teams to monitor potholes, cracks, rutting, and surface wear.
- Automated priority scoring based on damage severity, traffic density, civic risk, and reporting frequency.
- Demo prediction tool that accepts road image metadata and returns a structured maintenance recommendation.
- Lightweight setup with no database or heavy ML downloads required.

## Tech Stack

- Backend: Python, FastAPI, Uvicorn
- Frontend: HTML, CSS, JavaScript
- Data: In-memory civic incident dataset for localhost demonstration

## Run Locally

1. Create and activate a Python virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install backend dependencies.

```powershell
pip install -r backend/requirements.txt
```

3. Start the localhost server.

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

4. Open the app.

```text
http://127.0.0.1:8000
```

## Quick Script

On Windows PowerShell, you can also run:

```powershell
.\scripts\run_local.ps1
```

## API Endpoints

- `GET /api/health` - service health and model status
- `GET /api/incidents` - road damage incident records
- `GET /api/analytics` - ward-level civic analytics
- `POST /api/predict` - simulated deep learning prediction and maintenance priority

## Project Note

This project is designed for academic proof-of-work and localhost presentation. The prediction engine is a deterministic demo model that behaves like an inference service without requiring large trained model files.

