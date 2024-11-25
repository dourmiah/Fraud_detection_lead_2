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
                    docker.build(DOCKER_IMAGE)
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    withCredentials([string(credentialsId: "APP_URI", variable: "APP_URI")]) {
                        docker.image(DOCKER_IMAGE).inside {
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
                    withCredentials([string(credentialsId: "APP_URI", variable: "APP_URI")]) {
                        docker.image(DOCKER_IMAGE).inside {
                            sh """
                                echo "Running the container with APP_URI=$APP_URI"
                                env | grep APP_URI
                            """
                        }
                    }
                }
            }
        }
    }
    post {
        success {
            mail bcc: '', 
            body: "<b>Infos</b><br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL de build: ${env.BUILD_URL}", 
            cc: 'dourmiah@gmail.com', 
            charset: 'UTF-8', 
            from: '', 
            mimeType: 'text/html', 
            replyTo: '', 
            subject: "SUCCESS CI: Project name -> ${env.JOB_NAME}", 
            to: "jedhaprojetfrauddetect@gmail.com";
        }
        failure {
            mail bcc: '', 
            body: "<b>Infos</b><br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL de build: ${env.BUILD_URL}", 
            cc: 'dourmiah@gmail.com', 
            charset: 'UTF-8', 
            from: '', 
            mimeType: 'text/html', 
            replyTo: '', 
            subject: "ERROR CI: Project name -> ${env.JOB_NAME}", 
            to: "jedhaprojetfrauddetect@gmail.com";
        }
    }
}