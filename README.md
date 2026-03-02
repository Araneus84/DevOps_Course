# DevOps Project: Container Orchestration and Package Management

---

## Project Overview

This repository contains a comprehensive DevOps project demonstrating containerization, Kubernetes orchestration, and Helm package management. The project has evolved through multiple phases, now including advanced Kubernetes features, Helm charts, and CI/CD pipeline integration.

### Project Phases:

- **Phase 1:** Docker containerization and basic deployment
- **Phase 2:** Kubernetes deployment with advanced features
- **Phase 3:** Helm package management, Git workflows, and CI/CD pipeline (Current)

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following software installed on your system:

- **Git:** For version control and repository management.
  - [Download Git](https://git-scm.com/downloads)
- **Docker Engine:** For building and running Docker containers.
  - [Install Docker Engine](https://docs.docker.com/engine/install/)
- **Kubernetes CLI (kubectl):** For interacting with Kubernetes clusters.
  - [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- **Helm:** For Kubernetes package management.
  - [Install Helm](https://helm.sh/docs/intro/install/)
- **Jenkins:** For CI/CD pipeline automation.
  - [Install Jenkins](https://www.jenkins.io/doc/book/installing/)
- **Minikube (optional):** For local Kubernetes development.
  - [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)

You can verify your installations by running:

```bash
docker --version
kubectl version --client
helm version
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

#### Helm Package Management (Phase 3 - Current)

The latest phase introduces Helm for Kubernetes package management, providing templating and version control for deployments:

1. **Navigate to Helm Chart Directory:**

   ```bash
   cd myapp
   ```

2. **Validate the Helm Chart:**

   ```bash
   helm lint .
   ```

3. **Install Application with Helm:**

   ```bash
   # Install the chart
   helm install myapp .

   # Or install with custom image tag (for CI/CD)
   helm install myapp . --set image.tag=1.0.1
   ```

4. **Verify Helm Deployment:**

   ```bash
   helm list
   kubectl get all
   ```

5. **Test the Application:**

   ```bash
   helm test myapp
   ```

6. **Access the Application:**

   ```bash
   kubectl port-forward svc/myapp 5000:5000
   # Then visit: http://localhost:5000
   ```

7. **Upgrade the Application:**

   ```bash
   helm upgrade myapp . --set image.tag=1.0.2
   ```

8. **Uninstall the Application:**

   ```bash
   helm uninstall myapp
   ```

#### Manual Kubernetes Deployment (Legacy - Phase 2)

For direct Kubernetes deployment without Helm:

<details>
<summary>Click to expand manual Kubernetes deployment steps</summary>

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

</details>

---

## Phase 3: DevOps Course Requirements

### ✅ Package Management with Helm

**Objective:** Create a Helm chart for Kubernetes application management.

- **Helm Chart Location:** `/myapp/`
- **Key Components:**
  - Chart.yaml - Chart metadata and versioning
  - values.yaml - Configurable parameters
  - templates/ - Kubernetes manifest templates
  - README.md - Chart documentation

**Features Implemented:**

- Templated Kubernetes deployments
- Configurable values for different environments
- Horizontal Pod Autoscaling (HPA)
- Persistent volume management
- Health checks and probes
- Service discovery

### ✅ Version Control with Git

**Objective:** Demonstrate Git workflows and collaboration.

- **Repository Structure:** Well-organized with clear branching strategy
- **Branches:**
  - `main` - Production-ready code
  - `projectPhase3` - Current development branch
  - Feature branches for specific implementations

**Git Workflows Demonstrated:**

- Feature branch workflow
- Pull request process
- Conflict resolution
- Merge strategies

### ✅ CI/CD Pipeline Integration

**Objective:** Jenkins pipeline for automated build, test, and deploy.

**Jenkins Integration Points:**

- Automated Docker image building
- Helm chart deployment with dynamic versioning
- Environment-specific deployments
- Automated testing with `helm test`

**Pipeline Stages:**

```groovy
pipeline {
    stages {
        stage('Build') {
            // Docker image build
        }
        stage('Test') {
            // Application and chart testing
        }
        stage('Deploy') {
            // Helm deployment
        }
    }
}
```

---

## Helm Chart Details

### Chart Structure

```
myapp/
├── Chart.yaml                  # Chart metadata and version
├── values.yaml                 # Default configuration values
├── README.md                   # Chart documentation
└── templates/
    ├── deployment.yaml         # Application deployment template
    ├── service.yaml            # Service template
    ├── configmap.yaml          # ConfigMap template
    ├── pvc.yaml               # PersistentVolumeClaim template
    ├── hpa.yaml               # HorizontalPodAutoscaler template
    ├── NOTES.txt              # Post-installation notes
    └── tests/
        └── test-connection.yaml # Chart tests
```

### Key Configuration Options

| Parameter                 | Description        | Default                |
| ------------------------- | ------------------ | ---------------------- |
| `replicaCount`            | Number of replicas | `2`                    |
| `image.repository`        | Image repository   | `suenara/myapp`        |
| `image.tag`               | Image tag          | `""` (uses appVersion) |
| `service.port`            | Service port       | `5000`                 |
| `autoscaling.enabled`     | Enable HPA         | `true`                 |
| `autoscaling.maxReplicas` | Maximum replicas   | `5`                    |
| `persistence.size`        | PVC size           | `1Gi`                  |
| `resources.limits.cpu`    | CPU limit          | `200m`                 |
| `resources.limits.memory` | Memory limit       | `256Mi`                |

### Helm Commands Reference

```bash
# Install
helm install myapp ./myapp

# Upgrade
helm upgrade myapp ./myapp --set image.tag=v1.1.0

# Rollback
helm rollback myapp 1

# Status
helm status myapp

# History
helm history myapp

# Test
helm test myapp

# Uninstall
helm uninstall myapp
```

---

## Legacy Kubernetes Configuration Details

<details>
<summary>Click to expand legacy Kubernetes configuration details</summary>

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

</details>

---

## Project Structure

```
.
├── app.py                       # Main Flask application code
├── Dockerfile                   # Docker image definition
├── docker-compose.yaml          # Local container orchestration
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── myapp/                       # Helm chart directory (Phase 3)
│   ├── Chart.yaml              # Chart metadata
│   ├── values.yaml             # Chart configuration values
│   ├── README.md               # Chart documentation
│   └── templates/              # Kubernetes templates
│       ├── deployment.yaml     # Deployment template
│       ├── service.yaml        # Service template
│       ├── configmap.yaml      # ConfigMap template
│       ├── pvc.yaml           # PVC template
│       ├── hpa.yaml           # HPA template
│       ├── NOTES.txt          # Installation notes
│       └── tests/             # Chart tests
├── app/                         # Application source code
├── class4/                      # Class 4 exercises and examples
├── Data/                        # Data files
├── k8s/                         # Legacy Kubernetes manifests (Phase 2)
│   ├── deployment.yaml          # Direct Kubernetes deployment
│   ├── service.yaml             # Direct Kubernetes service
│   ├── ha.yaml                  # Direct HPA configuration
│   ├── configmap.yaml           # Direct ConfigMap
│   ├── secrets.yaml             # Direct Secret
│   ├── pvc.yaml                 # Direct PVC
│   └── cronjob.yaml             # Direct CronJob
└── logs/                        # Directory for application logs
```

---

## Future Enhancements (Course Roadmap)

### Completed ✅

- **Docker Containerization:** Application containerized with multi-stage builds
- **Kubernetes Deployment:** Advanced K8s features (HPA, PVC, ConfigMaps, Secrets)
- **Helm Package Management:** Chart creation and templating
- **Version Control:** Git workflows and branching strategies
- **CI/CD Foundation:** Jenkins pipeline structure

### Next Phase Goals 🎯

- **CI/CD Pipeline Implementation:** Complete Jenkins automation
- **Artifact Repository:** Helm chart publishing to repository
- **Advanced Testing:** Automated testing integration
- **Monitoring Setup:** Basic metrics and logging
- **Documentation:** Complete project documentation

### Future Considerations 🚀

- **Advanced Monitoring:** Prometheus and Grafana integration
- **Service Mesh:** Istio for traffic management
- **GitOps:** ArgoCD for declarative deployments
- **Security Scanning:** Container and code vulnerability scanning
- **Infrastructure as Code:** Terraform for infrastructure management
- **Multi-environment Support:** Dev/staging/prod environment automation

---

## Contributing

We welcome contributions to this DevOps course project! Please follow these steps:

1.  **Fork the repository**
2.  **Create a feature branch:** `git checkout -b feature/AmazingFeature`
3.  **Commit your changes:** `git commit -m 'Add some AmazingFeature'`
4.  **Push to the branch:** `git push origin feature/AmazingFeature`
5.  **Open a Pull Request**

### Course Project Guidelines

- Follow the phase-based approach
- Maintain backward compatibility with previous phases
- Document all changes in README files
- Test thoroughly before submitting

---

## Course Project Status

**Current Phase:** Phase 3 - Package Management & CI/CD  
**Branch:** `projectPhase3`  
**Completion Status:**

- ✅ Helm Chart Creation
- ✅ Git Workflow Implementation
- ✅ CI/CD Pipeline Development (Complete)

## CI/CD Pipeline

### Jenkins Pipeline Overview

The project includes a complete Jenkins CI/CD pipeline that automates the build, test, and deployment process:

**Pipeline Stages:**

1. **Checkout** - Retrieves source code from Git repository
2. **Build** - Creates Docker image with unique build number tag
3. **Test** - Runs comprehensive test suite including:
   - Python application tests with proper encoding
   - Docker container validation
   - Health check verification
4. **Push** - Publishes Docker image to Docker Hub registry
5. **Deploy** - Deploys application to Kubernetes using Helm

### Testing Strategy

The pipeline implements multi-layered testing:

- **Unit Tests**: Python-based application testing
- **Container Tests**: Docker image validation and health checks
- **Integration Tests**: End-to-end application functionality verification

### Helm Integration

The CI/CD pipeline leverages Helm for:

- **Package Management**: Standardized Kubernetes deployments
- **Configuration Management**: Environment-specific values
- **Release Management**: Versioned deployments with rollback capability
- **Template Reusability**: Consistent deployment patterns

### Pipeline Configuration

- **Trigger**: Automated on Git push to main branch
- **Environment**: Windows-compatible PowerShell execution
- **Registry**: Docker Hub integration for image storage
- **Deployment Target**: Minikube local Kubernetes cluster

### Usage

```bash
# Pipeline automatically triggers on push, or run manually:
# 1. Access Jenkins dashboard
# 2. Select pipeline job
# 3. Click "Build Now"
# 4. Monitor build progress and deployment
```

---

## Acknowledgments

- **Course Instructor:** For providing comprehensive DevOps guidance
- **DevOps Community:** For best practices and tooling recommendations
- **Open Source Projects:** Docker, Kubernetes, Helm, and Jenkins teams

