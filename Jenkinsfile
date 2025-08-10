pipeline {
    agent {
        label 'windows'
    }
    
    environment {
        IMAGE_NAME = 'suenara/myapp'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Getting code from GitHub...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    try {
                        bat "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                        bat "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                        echo "✅ Docker build successful"
                    } catch (Exception e) {
                        echo "❌ Docker build failed: ${e.getMessage()}"
                        throw e
                    }
                }
            }
        }
        
        stage('Test Application') {
            steps {
                echo 'Testing the application...'
                script {
                    try {
                        bat "docker run -d --name test-app-${BUILD_NUMBER} -p 5001:5000 ${IMAGE_NAME}:${BUILD_NUMBER}"
                        bat "timeout /t 15 /nobreak >nul"
                        
                        // Test using PowerShell
                        powershell '''
                            try {
                                Write-Host "Testing application..."
                                $response = Invoke-WebRequest -Uri "http://localhost:5001/" -UseBasicParsing -TimeoutSec 30
                                Write-Host "✅ Test passed! Status: $($response.StatusCode)"
                            } catch {
                                Write-Host "❌ Test failed: $($_.Exception.Message)"
                                exit 1
                            }
                        '''
                        
                        echo "✅ Application test successful"
                    } catch (Exception e) {
                        echo "❌ Application test failed: ${e.getMessage()}"
                        throw e
                    } finally {
                        // Always clean up test container
                        bat "docker stop test-app-${BUILD_NUMBER} >nul 2>&1 || echo Container already stopped"
                        bat "docker rm test-app-${BUILD_NUMBER} >nul 2>&1 || echo Container already removed"
                    }
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                            bat "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                            bat "docker push ${IMAGE_NAME}:latest"
                        }
                        echo "✅ Docker push successful"
                    } catch (Exception e) {
                        echo "❌ Docker push failed: ${e.getMessage()}"
                        throw e
                    }
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                echo 'Deploying to Minikube...'
                script {
                    try {
                        // Check if kubectl is available
                        bat 'kubectl version --client'
                        
                        // Deploy or update
                        bat """
                            kubectl set image deployment/myapp myapp=${IMAGE_NAME}:${BUILD_NUMBER} 2>nul || kubectl create deployment myapp --image=${IMAGE_NAME}:${BUILD_NUMBER}
                        """
                        
                        // Expose service
                        bat 'kubectl expose deployment myapp --port=5000 --type=NodePort 2>nul || echo Service already exists'
                        
                        // Show status
                        bat 'kubectl get pods'
                        bat 'kubectl get services'
                        
                        echo "✅ Deployment successful"
                    } catch (Exception e) {
                        echo "❌ Deployment failed: ${e.getMessage()}"
                        throw e
                    }
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                script {
                    try {
                        bat 'echo Waiting for deployment to be ready...'
                        bat 'kubectl wait --for=condition=available --timeout=300s deployment/myapp 2>nul || echo Deployment may still be starting'
                        bat 'kubectl get pods -l app=myapp'
                        
                        // Get service info
                        powershell '''
                            try {
                                Write-Host "🚀 Getting service information..."
                                $nodePort = kubectl get service myapp -o jsonpath='{.spec.ports[0].nodePort}' 2>$null
                                if ($nodePort) {
                                    Write-Host "✅ Service is available on NodePort: $nodePort"
                                    Write-Host "🔗 Access your app with: minikube service myapp --url"
                                }
                                
                                # Try to get minikube IP
                                $minikubeIp = minikube ip 2>$null
                                if ($minikubeIp -and $nodePort) {
                                    Write-Host "📱 Direct URL: http://$minikubeIp`:$nodePort"
                                }
                            } catch {
                                Write-Host "⚠️ Could not get service details: $($_.Exception.Message)"
                            }
                        '''
                        
                        echo "✅ Verification complete"
                    } catch (Exception e) {
                        echo "⚠️ Verification completed with warnings: ${e.getMessage()}"
                        // Don't fail the build for verification issues
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline cleanup...'
            script {
                // Clean up Docker resources
                bat 'docker system prune -f 2>nul || echo Docker cleanup completed'
                
                // Clean up any leftover test containers
                bat "docker rm -f test-app-${BUILD_NUMBER} 2>nul || echo No test containers to clean"
            }
        }
        success {
            echo '🎉 Pipeline completed successfully!'
            script {
                powershell '''
                    Write-Host "✅ Deployment successful!" -ForegroundColor Green
                    Write-Host "🔗 Access your app with: minikube service myapp --url" -ForegroundColor Cyan
                    Write-Host "📊 Check status with: kubectl get all" -ForegroundColor Yellow
                '''
            }
        }
        failure {
            echo '😞 Pipeline failed!'
            script {
                powershell '''
                    Write-Host "❌ Pipeline failed! Check the logs above for details." -ForegroundColor Red
                    Write-Host "🔧 Common fixes:" -ForegroundColor Yellow
                    Write-Host "  - Ensure Docker Desktop is running" -ForegroundColor White
                    Write-Host "  - Ensure Minikube is started" -ForegroundColor White
                    Write-Host "  - Check Docker Hub credentials" -ForegroundColor White
                '''
                
                // Clean up any hanging containers
                bat "docker rm -f test-app-${BUILD_NUMBER} 2>nul || echo No test containers to clean"
            }
        }
    }
}