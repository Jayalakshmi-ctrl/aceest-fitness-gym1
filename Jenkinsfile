pipeline {
    agent any

    environment {
        IMAGE_NAME = 'aceest-fitness-app'
        IMAGE_TAG  = 'v1.0.0'
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo 'Pulling code from GitHub Repository...'
                checkout scm
            }
        }

        stage('Environment Initialization') {
            steps {
                echo 'Creating Python isolated environment and installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Static Analysis & Linting') {
            steps {
                echo 'Running syntax check framework...'
                // Verifies files contain valid python syntax without executing them
                sh '''
                    . venv/bin/activate
                    python3 -m compileall app/ run.py
                '''
            }
        }

        stage('Execute Unit Tests') {
            steps {
                echo 'Running automated Pytest Validation Suite...'
                sh '''
                    . venv/bin/activate
                    pytest --verbose
                '''
            }
        }

        stage('Docker Image Assembly') {
            steps {
                echo 'Assembling the production Docker container...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }
    }

    post {
        success {
            echo "CI Workflow Completed Successfully. Quality Gate Passed!"
        }
        failure {
            echo "Pipeline Deployment Fault Detected. Checking logs..."
        }
    }
}
