# Data Model for Kubernetes Deployment

This document describes the key entities for the Kubernetes deployment, which are the Kubernetes objects themselves.

## Kubernetes Objects

### Frontend
- **Deployment**: Manages the frontend application pods.
  - **Replicas**: Defines the number of frontend pods to run.
  - **Container**: The frontend application container image and port.
  - **Probes**: Liveness and readiness probes to ensure the frontend is healthy.
- **Service**: Exposes the frontend deployment.
  - **Type**: NodePort or LoadBalancer to expose the service outside the cluster.
  - **Ports**: Maps the service port to the container port.

### Backend
- **Deployment**: Manages the backend application pods.
  - **Replicas**: Defines the number of backend pods to run.
  - **Container**: The backend application container image and port.
  - **Probes**: Liveness and readiness probes to ensure the backend is healthy.
  - **Secrets**: Mounts Kubernetes secrets for database credentials and other sensitive data.
- **Service**: Exposes the backend deployment.
  - **Type**: ClusterIP, as it only needs to be accessible within the cluster.
  - **Ports**: Maps the service port to the container port.

### AI-Service
- **Deployment**: Manages the AI-service application pods.
  - **Replicas**: Defines the number of AI-service pods to run.
  - **Container**: The AI-service application container image and port.
  - **Probes**: Liveness and readiness probes to ensure the AI-service is healthy.
  - **Secrets**: Mounts Kubernetes secrets for the AI service API key.
- **Service**: Exposes the AI-service deployment.
  - **Type**: ClusterIP, as it only needs to be accessible within the cluster.
  - **Ports**: Maps the service port to the container port.
