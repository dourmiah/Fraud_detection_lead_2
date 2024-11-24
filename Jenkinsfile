pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "fraud-detection-model" // Nom de l'image Docker
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
                    docker.build(DOCKER_IMAGE)
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'APP_URI', variable: 'APP_URI')]) {
                        docker.image(DOCKER_IMAGE).inside {
                            // Les variables sont injectées temporairement ici
                            sh """
                                echo "Testing APP_URI: $APP_URI"
                                pytest --junitxml=results.xml
                            """
                        }
                    }
                }
            }
        }
        stage('Run Container') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'APP_URI', variable: 'APP_URI')]) {
                        docker.image(DOCKER_IMAGE).inside {
                            sh """
                                echo "Running the container with APP_URI=$APP_URI"
                                env | grep APP_URI
                                ls -R /home/app
                            """
                        }
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}