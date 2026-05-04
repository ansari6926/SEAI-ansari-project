# EXPERIMENT 3

## TITLE

Containerization, Git Version Control, GitHub, and Docker Hub Deployment

## AIM

To containerize RoadSense AI using Docker, maintain the project using Git version control, and prepare the project for GitHub and Docker Hub publication.

## SOFTWARE USED

- Docker Desktop
- Docker Compose
- Git
- GitHub
- Docker Hub

## PROCEDURE

The project was initialized as a Git repository. All files were staged and committed using Git commands. A backend Dockerfile was created using the `python:3.10-slim` base image. It installs dependencies from `requirements.txt`, copies backend source files, exposes port 8000, and starts Uvicorn.

A frontend Dockerfile was created using `nginx:1.25-alpine`. It copies static HTML, CSS, and JavaScript files into the Nginx web directory and exposes port 80. Docker Compose was configured to run the backend, frontend, and Redis service together.

The Docker publishing script `scripts/docker_publish.sh` was created to build and push backend and frontend images to Docker Hub.

## GIT COMMANDS USED

```bash
git init
git add .
git commit -m "Build RoadSense AI mini project"
git commit -m "Add shareable submission package and local runner"
git status
```

## DOCKER COMMANDS USED

```bash
docker compose up --build
docker build -t yourusername/roadsense-ai-backend:latest ./backend
docker build -t yourusername/roadsense-ai-frontend:latest ./frontend
docker push yourusername/roadsense-ai-backend:latest
docker push yourusername/roadsense-ai-frontend:latest
```

## FILES CREATED

- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`
- `scripts/build_and_run.sh`
- `scripts/docker_publish.sh`

## FIGURES TO ADD

Figure 3.1: Git commit history  
Figure 3.2: Docker Compose configuration  
Figure 3.3: Docker build output  
Figure 3.4: Docker images listed locally  
Figure 3.5: Docker Hub repository page  
Figure 3.6: GitHub repository page

## RESULT

RoadSense AI was successfully prepared for GitHub and Docker Hub publication. The application includes separate Docker images for backend and frontend services.
