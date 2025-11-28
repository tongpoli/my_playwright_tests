pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}\\venv"
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
				bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'
				bat 'venv\\Scripts\\python.exe -m pip install -r requirements.txt'
				bat 'venv\\Scripts\\python.exe -m playwright install'
            }
        }

        stage('Run Tests') {
            steps {
                bat "${VENV}\\Scripts\\pytest tests\\ --html=playwright-report.html --self-contained-html"
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
