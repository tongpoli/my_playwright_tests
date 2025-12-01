pipeline {
agent any

```
environment {
    VENV = "${WORKSPACE}\\venv"
    PYTHON = "${VENV}\\Scripts\\python.exe"
    PIP = "${VENV}\\Scripts\\pip.exe"

    // Deployment base folder
    DEPLOY_BASE = "C:\\Users\\tongp\\my_playwright_tests_report"
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
            bat '"%PYTHON%" -m pytest tests --html=playwright-report.html --self-contained-html --disable-warnings'
        }
    }

    stage('Publish Report to Jenkins') {
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

    /* ---------------------------
       🔽 CONTINUOUS DEPLOYMENT (CD)
       --------------------------- */

    stage('Deploy Report + Artifacts') {
        steps {
            script {
                def ts = new Date().format("yyyyMMdd_HHmmss")
                env.DEPLOY_REPORT_DIR = "${DEPLOY_BASE}\\Report_${ts}"

                echo "Creating report folder: ${env.DEPLOY_REPORT_DIR}"
                bat "if not exist \"${env.DEPLOY_REPORT_DIR}\" mkdir \"${env.DEPLOY_REPORT_DIR}\""

                bat "copy /Y \"playwright-report.html\" \"${env.DEPLOY_REPORT_DIR}\""
                bat "if exist screenshots xcopy screenshots \"${env.DEPLOY_REPORT_DIR}\\screenshots\" /E /I /Y"
                bat "if exist logs xcopy logs \"${env.DEPLOY_REPORT_DIR}\\logs\" /E /I /Y"
            }
        }
    }

    stage('Cleanup Old Reports (keep latest 10)') {
        steps {
            bat 'powershell -NoProfile -Command "$path=\'C:\\Users\\tongp\\my_playwright_tests_report\'; $folders=Get-ChildItem -Path $path -Directory | Sort-Object LastWriteTime -Descending; if($folders.Count -gt 10) { $folders | Select-Object -Skip 10 | Remove-Item -Recurse -Force }"'
        }
    }

    stage('Compile Python App (PyInstaller)') {
        steps {
            script {
                bat "\"%PIP%\" install pyinstaller"

                if (fileExists('tests/main.py')) {
                    // Timestamped deployment folder for .exe
                    def ts = new Date().format("yyyyMMdd_HHmmss")
                    env.DEPLOY_EXE_DIR = "${DEPLOY_BASE}\\Deployment_${ts}"
                    echo "Creating deployment folder: ${env.DEPLOY_EXE_DIR}"
                    bat "if not exist \"${env.DEPLOY_EXE_DIR}\" mkdir \"${env.DEPLOY_EXE_DIR}\""

                    // Compile main.py
                    bat "\"%PYTHON%\" -m PyInstaller --onefile tests/main.py --distpath dist"

                    // Copy build results safely
                    bat "if exist dist\\main.exe copy /Y dist\\main.exe \"${env.DEPLOY_EXE_DIR}\""
                } else {
                    echo "Skipping PyInstaller: tests/main.py not found"
                }
            }
        }
    }

} // end stages

post {
    always {
        archiveArtifacts artifacts: '**/playwright-report.html', allowEmptyArchive: true
    }
    failure {
        echo 'Build failed! Check the test report for details.'
    }
}
```

}
