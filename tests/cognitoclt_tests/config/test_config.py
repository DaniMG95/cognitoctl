from unittest import TestCase
from unittest.mock import patch, Mock
from cognitoctl.config import Config
from cognitoctl.exceptions import ExceptionCLIValidateConfig


class TestConfig(TestCase):

    @classmethod
    def setUpClass(cls):
        # Configura el diccionario común aquí si es necesario
        cls.data_config = {
            'current': {
                'project': 'projectx'
            },
            'projectx': {
                'key_id': 'testx',
                'access_key': 'testx_2',
                'userpool_id': 'user_testx',
                'app_client_id': 'client_id_testx',
                'app_client_secret': 'client_secret_testx',
                'secret_hash': True
            },
            'projecty': {
                'key_id': 'testy',
                'access_key': 'testy_2',
                'userpool_id': 'user_testy',
                'app_client_id': 'client_id_testy',
                'app_client_secret': 'client_secret_testy',
                'secret_hash': True
            }
        }

    @patch('cognitoctl.config.config.Config.get_config')
    @patch.dict('os.environ', {}, clear=True)
    def test_create_config_without_name(self, mock_get_config: Mock):
        mock_get_config.side_effect = [self.data_config]

        config = Config()
        self.assertTrue(config.secret_hash)
        self.assertEqual('user_testx', config.userpool_id)
        self.assertEqual('client_id_testx', config.app_client_id)
        self.assertEqual('client_secret_testx', config.app_client_secret)
        self.assertEqual('testx', config.key_id)
        self.assertEqual('testx_2', config.access_key)

    @patch('cognitoctl.config.config.Config.get_config')
    @patch.dict('os.environ', {}, clear=True)
    def test_create_config_with_name(self, mock_get_config: Mock):
        mock_get_config.side_effect = [self.data_config]

        config = Config(name='projecty')
        self.assertTrue(config.secret_hash)
        self.assertEqual('user_testy', config.userpool_id)
        self.assertEqual('client_id_testy', config.app_client_id)
        self.assertEqual('client_secret_testy', config.app_client_secret)
        self.assertEqual('testy', config.key_id)
        self.assertEqual('testy_2', config.access_key)

    @patch('cognitoctl.config.config.Config.get_config')
    @patch.dict('os.environ', {}, clear=True)
    def test_create_config_invalid_name(self, mock_get_config: Mock):
        mock_get_config.side_effect = [self.data_config]
        with self.assertRaises(ExceptionCLIValidateConfig) as e:
            Config(name='projectz')
        self.assertEqual('Name projectz not exists in config file', str(e.exception))

    @patch('cognitoctl.config.config.Config.get_config')
    @patch.dict('os.environ', {}, clear=True)
    def test_create_config_invalid_data_config(self, mock_get_config: Mock):
        mock_get_config.side_effect = [{
            'projectx': {
                'key_id': 'testx',
                'access_key': 'testx_2',
                'userpool_id': 'user_testx',
                'app_client_secret': 'client_secret_testx',
                'secret_hash': True
            },
            'projecty': {
                'key_id': 'testy',
                'access_key': 'testy_2',
                'userpool_id': 'user_testy',
                'app_client_id': 'client_id_testy',
                'secret_hash': True
            }
        }]
        with self.assertRaises(ExceptionCLIValidateConfig) as e:
            Config()
        self.assertEqual('Need these values in config file: \nConfig projectx need these values: app_client_id\n'
                         'Config projecty need these values: app_client_secret', str(e.exception))

    @patch('cognitoctl.config.config.Config.get_config')
    @patch.dict('os.environ', {}, clear=True)
    def test_create_config_invalid_data_project(self, mock_get_config: Mock):
        mock_get_config.side_effect = [{
            'current': {
                'project': 'projectx'
            },
            'projectx': {
                'key_id': 'testx',
                'access_key': 'testx_2',
                'userpool_id': 'user_testx',
                'app_client_secret': 'client_secret_testx',
                'secret_hash': True
            },
            'projecty': {
                'key_id': 'testy',
                'access_key': 'testy_2',
                'userpool_id': 'user_testy',
                'app_client_id': 'client_id_testy',
                'secret_hash': True
            }
        }]
        with self.assertRaises(ExceptionCLIValidateConfig) as e:
            Config()
        self.assertEqual('Need these values in config file: \nConfig projectx need these values: app_client_id\n'
                         'Config projecty need these values: app_client_secret', str(e.exception))
