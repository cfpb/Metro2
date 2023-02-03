import botocore
import boto3
import json
import botocore.session
from botocore.exceptions import ClientError 

def get_secret():
    secret_name = "cfpb/team/appops/rds/mysql/appops-brenden-tester-rds3/master-user-credentials"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
        elif e.response['Error']['Code'] == 'ExpiredTokenException': 
            print("Your AWS session is expired.  Re-run gimme-aws-creds.")
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            MY_DB_SECRETS = json.loads(get_secret_value_response['SecretString'])
            print(MY_DB_SECRETS)
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']

get_secret()