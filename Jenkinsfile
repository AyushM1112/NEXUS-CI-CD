pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 10, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '15'))
    }

    environment {
        IMAGE_NAME = 'nexus-devops'
        CONTAINER_NAME = 'nexus-devops'
        APP_PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh '''
                    set -eux
                    python3 --version
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                    mkdir -p reports
                '''
            }
        }

        stage('Test') {
            parallel {
                stage('Application Tests') {
                    steps {
                        sh '''
                            .venv/bin/pytest -q tests/test_app.py --junitxml=reports/application-tests.xml
                        '''
                    }
                }
                stage('Jenkins Integration Tests') {
                    steps {
                        sh '''
                            .venv/bin/pytest -q tests/test_jenkins_config.py --junitxml=reports/jenkins-tests.xml
                        '''
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -eux
                    docker build                       --label "org.opencontainers.image.revision=${GIT_COMMIT}"                       --label "org.opencontainers.image.version=${BUILD_NUMBER}"                       -t "${IMAGE_NAME}:${BUILD_NUMBER}"                       -t "${IMAGE_NAME}:latest" .
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -eux
                    docker rm -f "${CONTAINER_NAME}" || true
                    docker run -d                       --name "${CONTAINER_NAME}"                       -p "${APP_PORT}:5000"                       --restart unless-stopped                       "${IMAGE_NAME}:${BUILD_NUMBER}"
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    set -eux
                    for i in $(seq 1 15); do
                      if curl -fsS "http://127.0.0.1:${APP_PORT}/health"; then
                        exit 0
                      fi
                      sleep 2
                    done
                    docker logs "${CONTAINER_NAME}" || true
                    exit 1
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/*.xml'
        }
        success {
            echo "NEXUS deployment completed successfully. Build #${BUILD_NUMBER}"
        }
        failure {
            echo "NEXUS pipeline failed. Use the real Jenkins console with ChatGPT for root-cause analysis."
        }
        cleanup {
            sh '''
                docker image prune -f || true
                rm -rf .venv || true
            '''
        }
    }
}
