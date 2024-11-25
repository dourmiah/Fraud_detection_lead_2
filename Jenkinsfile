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
            script {
                echo "Success"
                emailext(
                    subject: "Jenkins Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """<p>Good news!</p>
                             <p>The build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> was successful.</p>
                             <p>View the details <a href="${env.BUILD_URL}">here</a>.</p>""",
                    to: 'antoine@jedha.co'
                )
            }
        }
        failure {
            script {
                echo "Failure"
                emailext(
                    subject: "Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """<p>Unfortunately, the build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> has failed.</p>
                             <p>Please check the logs and address the issues.</p>
                             <p>View the details <a href="${env.BUILD_URL}">here</a>.</p>""",
                    to: 'antoine@jedha.co'
                )
            }
        }
    }
}