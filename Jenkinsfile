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
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                    sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Test Application') {
            steps {
                echo 'Testing the application...'
                script {
                    // Start container for testing
                    sh "docker run -d --name test-app-${BUILD_NUMBER} -p 5001:5000 ${IMAGE_NAME}:${BUILD_NUMBER}"
                    
                    // Wait a bit for the app to start
                    sh "sleep 10"
                    
                    // Simple test - check if app responds
                    sh "curl -f http://localhost:5001/ || exit 1"
                    
                    // Clean up test container
                    sh "docker stop test-app-${BUILD_NUMBER}"
                    sh "docker rm test-app-${BUILD_NUMBER}"
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                        sh "docker push ${IMAGE_NAME}:latest"
                    }
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                echo 'Deploying to Minikube...'
                script {
                    // Simple deployment using kubectl (easier than Helm for students)
                    sh """
                        kubectl set image deployment/myapp myapp=${IMAGE_NAME}:${BUILD_NUMBER} || \
                        kubectl create deployment myapp --image=${IMAGE_NAME}:${BUILD_NUMBER}
                        
                        kubectl expose deployment myapp --port=5000 --type=NodePort || echo "Service already exists"
                        
                        kubectl get pods
                        kubectl get services
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh "docker system prune -f"
        }
        success {
            echo 'Pipeline completed successfully! 🎉'
        }
        failure {
            echo 'Pipeline failed! 😞'
        }
    }
}