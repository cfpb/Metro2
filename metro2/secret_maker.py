import argparse
import boto3
import botocore.session


from botocore.exceptions import ClientError

parser = argparse.ArgumentParser()
parser.add_argument('--label')
parser.add_argument('--team')
parser.add_argument('--host')
parser.add_argument('--password')
parser.add_argument('--port')
parser.add_argument('--engine')
parser.add_argument('--database')
parser.add_argument('--user')

args = parser.parse_args()

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

def main(team, label, host, port, database, engine, password, user) -> None: 
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1',
    )

    mgr = SecretsManagerSecret(client)

    secret_string = f'''"HOST": "{host}","PORT": "{port}","DB": "{database}","ENGINE": "{engine}","PASSWORD": "{password}","USER": "{user}"'''

    secret_string_json = "{" + secret_string + "}"

    mgr.create(f'cfpb/team/{team}/{label}', secret_string_json) 


main(args.team, args.label, args.host, args.port, args.database, args.engine, args.password, args.user)