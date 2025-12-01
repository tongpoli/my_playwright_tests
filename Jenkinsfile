pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}\\venv"
        PYTHON = "${VENV}\\Scripts\\python.exe"
        PIP = "${VENV}\\Scripts\\pip.exe"
        DEPLOY_DIR = "C:\\Users\\tongp\\my_playwright_tests_report"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/tongpoli/my_playwright_tests.git'
            }
        }

        stage('Setup Python') {
            steps {
                bat 'python -m venv venv'
                bat '"%PIP%" install --upgrade pip'
                bat '"%PIP%" install -r requirements.txt'
                bat '"%PYTHON%" -m playwright install'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"%PYTHON%" -m pytest tests --html=playwright-report.html --self-contained-html'
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'playwright-report.html',
                    reportName: 'Playwright Test Report'
                ])
            }
        }

        stage('Deploy Report (CD)') {
            steps {
                script {
                    // Generate timestamp for versioning: 2025-12-01_10-45-20
                    def timestamp = new Date().format("yyyy-MM-dd_HH-mm-ss")

                    // Full target path
                    env.TARGET_PATH = "${DEPLOY_DIR}\\${timestamp}"

                    echo "Deploying report to ${env.TARGET_PATH}"

                    // Create folder
                    bat """
                        powershell -NoProfile -Command "New-Item -ItemType Directory -Force -Path '${env.TARGET_PATH}'"
                    """

                    // Copy report file
                    bat """
                        powershell -NoProfile -Command "Copy-Item '${WORKSPACE}\\playwright-report.html' '${env.TARGET_PATH}\\playwright-report.html' -Force"
                    """
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/playwright-report.html', allowEmptyArchive: true
        }
        failure {
            echo 'Build failed! Check the test report for details.'
        }
    }
}
