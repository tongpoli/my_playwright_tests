pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}\\venv"
        PYTHON = "${VENV}\\Scripts\\python.exe"
        PIP = "${VENV}\\Scripts\\pip.exe"

        // Deployment base folder
        DEPLOY_BASE = "C:\\Users\\tongp\\my_playwright_tests_report"

        // Final deployment folder for compiled files
        DEPLOY_BIN = "C:\\Users\\tongp\\my_playwright_tests_report\\deployment"
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
					// Timestamp
					def ts = new Date().format("yyyyMMdd_HHmmss")
					env.DEPLOY_DIR = "${DEPLOY_BASE}\\Report_${ts}"
		
					echo "Creating report folder: ${env.DEPLOY_DIR}"
					bat "mkdir \"${env.DEPLOY_DIR}\""
		
					// Copy HTML report, screenshots & logs if exist
					bat "copy /Y \"playwright-report.html\" \"${env.DEPLOY_DIR}\""
					bat "if exist screenshots xcopy screenshots \"${env.DEPLOY_DIR}\\screenshots\" /E /I /Y"
					bat "if exist logs xcopy logs \"${env.DEPLOY_DIR}\\logs\" /E /I /Y"
				}
			}
		}

		stage('Cleanup Old Reports (keep latest 10)') {
			steps {
				bat '''
		powershell -NoProfile -Command ^
		"$path = 'C:\\Users\\tongp\\my_playwright_tests_report'; ^
		$folders = Get-ChildItem -Path $path -Directory | Sort-Object LastWriteTime -Descending; ^
		if ($folders.Count -gt 10) { ^
			$folders | Select-Object -Skip 10 | Remove-Item -Recurse -Force; ^
		}"
		'''
			}
		}




        stage('Compile Python App (PyInstaller)') {
            steps {
                script {
                    bat "\"%PIP%\" install pyinstaller"

                    // Compile everything under tests/
                    bat "\"%PYTHON%\" -m PyInstaller --onefile tests/main.py --distpath dist"

                    // Create deployment folder
                    bat "mkdir \"${DEPLOY_BIN}\""

                    // Copy build results
                    bat "copy /Y dist\\main.exe \"${DEPLOY_BIN}\""
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
}
