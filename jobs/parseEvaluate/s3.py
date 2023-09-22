import boto3
from botocore.exceptions import ClientError
from envvar import fetch_env_var


# This code assumes that the AWS credentials are available in the environment.
# In addition to the env vars explicitly used in the code, it automatically 
# finds and uses the following values to connect to S3:
# AWS_DEFAULT_REGION
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_SESSION_TOKEN
# For more on how to set credentials:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html


def s3_resource():
    return boto3.resource('s3')

def getBucket():
    bucket_name = fetch_env_var('S3_BUCKET_NAME')
    resource = s3_resource()
    bucket = resource.Bucket(name=bucket_name)
    return bucket


def list_objects(bucket, prefix=None):
    if prefix:
        objects = bucket.objects.filter(Prefix=prefix)
    else:
        objects = bucket.objects.all()
    return objects

def open_file(file_object):
    """
    Gets the object (file) data in bytes.
    """
    try:
        body = file_object.get()['Body'].read()
        print(body)
    except ClientError:
        raise
    else:
        return body