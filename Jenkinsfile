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
        stage('RegistryPush') {
            steps {
                sh '''echo "Tagging and Pushing Images"
                docker tag test-result-flask-app:latest test-result-flask-app:$BUILD_NUMBER || true
                docker tag test-result-mysql-db:latest test-result-mysql-db:$BUILD_NUMBER || true
                docker tag test-result-nginx:latest test-result-nginx:$BUILD_NUMBER || true
                docker push test-result-nginx:$BUILD_NUMBER
                docker push test-result-nginx:latest
                docker push test-result-flask-app:latest
                docker push test-result-flask-app:$BUILD_NUMBER
                docker push test-result-mysql-db:latest
                docker push test-result-mysql-db:$BUILD_NUMBER
                '''
            }
        }
    }
}