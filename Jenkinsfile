pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 15, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
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
                bat '''
                    if not exist .venv (
                        python -m venv .venv
                    )

                    .venv\\Scripts\\python.exe -m pip install --upgrade pip
                    .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            parallel {

                stage('Application Tests') {
                    steps {
                        bat '''
                            if not exist reports mkdir reports
                            .venv\\Scripts\\python.exe -m pytest tests\\test_app.py --junitxml=reports\\application-tests.xml
                        '''
                    }
                }

                stage('Jenkins Integration Tests') {
                    steps {
                        bat '''
                            if not exist reports mkdir reports
                            .venv\\Scripts\\python.exe -m pytest tests\\test_jenkins_config.py --junitxml=reports\\jenkins-tests.xml
                        '''
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                bat '''
                    docker build ^
                        -t %IMAGE_NAME%:%BUILD_NUMBER% ^
                        -t %IMAGE_NAME%:latest ^
                        --label com.nexus.jenkins.build=%BUILD_NUMBER% ^
                        .
                '''
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                    docker rm -f %CONTAINER_NAME% 2>nul || exit /b 0

                    docker run -d ^
                        --name %CONTAINER_NAME% ^
                        -p %APP_PORT%:5000 ^
                        %IMAGE_NAME%:%BUILD_NUMBER%
                '''
            }
        }

        stage('Health Check') {
            steps {
                bat '''
                    echo Checking NEXUS application health...

                    for /L %%i in (1,1,20) do (
                        curl.exe -fsS http://127.0.0.1:5000/health >nul 2>&1

                        if not errorlevel 1 (
                            echo Health check PASSED.
                            exit /b 0
                        )

                        echo Waiting for application...
                        timeout /t 2 /nobreak >nul
                    )

                    echo Health check FAILED.
                    exit /b 1
                '''
            }
        }
    }

    post {
        always {
            junit testResults: 'reports\\*.xml', allowEmptyResults: true

            bat '''
                docker ps -a
            '''
        }

        success {
            echo 'NEXUS CI/CD pipeline completed successfully.'
        }

        failure {
            echo 'NEXUS CI/CD pipeline failed. Check the console log for the failing stage.'
        }
    }
}