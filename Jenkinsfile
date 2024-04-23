pipeline {
    agent any
    stages {
        stage('CleanUp') {
            steps {
                sh '''echo "Removing Docker services"
                docker compose down || true
                '''
            }
        }
        stage('Removing Images') {
            steps {
                sh '''echo "Removing images"    
                docker image rm -f test-result-flask-app:latest || true
                docker image rm -f test-result-mysql-db:latest || true
                docker image rm -f test-result-nginx:latest || true
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''echo "Deploying services"
                docker compose up -d
                '''
            }
        }
    }
}