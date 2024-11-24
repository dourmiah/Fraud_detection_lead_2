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
        stage('Debug') {
            steps {
                script {
                    docker.image('fraud-detection-model').inside {
                        sh 'ls -R /home/app'
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image('fraud-detection-model').inside {
                        sh 'pytest /home/app/Model/tests/tests.py --junitxml=results.xml'
                    }
                }
            }
        }
        stage('Run Container') {
            steps {
                script {
                    sh 'docker run --rm -v "$(pwd):/home/app" fraud-detection-model sh -c "ls -R /home/app"'
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully !'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}