from unittest import TestCase
from unittest.mock import patch, Mock, call, mock_open
from cognitoctl.config import Config
from cognitoctl.exceptions import ExceptionCLIValidateConfig
import tempfile
import toml
import os


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
        mock_get_config.side_effect =[self.data_config]

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
        self.assertEqual('Need set current project', str(e.exception))

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
        self.assertEqual('Need these values in config file:\nConfig projectx need these values: app_client_id\n'
                         'Config projecty need these values: app_client_secret', str(e.exception))

    def test_create_config_with_file(self):
        data = {
            'aws': {
                'key_id': 'test',
                'access_key': 'test_2'
            },
            'cognito': {
                'userpool_id': 'user_test',
                'app_client_id': 'client_id_test',
                'app_client_secret': 'client_secret_test',
                'secret_hash': True
            }
        }
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as my_file:
            with open(my_file.name, "w") as f:
                toml.dump(data, f)

            config = Config(config_file=my_file.name)
            self.assertTrue(config.status)
            self.assertTrue(config.secret_hash)
            self.assertEqual('user_test', config.userpool_id)
            self.assertEqual('client_id_test', config.app_client_id)
            self.assertEqual('client_secret_test', config.app_client_secret)
            self.assertEqual('test', config.key_id)
            self.assertEqual('test_2', config.access_key)

    def test_create_config_with_file_invalid_data(self):
        data = {
            'aws': {
                'key_id': 'test',
                'access_key': 'test_2'
            },
            'cognito': {
                'userpool_id': 'user_test',
                'app_client_id': 'client_id_test',
                'secret_hash': True
            }
        }
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as my_file:
            with open(my_file.name, "w") as f:
                toml.dump(data, f)

            with self.assertRaises(ExceptionCLIValidateConfig) as e:
                Config(config_file=my_file.name)
            self.assertEqual('Need this values in config file cognito.app_client_secret', str(e.exception))

    @patch('os.name', 'posix')
    @patch('os.path.exists', return_value=False)
    @patch('os.mkdir')
    @patch('pathlib.Path.home', return_value='/home/test')
    def test_save_config(self, mock_home: Mock, mock_mkdir: Mock, mock_exists: Mock):

        data = {
            'aws': {
                'key_id': 'test',
                'access_key': 'test_2'
            },
            'cognito': {
                'userpool_id': 'user_test',
                'app_client_id': 'client_id_test',
                'app_client_secret': 'client_secret_test',
                'secret_hash': True
            }
        }

        config = Config(config_data=data)
        with (patch('cognitopy.cli.config.config.toml.dump') as mock_toml_dump,
              patch('cognitopy.cli.config.config.open') as mock_open_file):
            config.save_config()
        self.assertEqual([call('/home/test/.pycognito')], mock_mkdir.call_args_list)
        self.assertEqual([call('/home/test/.pycognito/config.toml', 'w+')], mock_open_file.call_args_list)
        self.assertEqual(1, mock_toml_dump.call_count)
        self.assertEqual(data, mock_toml_dump.call_args_list[0][0][0])
        self.assertEqual(1, mock_exists.call_count)
        self.assertEqual(1, mock_home.call_count)

    @patch('os.name', 'posix')
    @patch('os.path.exists', return_value=True)
    @patch('os.mkdir')
    @patch('pathlib.Path.home', return_value='/home/test')
    def test_save_config_exist_dir(self, mock_home: Mock, mock_mkdir: Mock, mock_exists: Mock):
        data = {
            'aws': {
                'key_id': 'test',
                'access_key': 'test_2'
            },
            'cognito': {
                'userpool_id': 'user_test',
                'app_client_id': 'client_id_test',
                'app_client_secret': 'client_secret_test',
                'secret_hash': True
            }
        }

        config = Config(config_data=data)
        with (patch('cognitopy.cli.config.config.toml.dump') as mock_toml_dump,
              patch('cognitopy.cli.config.config.open') as mock_open_file):
            config.save_config()
        self.assertEqual(0, mock_mkdir.call_count)
        self.assertEqual([call('/home/test/.pycognito/config.toml', 'w+')], mock_open_file.call_args_list)
        self.assertEqual(1, mock_toml_dump.call_count)
        self.assertEqual(data, mock_toml_dump.call_args_list[0][0][0])
        self.assertEqual(1, mock_exists.call_count)
        self.assertEqual(1, mock_home.call_count)

    @patch('cognitopy.cli.config.config.open', new_callable=mock_open, read_data="""
    [aws]
    key_id = "test"
    access_key = "test_2"   
    [cognito]
    userpool_id = "test_user"
    app_client_id = "test_client"
    app_client_secret = "test_secret"
    secret_hash = true
    """)  # noqa: W291
    @patch('pathlib.Path.home', return_value='/home/test')
    @patch.dict('os.environ', {}, clear=True)
    def test_load_config(self, mock_home: Mock, mock_open_file: Mock):
        Config.load_config()

        self.assertEqual('test', os.environ.get('AWS_ACCESS_KEY_ID'))
        self.assertEqual('test_2', os.environ.get('AWS_SECRET_ACCESS_KEY'))
        self.assertEqual(1, mock_home.call_count)
        self.assertEqual(1, mock_open_file.call_count)

    @patch('cognitopy.cli.config.config.open', new_callable=mock_open, read_data="""
    [aws]
    key_id = "test"
    access_key = "test_2"
    """)
    @patch('pathlib.Path.home', return_value='/home/test')
    @patch.dict('os.environ', {}, clear=True)
    def test_load_config_with_error_validation(self, mock_home: Mock, mock_open_file: Mock):
        with self.assertRaises(ExceptionCLIValidateConfig) as e:
            Config.load_config()

        self.assertEqual('Need this values in config file cognito', str(e.exception))
        self.assertEqual({}, os.environ)
        self.assertEqual(1, mock_home.call_count)
        self.assertEqual(1, mock_open_file.call_count)

    @patch('pathlib.Path.home', return_value='/home/test123')
    @patch.dict('os.environ', {}, clear=True)
    def test_load_config_with_error_file_not_exist(self, mock_home: Mock):
        with self.assertRaises(ExceptionCLIValidateConfig) as e:
            Config.load_config()

        self.assertEqual('Need configurate cognito, run command init before running this command.',
                         str(e.exception))
        self.assertEqual({}, os.environ)
        self.assertEqual(1, mock_home.call_count)
