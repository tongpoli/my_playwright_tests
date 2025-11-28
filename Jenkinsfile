pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}\\venv"
        PYTHON = "${VENV}\\Scripts\\python.exe"
        PIP = "${VENV}\\Scripts\\pip.exe"
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
