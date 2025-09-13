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
                withCredentials([usernamePassword(credentialsId: 'aws_cred', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
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
                REM Remove existing virtualenv if present
                if exist venv rmdir /s /q venv

                REM Create fresh virtualenv
                python -m venv venv
                call venv\\Scripts\\activate

                REM Upgrade pip and numpy to latest 64-bit version
                pip install --upgrade pip
                pip install --no-cache-dir --force-reinstall numpy

                REM Install remaining dependencies
                pip install -r requirements.txt
                pip install sagemaker boto3
                '''
            }
        }
        stage('Debug Workspace') {
          steps {
              bat """
              echo Current workspace: %WORKSPACE%
              """
            }
        }


        stage('Run SageMaker Training') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                set SAGEMAKER_ROLE=%SAGEMAKER_ROLE%
                REM Run SageMaker script with NumPy warnings suppressed
                python -c "import warnings; warnings.filterwarnings('ignore', category=RuntimeWarning); import sage_Maker"
                '''
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