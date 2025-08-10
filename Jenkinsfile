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
                script {
                    if (isUnix()) {
                        sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                        sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                    } else {
                        bat "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                        bat "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                    }
                }
            }
        }
        
        stage('Test Application') {
            steps {
                echo 'Testing the application...'
                script {
                    if (isUnix()) {
                        // Linux/Unix commands
                        sh "docker run -d --name test-app-${BUILD_NUMBER} -p 5001:5000 ${IMAGE_NAME}:${BUILD_NUMBER}"
                        sh "sleep 10"
                        sh "curl -f http://localhost:5001/ || exit 1"
                        sh "docker stop test-app-${BUILD_NUMBER}"
                        sh "docker rm test-app-${BUILD_NUMBER}"
                    } else {
                        // Windows commands
                        bat "docker run -d --name test-app-${BUILD_NUMBER} -p 5001:5000 ${IMAGE_NAME}:${BUILD_NUMBER}"
                        bat "timeout /t 10 /nobreak"
                        bat """
                            powershell -Command "try { Invoke-WebRequest -Uri http://localhost:5001/ -UseBasicParsing | Out-Null; Write-Host 'Test passed' } catch { Write-Host 'Test failed'; exit 1 }"
                        """
                        bat "docker stop test-app-${BUILD_NUMBER}"
                        bat "docker rm test-app-${BUILD_NUMBER}"
                    }
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        if (isUnix()) {
                            sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                            sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                            sh "docker push ${IMAGE_NAME}:latest"
                        } else {
                            bat "echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin"
                            bat "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                            bat "docker push ${IMAGE_NAME}:latest"
                        }
                    }
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                echo 'Deploying to Minikube...'
                script {
                    if (isUnix()) {
                        // Linux/Unix deployment
                        sh """
                            kubectl set image deployment/myapp myapp=${IMAGE_NAME}:${BUILD_NUMBER} || \
                            kubectl create deployment myapp --image=${IMAGE_NAME}:${BUILD_NUMBER}
                            
                            kubectl expose deployment myapp --port=5000 --type=NodePort || echo "Service already exists"
                            
                            kubectl get pods
                            kubectl get services
                        """
                    } else {
                        // Windows deployment
                        bat """
                            kubectl set image deployment/myapp myapp=${IMAGE_NAME}:${BUILD_NUMBER} || kubectl create deployment myapp --image=${IMAGE_NAME}:${BUILD_NUMBER}
                            kubectl expose deployment myapp --port=5000 --type=NodePort || echo Service already exists
                            kubectl get pods
                            kubectl get services
                        """
                    }
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                script {
                    if (isUnix()) {
                        sh """
                            echo "Waiting for deployment to be ready..."
                            kubectl wait --for=condition=available --timeout=300s deployment/myapp || echo "Deployment may still be starting"
                            kubectl get pods -l app=myapp
                        """
                    } else {
                        bat """
                            echo Waiting for deployment to be ready...
                            kubectl wait --for=condition=available --timeout=300s deployment/myapp || echo Deployment may still be starting
                            kubectl get pods -l app=myapp
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            script {
                if (isUnix()) {
                    sh "docker system prune -f || true"
                } else {
                    bat "docker system prune -f || echo Cleanup completed"
                }
            }
        }
        success {
            echo 'Pipeline completed successfully! 🎉'
            script {
                if (isUnix()) {
                    sh "echo 'Deployment successful! Access your app with: minikube service myapp --url'"
                } else {
                    bat "echo Deployment successful! Access your app with: minikube service myapp --url"
                }
            }
        }
        failure {
            echo 'Pipeline failed! 😞'
            script {
                echo 'Check the logs above for error details'
                // Clean up any leftover test containers
                if (isUnix()) {
                    sh "docker rm -f test-app-${BUILD_NUMBER} || true"
                } else {
                    bat "docker rm -f test-app-${BUILD_NUMBER} || echo No test container to clean"
                }
            }
        }
    }
}