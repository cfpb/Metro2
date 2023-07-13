from unittest import TestCase, mock 

from secret import SecretsManagerSecret, getClient, deleteSecret, get_secret, writeSecret

class TestSecret(TestCase):

    def setUp(self):
        self.service = 'secretsmanager'
        self.region = 'us-east-1'
        self.team = 'fake'
        self.label = 'mistake'
        self.secret = 'this is fake'
    
    def test_secrets_manager_secret_init(self):
        client = mock.MagicMock()
        secret = SecretsManagerSecret(client)
        self.assertEqual(secret.secretsmanager_client, client)
    
    def test_secrets_manager_secret_create_string(self):
        client = mock.MagicMock()
        secret = SecretsManagerSecret(client)

        name = "secret_name"
        value = "secret_value"

        secret.create(name, value)

        client.create_secret.assert_called_once_with(Name=name, SecretString=value)

    def test_secrets_manager_secret_create_binary(self):
        client = mock.MagicMock()
        secret = SecretsManagerSecret(client)

        name = "secret_name"
        value = b"secret_value"

        secret.create(name, value)

        client.create_secret.assert_called_once_with(Name=name, SecretBinary=value)

    @mock.patch('boto3.session.Session.client')
    def test_get_client(self, mock_client):
        getClient()
        mock_client.assert_called_once_with(service_name=self.service, region_name=self.region)

    @mock.patch('secret.getClient')
    @mock.patch('secret.SecretsManagerSecret.create')
    def test_write_secret(self, mock_mgr_create, mock_client):
        writeSecret(self.team, self.label, self.secret)
        mock_client.assert_called_once()
        mock_mgr_create.assert_called_once_with(f'cfpb/team/{self.team}/{self.label}', self.secret)
    
    #TODO FIX
    # @mock.patch('metro2.secret.getClient')
    # def test_delete_secret(self, mock_get_client):
    #     mock_client = mock.MagicMock()
    #     mock_client.deleteSecret.return_value = None
    #     mock_get_client = mock_client
    #     deleteSecret(self.team, self.label)
    #     mock_get_client.assert_called_once()

    @mock.patch('secret.getClient')
    def test_get_secret_string(self, mock_get_client):
        mock_secret_value = {'SecretString': 'fake'}
        mock_client = mock.MagicMock()
        mock_client.get_secret_value.return_value = mock_secret_value
        mock_get_client.return_value = mock_client

        result = get_secret(self.team, self.label)
        self.assertEqual(result, 'fake')

    @mock.patch('secret.getClient')
    def test_get_secret_binary(self, mock_get_client):
        mock_secret_value = {'SecretBinary': b'fake'}
        mock_client = mock.MagicMock()
        mock_client.get_secret_value.return_value = mock_secret_value
        mock_get_client.return_value = mock_client

        result = get_secret(self.team, self.label)
        self.assertEqual(result, b'fake')