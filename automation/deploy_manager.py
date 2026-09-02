import subprocess
import sys
import logging
from pathlib import Path
from typing import Tuple, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DeploymentManager:
    """Manages production Kubernetes deployments with pre-flight checks."""
    
    def __init__(self, chart_path: str = "../myapp", kubeconfig: Optional[str] = None):
        """
        Initialize the deployment manager.
        
        Args:
            chart_path: Path to the Helm chart directory
            kubeconfig: Optional kubeconfig path (uses default if not specified)
        """
        self.chart_path = Path(chart_path)
        self.kubeconfig = kubeconfig
        self.env = self._get_env_with_kubeconfig()
    
    def _get_env_with_kubeconfig(self) -> dict:
        """Get environment with kubeconfig if specified."""
        import os
        env = os.environ.copy()
        if self.kubeconfig:
            env['KUBECONFIG'] = self.kubeconfig
        return env
    
    def run_command(self, command: list, description: str = "") -> Tuple[bool, str]:
        """
        Run a shell command and return success status and output.
        
        Args:
            command: Command as list of strings
            description: Description of the command for logging
            
        Returns:
            Tuple of (success: bool, output: str)
        """
        try:
            logger.info(f"Running: {' '.join(command)}" + (f" ({description})" if description else ""))
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                env=self.env
            )
            
            if result.returncode == 0:
                logger.info(f"✓ {description if description else 'Command'} succeeded")
                return True, result.stdout
            else:
                logger.error(f"✗ {description if description else 'Command'} failed")
                logger.error(f"Error output: {result.stderr}")
                return False, result.stderr
        except FileNotFoundError as e:
            logger.error(f"Command not found: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Unexpected error running command: {e}")
            return False, str(e)
    
    def check_cluster_connectivity(self) -> bool:
        """
        Check if the Kubernetes cluster is reachable.
        
        Uses 'kubectl cluster-info' to verify connectivity to the production cluster.
        
        Returns:
            bool: True if cluster is reachable, False otherwise
        """
        logger.info("Checking Kubernetes cluster connectivity...")
        success, output = self.run_command(
            ["kubectl", "cluster-info"],
            "Cluster connectivity check"
        )
        
        if success:
            logger.info("✓ Cluster is reachable")
            return True
        else:
            logger.error("✗ Cannot reach Kubernetes cluster")
            logger.error("Make sure:")
            logger.error("  - Kubernetes cluster is running and accessible")
            logger.error("  - kubectl is installed and properly configured")
            logger.error("  - kubeconfig credentials are valid")
            logger.error("  - Network connectivity to cluster is available")
            return False
    
    def check_cluster_nodes(self) -> bool:
        """
        Check if cluster has available nodes.
        
        Returns:
            bool: True if at least one node is available, False otherwise
        """
        logger.info("Checking cluster nodes...")
        success, output = self.run_command(
            ["kubectl", "get", "nodes", "-o", "jsonpath={.items[*].metadata.name}"],
            "Get cluster nodes"
        )
        
        if success and output.strip():
            nodes = output.strip().split()
            logger.info(f"✓ Found {len(nodes)} node(s): {', '.join(nodes)}")
            return True
        else:
            logger.error("✗ No nodes found in cluster")
            return False
    
    def validate_helm_chart(self) -> bool:
        """
        Run helm lint to validate the Helm chart.
        
        Returns:
            bool: True if chart passes validation, False otherwise
        """
        if not self.chart_path.exists():
            logger.error(f"✗ Chart path does not exist: {self.chart_path}")
            return False
        
        logger.info(f"Validating Helm chart at {self.chart_path}...")
        success, output = self.run_command(
            ["helm", "lint", str(self.chart_path)],
            "Helm chart validation"
        )
        
        if success:
            logger.info("✓ Helm chart validation passed")
            logger.debug(f"Lint output:\n{output}")
            return True
        else:
            logger.error("✗ Helm chart validation failed")
            logger.error(f"Details:\n{output}")
            return False
    
    def run_preflight_checks(self) -> bool:
        """
        Run all pre-flight checks before deployment.
        
        Returns:
            bool: True if all checks pass, False otherwise
        """
        logger.info("=" * 60)
        logger.info("Starting pre-flight checks...")
        logger.info("=" * 60)
        
        checks = [
            ("Helm Chart Validation", self.validate_helm_chart),
            ("Cluster Connectivity", self.check_cluster_connectivity),
            ("Cluster Nodes", self.check_cluster_nodes),
        ]
        
        results = {}
        for check_name, check_func in checks:
            results[check_name] = check_func()
            logger.info("-" * 60)
        
        logger.info("=" * 60)
        if all(results.values()):
            logger.info("✓ All pre-flight checks passed!")
            logger.info("=" * 60)
            return True
        else:
            failed_checks = [name for name, result in results.items() if not result]
            logger.error(f"✗ Pre-flight checks failed: {', '.join(failed_checks)}")
            logger.info("=" * 60)
            return False
    
    def deploy(self, release_name: str = "my-app", namespace: str = "default") -> bool:
        """
        Deploy the Helm chart after passing pre-flight checks.
        
        Args:
            release_name: Helm release name
            namespace: Kubernetes namespace for deployment
            
        Returns:
            bool: True if deployment succeeded, False otherwise
        """
        if not self.run_preflight_checks():
            logger.error("Pre-flight checks failed. Aborting deployment.")
            return False
        
        logger.info("=" * 60)
        logger.info(f"Deploying {release_name} to namespace '{namespace}'...")
        logger.info("=" * 60)
        
        # Create namespace if it doesn't exist
        self.run_command(
            ["kubectl", "create", "namespace", namespace, "--dry-run=client", "-o", "yaml"],
            f"Create namespace {namespace}"
        )
        
        # Deploy using helm
        success, output = self.run_command(
            [
                "helm", "install", release_name, str(self.chart_path),
                "--namespace", namespace,
                "--create-namespace"
            ],
            f"Helm install {release_name}"
        )
        
        if success:
            logger.info("✓ Deployment completed successfully")
            logger.info(f"Release name: {release_name}")
            logger.info(f"Namespace: {namespace}")
            return True
        else:
            logger.error("✗ Deployment failed")
            return False
    
    def upgrade(self, release_name: str, namespace: str = "default") -> bool:
        """
        Upgrade an existing Helm release after passing pre-flight checks.
        
        Args:
            release_name: Helm release name to upgrade
            namespace: Kubernetes namespace
            
        Returns:
            bool: True if upgrade succeeded, False otherwise
        """
        if not self.run_preflight_checks():
            logger.error("Pre-flight checks failed. Aborting upgrade.")
            return False
        
        logger.info("=" * 60)
        logger.info(f"Upgrading release {release_name} in namespace '{namespace}'...")
        logger.info("=" * 60)
        
        success, output = self.run_command(
            [
                "helm", "upgrade", release_name, str(self.chart_path),
                "--namespace", namespace
            ],
            f"Helm upgrade {release_name}"
        )
        
        if success:
            logger.info("✓ Upgrade completed successfully")
            return True
        else:
            logger.error("✗ Upgrade failed")
            return False


def main():
    """Example usage of DeploymentManager."""
    # Initialize the deployment manager
    manager = DeploymentManager(chart_path="../myapp")
    
    # Option 1: Run pre-flight checks only
    if not manager.run_preflight_checks():
        logger.error("Pre-flight checks failed. Exiting.")
        sys.exit(1)
    
    # Option 2: Deploy (includes pre-flight checks)
    # if not manager.deploy(release_name="my-app", namespace="default"):
    #     sys.exit(1)
    
    # Option 3: Upgrade existing deployment (includes pre-flight checks)
    # if not manager.upgrade(release_name="my-app", namespace="default"):
    #     sys.exit(1)
    
    logger.info("Deployment manager ready for use")


if __name__ == "__main__":
    main()
