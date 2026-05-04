# EXPERIMENT 4

## TITLE

Kubernetes Deployment of RoadSense AI

## AIM

To deploy the RoadSense AI backend as a Kubernetes application with sidecar containers and expose it through a service.

## SOFTWARE USED

- Kubernetes
- Minikube or Docker Desktop Kubernetes
- kubectl
- YAML deployment file

## DEPLOYMENT FILE

The Kubernetes configuration is stored in `deployment.yaml`. It defines:

- RoadSense backend container
- Redis sidecar container
- BusyBox sidecar container
- Three replicas
- NodePort service
- Optional OpenAI API key through Kubernetes Secret

## PROCEDURE

1. Kubernetes was enabled using Minikube or Docker Desktop.
2. The deployment file `deployment.yaml` was created.
3. The backend container image was referenced in the deployment manifest.
4. Redis and BusyBox sidecars were added to demonstrate multi-container pod deployment.
5. The deployment was applied using `kubectl apply`.
6. Running pods were checked using `kubectl get pods`.
7. The service was verified using `kubectl get services`.

## COMMANDS USED

```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get deployments
kubectl get services
kubectl describe deployment roadsense-deployment
```

## FIGURES TO ADD

Figure 4.1: deployment.yaml file  
Figure 4.2: kubectl apply command output  
Figure 4.3: Running pods list  
Figure 4.4: Kubernetes service output  
Figure 4.5: Deployment description

## RESULT

The RoadSense AI Kubernetes deployment file was prepared successfully. It can be applied on a local Kubernetes cluster after Docker Desktop or Minikube is running.
