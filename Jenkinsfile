pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        SAGEMAKER_ROLE = 'arn:aws:iam::084719916966:role/service-role/AmazonSageMaker-ExecutionRole'
        
    }
    stages {
        stage('Setup AWS Credentials') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'kolla_credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                    aws configure set default.region $AWS_REGION
                    '''
                }
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install sagemaker boto3
                '''
            }
        }

        stage('Run SageMaker Training') {
            steps {
                sh '''
                source venv/bin/activate
                python sagemaker_pipeline.py
                '''
            }
        }
    }

    post {
        success {
            echo "Training pipeline executed successfully!"
        }
        failure {
            echo "Training pipeline failed. Check logs."
        }
    }
}
