import boto3
from django.conf import settings
from django_application.file_utils import get_file_contents


def s3_resource():
    """
    Return a resource for use in uploading or downloading files to/from S3.

    In deployed environments (in EKS), use the credentials from the secrets file
    to create the S3 resource directly.

    When running locally, allow boto3 to infer the credentials from your environment.
    Do this by running `aws configure sso`, then using `export AWS_PROFILE=[your profile]`
    """
    if settings.AWS_CREDS_LOCATION:
        access_key_id = get_file_contents(settings.AWS_CREDS_LOCATION[0])
        secret_key = get_file_contents(settings.AWS_CREDS_LOCATION[1])
        return boto3.resource(
            service_name="s3",
            region_name="us-east-1",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key,
        )
    else:
        return boto3.resource("s3")

def s3_session():
    """
    Return a session for use in uploading files to S3.

    Use the credentials from the secrets files to create the S3 session directly.

    When running locally, you will need to provide an access key and secret key manually.
    You can use sample settings in settings/docker-compose.py.
    """
    if settings.AWS_CREDS_LOCATION:
        access_key_id = get_file_contents(settings.AWS_CREDS_LOCATION[0])
        secret_key = get_file_contents(settings.AWS_CREDS_LOCATION[1])
        return boto3.Session(
            region_name="us-east-1",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key).client('s3')
    else:
        return boto3.Session("s3")