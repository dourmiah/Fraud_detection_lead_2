pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "fraud-detection-model"
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/dourmiah/Fraud_detection_lead_2.git'
                
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('fraud-detection-model')
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image('fraud-detection-model').inside {
                        sh 'pytest tests/tests.py --junitxml=results.xml'
                    }
                }
            }
        }
       stage('Run Container') {
            steps {
                script {
                    sh 'docker run --rm -v "$(pwd):/home/app" fraud-detection-model'
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully !'
            // Send email notification
        }
        failure {
            echo 'Pipeline failed.'
            // Send email notification
        }
    }
}