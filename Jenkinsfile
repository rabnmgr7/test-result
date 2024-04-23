pipeline {
    agent any
    stages {
        stage('CleanUp') {
            steps {
                sh '''echo "Removing Docker services"
                docker compose down || true
                echo "Removing Docker images"
                docker image rm -f rabnmgr7/test-result-flask-app:latest
                docker image rm -f rabnmgr7/test-result-mysql-db:latest
                docker image rm -f rabnmgr7/test-result-nginx:latest
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
                sh '''echo "Tagging and Pushing Images..."
                docker tag rabnmgr7/test-result-flask-app:latest rabnmgr7/test-result-flask-app:$BUILD_NUMBER || true
                docker tag rabnmgr7/test-result-mysql-db:latest rabnmgr7/test-result-mysql-db:$BUILD_NUMBER || true
                docker tag rabnmgr7/test-result-nginx:latest rabnmgr7/test-result-nginx:$BUILD_NUMBER || true
                docker push rabnmgr7/test-result-nginx:$BUILD_NUMBER
                docker push rabnmgr7/test-result-nginx:latest
                docker push rabnmgr7/test-result-flask-app:latest
                docker push rabnmgr7/test-result-flask-app:$BUILD_NUMBER
                docker push rabnmgr7/test-result-mysql-db:latest
                docker push rabnmgr7/test-result-mysql-db:$BUILD_NUMBER
                '''
            }
        }
        stage('CleanupWorkspace') {
            steps {
                sh '''echo "Removing Tagged Images. This is for storage cleanup."    
                docker image rm -f rabnmgr7/test-result-flask-app:$BUILD_NUMBER || true
                docker image rm -f rabnmgr7/test-result-mysql-db:$BUILD_NUMBER || true
                docker image rm -f rabnmgr7/test-result-nginx:$BUILD_NUMBER || true
                '''
            }
        }
    }
}