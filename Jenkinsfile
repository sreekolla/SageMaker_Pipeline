pipeline {
    agent any

    

    environment {
        AWS_REGION     = 'us-east-1'
        SAGEMAKER_ROLE = 'arn:aws:iam::084719916966:role/service-role/AmazonSageMaker-ExecutionRole'
        CONDA_ENV      = 'mlops_env'
        CONDA_PATH     = 'C:\\Users\\Laptop\\anaconda3\\Scripts\\activate.bat'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Debug Workspace') {
            steps {
                bat """
                echo Current workspace: %WORKSPACE%
                dir "%WORKSPACE%" /s
                """
            }
        }

        stage('Setup AWS Credentials') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: '22c560e3-0493-434e-a60a-106a4bbb2c84',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    bat """
                    if not exist %USERPROFILE%\\.aws mkdir %USERPROFILE%\\.aws
                    echo [default] > %USERPROFILE%\\.aws\\credentials
                    echo aws_access_key_id=%AWS_ACCESS_KEY_ID% >> %USERPROFILE%\\.aws\\credentials
                    echo aws_secret_access_key=%AWS_SECRET_ACCESS_KEY% >> %USERPROFILE%\\.aws\\credentials
                    echo region=%AWS_REGION% >> %USERPROFILE%\\.aws\\credentials
                    """
                }
            }
        }

        stage('Setup Conda Environment') {
            steps {
                bat """
                REM Create conda environment if it doesn't exist
                conda info --envs | findstr %CONDA_ENV%
                IF %ERRORLEVEL% NEQ 0 (
                    conda create -n %CONDA_ENV% python=3.11 -y
                )

                REM Activate conda environment
                call %CONDA_PATH% %CONDA_ENV%

                REM Upgrade pip and NumPy
                pip install --upgrade pip
                pip install --no-cache-dir --force-reinstall numpy

                REM Install other dependencies
                pip install -r requirements.txt
                pip install sagemaker boto3
                """
            }
        }

        stage('Run SageMaker Training') {
            steps {
                bat """
                REM Activate conda environment
                call %CONDA_PATH% %CONDA_ENV%
                set SAGEMAKER_ROLE=%SAGEMAKER_ROLE%

                REM Run SageMaker script with warnings suppressed
                python -c "import os, warnings, numpy as np; \
os.environ['NUMPY_EXPERIMENTAL']='0'; \
warnings.filterwarnings('ignore', category=RuntimeWarning); \
np.float128 = float; import sagemaker_pipeline"
                """
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
