pipeline {
    agent any
    
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
                bat "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                bat "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
            }
        }
        
        stage('Test Application') {
            steps {
                echo 'Testing the application...'
                bat "docker run -d --name test-app-${BUILD_NUMBER} -p 5001:5000 ${IMAGE_NAME}:${BUILD_NUMBER}"
                bat "timeout /t 10 /nobreak"
                
                // Test using PowerShell
                powershell '''
                    try {
                        $response = Invoke-WebRequest -Uri "http://localhost:5001/" -UseBasicParsing -TimeoutSec 30
                        Write-Host "✅ Test passed! Status: $($response.StatusCode)"
                    } catch {
                        Write-Host "❌ Test failed: $($_.Exception.Message)"
                        exit 1
                    }
                '''
                
                bat "docker stop test-app-${BUILD_NUMBER}"
                bat "docker rm test-app-${BUILD_NUMBER}"
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    bat "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                    bat "docker push ${IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                echo 'Deploying to Minikube...'
                
                // First, try to update existing deployment, if that fails, create new one
                bat """
                    kubectl set image deployment/myapp myapp=${IMAGE_NAME}:${BUILD_NUMBER} || kubectl create deployment myapp --image=${IMAGE_NAME}:${BUILD_NUMBER}
                """
                
                // Expose the service (ignore if already exists)
                bat 'kubectl expose deployment myapp --port=5000 --type=NodePort || echo Service already exists'
                
                // Show status
                bat 'kubectl get pods'
                bat 'kubectl get services'
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                bat 'echo Waiting for deployment to be ready...'
                bat 'kubectl wait --for=condition=available --timeout=300s deployment/myapp || echo Deployment may still be starting'
                bat 'kubectl get pods -l app=myapp'
                
                // Get the service URL
                powershell '''
                    try {
                        Write-Host "🚀 Getting service URL..."
                        $serviceUrl = kubectl get service myapp -o jsonpath='{.spec.ports[0].nodePort}'
                        if ($serviceUrl) {
                            Write-Host "✅ Service is available on NodePort: $serviceUrl"
                            Write-Host "Access your app with: minikube service myapp --url"
                        }
                    } catch {
                        Write-Host "⚠️ Could not get service URL: $($_.Exception.Message)"
                    }
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            bat 'docker system prune -f || echo Cleanup completed'
        }
        success {
            echo '🎉 Pipeline completed successfully!'
            powershell '''
                Write-Host "✅ Deployment successful!"
                Write-Host "🔗 Access your app with: minikube service myapp --url"
                Write-Host "📊 Check status with: kubectl get all"
            '''
        }
        failure {
            echo '😞 Pipeline failed!'
            echo 'Check the logs above for error details'
            // Clean up any leftover test containers
            bat "docker rm -f test-app-${BUILD_NUMBER} || echo No test container to clean"
        }
    }
}