# DevOps Project: Initial Setup and Dockerization

---

## Project Overview

This repository contains the foundational elements for a DevOps project, focusing on containerization with Docker and deployment to Kubernetes. The initial phase involves building a Docker image and running it using `docker-compose`. The project has now evolved to include advanced Kubernetes features like ConfigMaps, Secrets, Health Probes, and CronJobs.

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following software installed on your system:

- **Git:** For cloning the repository.
  - [Download Git](https://git-scm.com/downloads)
- **Docker Engine:** For building and running Docker containers.
  - [Install Docker Engine](https://docs.docker.com/engine/install/)
- **Kubernetes CLI (kubectl):** For interacting with Kubernetes clusters.
  - [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- **Minikube (optional):** For local Kubernetes development.
  - [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)

You can verify your Docker installation by running:

```bash
docker --version
kubectl version --client
```

### Installation and Setup

#### Docker Setup

Follow these steps to get your initial Docker image built and running:

1.  **Clone the Repository:**
    Navigate to your desired directory and clone this repository:

    ```bash
    git clone <your-repository-url>
    cd <your-repository-folder-name>
    ```

2.  **Build the Docker Image:**
    From the root of your project directory (where `Dockerfile` and `docker-compose.yaml` are located), build your Docker image.

    ```bash
    docker build -t suenara/myapp:1 .
    ```

3.  **Verify the Docker Image:**
    Confirm that your newly built image is listed:

    ```bash
    docker images
    ```

4.  **Run with Docker Compose:**
    Start your application using Docker Compose:

    ```bash
    docker-compose up -d
    ```

5.  **Verify Running Containers:**
    Check that your container(s) are running:

    ```bash
    docker ps
    ```

#### Kubernetes Deployment

Follow these steps to deploy your application to Kubernetes:

1. **Create Namespace (Optional):**

   ```bash
   kubectl create namespace myapp
   kubectl config set-context --current --namespace=myapp
   ```

2. **Deploy ConfigMap and Secrets:**

   ```bash
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/secrets.yaml
   ```

3. **Create PersistentVolumeClaim:**

   ```bash
   kubectl apply -f k8s/pvc.yaml
   ```

4. **Deploy the Application:**

   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

5. **Configure Autoscaling:**

   ```bash
   kubectl apply -f k8s/ha.yaml
   ```

6. **Set Up CronJob:**

   ```bash
   kubectl apply -f k8s/cronjob.yaml
   ```

7. **Verify Deployment:**

   ```bash
   kubectl get all
   kubectl get cm,secrets,pvc,cronjobs
   ```

8. **Access the Application:**

   ```bash
   # For minikube
   minikube service myapp-service

   # For standard kubernetes
   kubectl get service myapp-service
   # Note the NodePort and access via http://node-ip:nodePort
   ```

## Cleanup

To remove all Kubernetes resources:

```bash
kubectl delete -f k8s/
```

---

## Kubernetes Configuration Details

### ConfigMaps and Secrets

Our application uses ConfigMaps and Secrets to externalize configuration:

- **ConfigMap (`k8s/configmap.yaml`):** Stores non-sensitive configuration like environment settings, log levels, and feature flags.
- **Secret (`k8s/secrets.yaml`):** Stores sensitive information like API keys and database credentials.

### Health Monitoring

The application implements two types of probes to ensure proper health monitoring:

- **Liveness Probe:** Checks if the application is running. If this check fails, Kubernetes restarts the container.
- **Readiness Probe:** Checks if the application is ready to receive traffic. If this check fails, Kubernetes stops sending traffic to the pod until it passes.

### Autoscaling

The application uses Horizontal Pod Autoscaling to automatically scale based on CPU utilization:

- **HPA (`k8s/ha.yaml`):** Configures autoscaling with a minimum of 2 replicas and a maximum of 5, targeting 50% CPU utilization.

### Automated Tasks

The application uses CronJobs to automate periodic tasks:

- **CronJob (`k8s/cronjob.yaml`):** Runs a usage report generation task hourly to collect and analyze application metrics.

### Persistent Storage

The application uses persistent storage for logs:

- **PersistentVolumeClaim (`k8s/pvc.yaml`):** Requests storage for application logs that persists across pod restarts.

---

## Project Structure

```
.
├── app.py                       # Main application code
├── Dockerfile                   # Defines the Docker image
├── docker-compose.yaml          # Orchestrates Docker containers locally
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── app/                         # Application source code
├── class4/                      # Class 4 exercises and examples
├── Data/                        # Data files
├── k8s/                         # Kubernetes manifests
│   ├── deployment.yaml          # Kubernetes Deployment manifest
│   ├── service.yaml             # Kubernetes Service manifest
│   ├── ha.yaml                  # Kubernetes HorizontalPodAutoscaler manifest
│   ├── configmap.yaml           # Kubernetes ConfigMap manifest
│   ├── secrets.yaml             # Kubernetes Secret manifest
│   ├── pvc.yaml                 # Kubernetes PersistentVolumeClaim manifest
│   └── cronjob.yaml             # Kubernetes CronJob manifest
└── logs/                        # Directory for application logs
```

---

## Future Enhancements (Roadmap)

As the project progresses, we plan to integrate and expand upon the following areas:

- **CI/CD Pipeline:** Implementing automated build, test, and deployment workflows.
- **Advanced Monitoring:** Setting up Prometheus and Grafana for comprehensive metrics.
- **Service Mesh:** Implementing Istio for advanced traffic management.
- **GitOps:** Setting up ArgoCD or Flux for GitOps-based deployments.
- **Security Scanning:** Implementing container and code security scanning.
- **Infrastructure as Code (IaC):** Defining infrastructure using Terraform.
- **Multi-environment Support:** Configuring different environments (dev, staging, prod).

---

## Contributing

We welcome contributions to this project! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## Acknowledgments

- Special thanks to the instructor for guiding us through this DevOps journey.
