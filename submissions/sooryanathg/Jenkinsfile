pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USERNAME = 'sooryanath'
        IMAGE_NAME = 'flask-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '========== Checking out code =========='
                checkout scm
                sh 'ls -la'
                sh 'pwd'
            }
        }
        
        stage('Build') {
            steps {
                echo '========== Building Docker image =========='
                script {
                    sh """
                        docker build -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                        docker images | grep ${IMAGE_NAME}
                    """
                }
            }
        }
        
        stage('Test') {
            steps {
                echo '========== Running tests =========='
                script {
                    sh """
                        docker run --rm ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} pytest test_app.py -v
                    """
                }
            }
        }
        
        stage('Push') {
            steps {
                echo '========== Pushing to DockerHub =========='
                script {
                    sh """
                        echo \$DOCKERHUB_CREDENTIALS_PSW | docker login -u \$DOCKERHUB_CREDENTIALS_USR --password-stdin
                        docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                        echo "Image pushed successfully!"
                    """
                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo '========== Deploying container locally =========='
                script {
                    sh """
                        # Stop and remove existing container if running
                        docker stop flask-app-container 2>/dev/null || true
                        docker rm flask-app-container 2>/dev/null || true
                        
                        # Run new container
                        docker run -d \
                            --name flask-app-container \
                            -p 5000:5000 \
                            ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                        
                        # Wait for container to start
                        sleep 5
                        
                        # Verify container is running
                        docker ps | grep flask-app-container
                        
                        # Test the application
                        curl -f http://localhost:5000 || exit 1
                        
                        echo "Container deployed successfully!"
                        echo "Access the app at: http://localhost:5000"
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo '========== Cleaning up =========='
            sh 'docker logout || true'
        }
        success {
            echo '========================================='
            echo '✅ Pipeline completed successfully!'
            echo '========================================='
            echo 'Docker Image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest'
            echo 'Application URL: http://localhost:5000'
            echo '========================================='
        }
        failure {
            echo '========================================='
            echo '❌ Pipeline failed! Check the logs above.'
            echo '========================================='
        }
    }
}
