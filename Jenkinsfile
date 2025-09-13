pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        SAGEMAKER_ROLE = 'arn:aws:iam::084719916966:role/service-role/AmazonSageMaker-ExecutionRole'
        
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup AWS Credentials') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'kolla_credentails', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    bat '''
                    if not exist %USERPROFILE%\\.aws mkdir %USERPROFILE%\\.aws
                    echo [default] > %USERPROFILE%\\.aws\\credentials
                    echo aws_access_key_id=%AWS_ACCESS_KEY_ID% >> %USERPROFILE%\\.aws\\credentials
                    echo aws_secret_access_key=%AWS_SECRET_ACCESS_KEY% >> %USERPROFILE%\\.aws\\credentials
                    echo region=%AWS_REGION% >> %USERPROFILE%\\.aws\\credentials
                    '''
                }
            }
        }

        stage('Setup Python') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install sagemaker boto3
                '''
            }
        }

        stage('Run SageMaker Training') {
            steps {
                withCredentials([string(credentialsId: 'sagemaker-role', variable: 'SAGEMAKER_ROLE')]) {
                    bat '''
                    call venv\\Scripts\\activate
                    set SAGEMAKER_ROLE=%SAGEMAKER_ROLE%
                    set TRAIN_S3_URI=%TRAIN_S3_URI%
                    python sagemaker_pipeline.py
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Training pipeline executed successfully!"
        }
        failure {
            echo "❌ Training pipeline failed. Check logs."
        }
    }
}

