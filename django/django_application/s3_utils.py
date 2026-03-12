import boto3
from django.conf import settings


def s3_bucket_files(bucket_directory: str):
    bucket_name = settings.S3_BUCKET_NAME
    bucket = s3_resource().Bucket(bucket_name)
    return bucket.objects.filter(Prefix=bucket_directory)

def s3_resource():
    """
    Return a resource for use in uploading or downloading files to/from S3.

    Use the credentials from the settings to create the S3 resource directly.
    Or, see Boto3 documentation for alternative ways to handle credentials:
    https://docs.aws.amazon.com/boto3/latest/guide/credentials.html
    """
    if settings.SVC_ACCESS_KEY and settings.SVC_SECRET_KEY:
        return boto3.resource(
            service_name="s3",
            region_name="us-east-1",
            aws_access_key_id=settings.SVC_ACCESS_KEY,
            aws_secret_access_key=settings.SVC_SECRET_KEY,
        )
    else:
        return boto3.resource("s3")

def s3_session():
    """
    Return a session for use in uploading files to S3.

    Use the credentials from the settings to create the S3 session directly.
    Or, see Boto3 documentation for alternative ways to handle credentials:
    https://docs.aws.amazon.com/boto3/latest/guide/credentials.html
    """
    if settings.SVC_ACCESS_KEY and settings.SVC_SECRET_KEY:
        return boto3.Session(
            region_name="us-east-1",
            aws_access_key_id=settings.SVC_ACCESS_KEY,
            aws_secret_access_key=settings.SVC_SECRET_KEY,
        ).client('s3')
    else:
        return boto3.Session("s3")
