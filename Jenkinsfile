pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Checkout from main branch
                git branch: 'main', url: 'https://github.com/rinkugupta3/Automation_Accessibility'
            }
        }
        stage('Set up Python environment') {
            steps {
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install --upgrade pip"
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install -r requirements.txt"
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install pytest-html"
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install axe-selenium-python" // Install axe-selenium-python
            }
        }
        stage('Install Lighthouse') {
            steps {
                bat "npm install -g lighthouse" // Install Lighthouse globally
            }
        }
        stage('Install Playwright Browsers') {
            steps {
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m playwright install"
            }
        }
        stage('Run Accessibility Tests') {
            steps {
                // Run headless tests for accessibility
                bat '''
                    set HEADLESS=true
                    C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pytest tests_axecore_lighthouse/ --html=accessibility_report.html --maxfail=3 --disable-warnings -v
                '''
            }
        }
        stage('Run Lighthouse Tests') {
            steps {
                // Run headless tests for Lighthouse
                bat '''
                    set HEADLESS=true
                    C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pytest tests_axecore_lighthouse/ --html=lighthouse_report.html --maxfail=3 --disable-warnings -v
                '''
            }
        }
        stage('Run Login Home Webpage Tests') {
            steps {
                bat '''
                    set HEADLESS=true
                    C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pytest tests_login_home_webpage/ --html=report_login_home_webpage.html --maxfail=3 --disable-warnings -v
                '''
            }
        }
        stage('Run Login Webpage Tests') {
            steps {
                bat '''
                    set HEADLESS=true
                    C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pytest tests_login_webpage/ --html=report_login_webpage.html --maxfail=3 --disable-warnings -v
                '''
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
            archiveArtifacts artifacts: '**/*.html', allowEmptyArchive: true
            archiveArtifacts artifacts: 'screenshots/**/*', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}