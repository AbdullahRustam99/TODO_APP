# Quickstart: Deploying the Todo App to Kubernetes

This guide provides the steps to deploy the Todo App to a local Kubernetes cluster.

## Prerequisites

- Docker Desktop with Kubernetes enabled
- `kubectl` configured to use the Docker Desktop context
- Helm installed

## Deployment Steps

1.  **Build and Push Docker Images**:
    Before deploying to Kubernetes, you need to build the Docker images for the frontend, backend, and AI-service applications and push them to a container registry.

2.  **Create Kubernetes Secrets**:
    Create the necessary secrets for the backend and AI-service.

    ```bash
    kubectl create secret generic backend-secrets --from-literal=database-url=...
    kubectl create secret generic ai-service-secrets --from-literal=api-key=...
    ```

3.  **Deploy with Helm**:
    Navigate to the `charts` directory and deploy each application using Helm.

    ```bash
    helm install frontend ./frontend
    helm install backend ./backend
    helm install ai-service ./ai-service
    ```

4.  **Verify the Deployment**:
    Check the status of the pods and services.

    ```bash
    kubectl get pods
    kubectl get services
    ```

5.  **Access the Application**:
    The frontend service is exposed using a NodePort. Find the port and access the application in your browser at `http://localhost:<node-port>`.

    ```bash
    kubectl get svc frontend
    ```
