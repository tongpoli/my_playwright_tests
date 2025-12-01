pipeline {
    agent any

    environment {
        // Virtual environment
        VENV        = "${WORKSPACE}\\venv"
        PYTHON      = "${VENV}\\Scripts\\python.exe"
        PIP         = "${VENV}\\Scripts\\pip.exe"

        // Deployment locations
        DEPLOY_BASE = "C:\\Users\\tongp\\my_playwright_tests_report"
        DEPLOY_BIN  = "${DEPLOY_BASE}\\deployment"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/tongpoli/my_playwright_tests.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat 'python -m venv venv'
                bat '"%PIP%" install --upgrade pip'
                bat '"%PIP%" install -r requirements.txt'
                bat '"%PYTHON%" -m playwright install --with-deps --force'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                bat """
                    "%PYTHON%" -m pytest tests ^
                      --html=playwright-report.html ^
                      --self-contained-html ^
                      --disable-warnings
                """
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '',
                    reportFiles: 'playwright-report.html',
                    reportName: 'Playwright Test Report'
                ])
            }
        }

        stage('Deploy Report & Artifacts') {
            steps {
                script {
                    def ts = new Date().format("yyyyMMdd_HHmmss")
                    env.DEPLOY_DIR = "${DEPLOY_BASE}\\Report_${ts}"

                    bat "mkdir \"${env.DEPLOY_DIR}\""
                    bat "copy /Y playwright-report.html \"${env.DEPLOY_DIR}\\\""

                    // Copy screenshots, trace, videos, etc. if they exist
                    bat 'if exist screenshots   xcopy screenshots   "%DEPLOY_DIR%\\screenshots"   /E /I /Y || exit 0'
                    bat 'if exist test-results  xcopy test-results  "%DEPLOY_DIR%\\test-results"  /E /I /Y || exit 0'
                    bat 'if exist trace         xcopy trace         "%DEPLOY_DIR%\\trace"         /E /I /Y || exit 0'
                    bat 'if exist videos        xcopy videos        "%DEPLOY_DIR%\\videos"        /E /I /Y || exit 0'

                    echo "Deployed to: ${env.DEPLOY_DIR}"
                }
            }
        }

        stage('Cleanup Old Deployments (keep latest 10)') {
            steps {
                bat """
                    powershell -Command ^
                      "$path = '%DEPLOY_BASE%'; ^
                       Get-ChildItem -Path $path -Directory ^
                         | Where-Object { $_.Name -match '^Report_\\d{8}_\\d{6}$' } ^
                         | Sort-Object CreationTime -Descending ^
                         | Select-Object -Skip 10 ^
                         | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"
                """
            }
        }

        stage('Build Standalone Executable') {
            steps {
                bat '"%PIP%" install --upgrade pyinstaller'
                bat """
                    rmdir /S /Q build 2>nul || ver >nul
                    del /Q *.spec 2>nul || ver >nul
                    rmdir /S /Q "%DEPLOY_BIN%" 2>nul || ver >nul
                    mkdir "%DEPLOY_BIN%"
                """
                bat """
                    "%PYTHON%" -m PyInstaller ^
                      --onefile ^
                      --name playwright_runner ^
                      --distpath "%DEPLOY_BIN%" ^
                      --clean ^
                      tests\\main.py
                """
                echo "Executable created at: %DEPLOY_BIN%\\playwright_runner.exe"
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'playwright-report.html', 
                            allowEmptyArchive: true
            archiveArtifacts artifacts: '${DEPLOY_BIN}/playwright_runner.exe', 
                            allowEmptyArchive: true
            // Optional: clean workspace to save disk space
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    notFailBuild: true)
        }
        success {
            echo 'Playwright tests passed and report + executable deployed successfully!'
        }
        failure {
            echo 'Pipeline failed — check the Playwright HTML report above for details.'
        }
    }
}