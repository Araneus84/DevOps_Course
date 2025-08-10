# MyApp Helm Chart - DevOps Course Project Phase 3

This Helm chart deploys a simple Flask application to Kubernetes as part of a DevOps course project.

## Course Project Requirements

### Phase 3 Tasks:

1. **Package Management with Helm** ✅

   - Create Helm chart for Kubernetes application
   - Publish to artifact repository

2. **Version Control with Git** ✅

   - Git repository setup
   - Multiple branches and workflows
   - Conflict resolution and pull requests

3. **CI/CD Pipeline** ✅
   - Jenkins pipeline creation
   - Build, test, deploy stages

## Chart Components

- **Flask Application**: Simple deployment with 2 replicas
- **Horizontal Pod Autoscaler**: 2-5 replicas based on CPU (70%)
- **Persistent Volume**: 1Gi for application logs
- **Health Checks**: Liveness and readiness probes
- **ConfigMap**: Basic environment configuration

## Quick Start

```bash
# Install the chart
helm install myapp ./myapp

# Test the deployment
helm test myapp

# Access the application
kubectl port-forward svc/myapp 5000:5000
```

## Configuration

| Parameter                 | Description        | Default                |
| ------------------------- | ------------------ | ---------------------- |
| `replicaCount`            | Number of replicas | `2`                    |
| `image.repository`        | Image repository   | `suenara/myapp`        |
| `image.tag`               | Image tag          | `""` (uses appVersion) |
| `autoscaling.enabled`     | Enable HPA         | `true`                 |
| `autoscaling.maxReplicas` | Max replicas       | `5`                    |
| `persistence.size`        | PVC size           | `1Gi`                  |

## Jenkins Integration

For the CI/CD pipeline, Jenkins can deploy with:

```bash
helm upgrade --install myapp ./myapp --set image.tag=${BUILD_NUMBER}
```

This chart demonstrates key DevOps concepts: containerization, orchestration, package management, and automated deployment.

## Installation

1. Install the chart:

```bash
helm install myapp ./myapp
```

2. Or install with custom values:

```bash
helm install myapp ./myapp -f custom-values.yaml
```

## Configuration

The following table lists the configurable parameters and their default values:

| Parameter                   | Description        | Default         |
| --------------------------- | ------------------ | --------------- |
| `replicaCount`              | Number of replicas | `2`             |
| `image.repository`          | Image repository   | `suenara/myapp` |
| `image.tag`                 | Image tag          | `latest`        |
| `image.pullPolicy`          | Image pull policy  | `IfNotPresent`  |
| `service.type`              | Service type       | `ClusterIP`     |
| `service.port`              | Service port       | `5000`          |
| `resources.requests.cpu`    | CPU request        | `100m`          |
| `resources.requests.memory` | Memory request     | `128Mi`         |
| `resources.limits.cpu`      | CPU limit          | `200m`          |
| `resources.limits.memory`   | Memory limit       | `256Mi`         |
| `persistence.enabled`       | Enable persistence | `true`          |
| `persistence.size`          | PVC size           | `1Gi`           |

## Secrets

Before deploying, create the required secrets:

```bash
kubectl create secret generic myapp-secrets \
  --from-literal=API_KEY=your-api-key \
  --from-literal=DB_PASSWORD=your-db-password
```

## Uninstalling

To uninstall the release:

```bash
helm uninstall myapp
```
