pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "fraud-detection-model"
        ENV_FILE = 'secrets.env'
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
                    docker.image(DOCKER_IMAGE).inside("-e APP_URI=${env.APP_URI}") { 
                        sh """
                            export \$(cat ${ENV_FILE} | xargs)
                            pytest --junitxml=results.xml
                        """
                    }
                }
            }
        }
        stage('Run Container') {
            steps {
                script {
                    sh """
                        docker run --rm --env-file=${ENV_FILE} -v "\$(pwd):/home/app" ${DOCKER_IMAGE} sh -c "ls -R /home/app"
                    """
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