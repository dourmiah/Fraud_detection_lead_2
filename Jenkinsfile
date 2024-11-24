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
                    docker.image(DOCKER_IMAGE).inside {
                        // Les variables d'environnement sont automatiquement injectées
                        sh """
                            pytest --junitxml=results.xml
                        """
                    }
                }
            }
        }
        stage('Run Container') {
            steps {
                script {
                    docker.image(DOCKER_IMAGE).inside {
                        sh """
                            echo "Running the container with injected environment variables"
                            env | grep APP_URI // Vérifie si les variables sont bien injectées
                            ls -R /home/app
                        """
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