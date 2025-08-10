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
        
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                bat "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                bat "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                bat "docker run -d --name test-app-${BUILD_NUMBER} -p 5001:5000 ${IMAGE_NAME}:${BUILD_NUMBER}"
                powershell 'Start-Sleep -Seconds 10'
                
                // Run the Python test
                bat 'python test_simple.py'
                
                // Cleanup test container
                bat "docker stop test-app-${BUILD_NUMBER}"
                bat "docker rm test-app-${BUILD_NUMBER}"
            }
        }
        
        stage('Push') {
            steps {
                echo 'Pushing to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    bat "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                    bat "docker push ${IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying with Helm...'
                bat "helm upgrade --install myapp ./myapp --set image.tag=${BUILD_NUMBER}"
                bat 'kubectl get pods'
                bat 'kubectl get services'
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            bat "docker rm -f test-app-${BUILD_NUMBER} || echo No containers to clean"
        }
    }
}