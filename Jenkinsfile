pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                bat 'C:\\Users\\gorge\\AppData\\Local\\Programs\\Python\\Python314\\python.exe -m venv .venv'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }
        stage('Tests') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest .\\tests\\ -v'
            }
        }
        stage('Verify') {
            steps {
                bat '.venv\\Scripts\\python.exe -m src.verification'
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts: 'reports/*.csv'
        }
    }
}