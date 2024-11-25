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
                    withCredentials([string(credentialsId: "APP_URI", variable: "APP_URI")]) {
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
            // emailext (
            //     subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            //     body: "Good news! Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' succeeded.",
            //     to: "jedhaprojetfrauddetect@gmail.com"
            // )
            mail bcc: '', body: "<b>Example</b><br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL de build: ${env.BUILD_URL}", cc: 'dourmiah@gmail.com', charset: 'UTF-8', from: '', mimeType: 'text/html', replyTo: '', subject: "SUCCESS CI: Project name -> ${env.JOB_NAME}", to: "jedhaprojetfrauddetect@gmail.com";
        }
        failure {
            // emailext (
            //     subject: "FAILURE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            //     body: "Unfortunately, Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' failed.\nCheck the logs at: ${env.BUILD_URL}",
            //     to: "jedhaprojetfrauddetect@gmail.com"
            // )
            mail bcc: '', body: "<b>Example</b><br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL de build: ${env.BUILD_URL}", cc: 'dourmiah@gmail.com', charset: 'UTF-8', from: '', mimeType: 'text/html', replyTo: '', subject: "ERROR CI: Project name -> ${env.JOB_NAME}", to: "jedhaprojetfrauddetect@gmail.com";
        }
    }
}