import sagemaker
from sagemaker.sklearn.estimator import SKLearn
import os

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()
role = "arn:aws:iam::084719916966:role/service-role/AmazonSageMaker-ExecutionRole"  # replace with your role ARN

# Define estimator
sklearn_estimator = SKLearn(
    entry_point="train.py",
    role=role,
    instance_type="ml.m5.large",
    framework_version="1.2-1",
    py_version="py3",
    base_job_name="simple-sklearn-job",
    sagemaker_session=sagemaker_session,
)

# Input data (can be empty or S3 path)
train_s3_uri = os.getenv("TRAIN_S3_URI", None)
inputs = {"train": train_s3_uri} if train_s3_uri else None

# Launch training job
sklearn_estimator.fit(inputs)
print("SageMaker training job launched successfully!")

