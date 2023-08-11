import argparse
import boto3
import botocore.session
import logging


from botocore.exceptions import ClientError

class SecretsManagerSecret:
    """Encapsulates Secrets Manager functions."""
    def __init__(self, secretsmanager_client):
        """
        :param secretsmanager_client: A Boto3 Secrets Manager client.
        """
        self.secretsmanager_client = secretsmanager_client
        self.name = None

    def create(self, name, secret_value):
        """
        Creates a new secret. The secret value can be a string or bytes.
        :param name: The name of the secret to create.
        :param secret_value: The value of the secret.
        :return: Metadata about the newly created secret.
        """
        try:
            kwargs = {'Name': name}
            if isinstance(secret_value, str):
                kwargs['SecretString'] = secret_value
            elif isinstance(secret_value, bytes):
                kwargs['SecretBinary'] = secret_value
            response = self.secretsmanager_client.create_secret(**kwargs)
            self.name = name
        except ClientError:
            raise
        else:
            return response

def getClient():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1',
    )
    return client

def writeSecret(team, label, secret_string) -> None: 
    client = getClient()
    mgr = SecretsManagerSecret(client)

    try:
        return mgr.create(f'cfpb/team/{team}/{label}', secret_string)
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceExistsException':
            logging.error('The desired secret ' + f'cfpb/team/{team}/{label}' + ' already exists.')
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            logging.error('The request was invalid due to:', e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            logging.error('The request had invalid params:', e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            logging.error('An error occurred on service side:', e)
        elif e.response['Error']['Code'] == 'ExpiredTokenException': 
            logging.error('Your AWS session is expired.  Re-run gimme-aws-creds.')

def deleteSecret(team, label) -> None:
    client = getClient()
    
    try:
        client.delete_secret(
            SecretId=f'cfpb/team/{team}/{label}'
        )
        logging.info(f'cfpb/team/{team}/{label} successfully deleted')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            logging.error('The requested secret ' + f'cfpb/team/{team}/{label}' + ' was not found')
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            logging.error('The request was invalid due to:', e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            logging.error('The request had invalid params:', e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            logging.error('The requested secret can\'t be decrypted using the provided KMS key:', e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            logging.error('An error occurred on service side:', e)
        elif e.response['Error']['Code'] == 'ExpiredTokenException': 
            logging.error('Your AWS session is expired.  Re-run gimme-aws-creds.')

def get_secret(team, label) -> str:
    client = getClient()
    secret_name=f'cfpb/team/{team}/{label}'

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            logging.error('The requested secret ' + secret_name + ' was not found')
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            logging.error('The request was invalid due to:', e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            logging.error('The request had invalid params:', e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            logging.error('The requested secret can\'t be decrypted using the provided KMS key:', e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            logging.error('An error occurred on service side:', e)
        elif e.response['Error']['Code'] == 'ExpiredTokenException': 
            logging.error('Your AWS session is expired.  Re-run gimme-aws-creds.')
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
            return binary_secret_data