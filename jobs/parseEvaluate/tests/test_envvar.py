import os
import logging
from unittest import TestCase, mock
from envvar import fetch_env_var

class TestEnvvar(TestCase):
    def test_fetch_env_var_uses_default_if_not_set(self):
        self.assertEqual(fetch_env_var("FAVORITE_PLANET", "earth"), "earth")

    def test_fetch_env_var_errors_if_unset_and_no_default(self):
        with mock.patch.object(logging.getLogger('envvar.fetch_env_var'), 'error') as log:
            self.assertRaises(KeyError, fetch_env_var, "FAVORITE_PLANET")
            log.assert_called_with("Required env var not set: FAVORITE_PLANET. Exiting.")

    @mock.patch.dict(os.environ, {"FAVORITE_PLANET": "mars"})
    def test_fetch_env_var_gets_value_if_var_set(self):
        self.assertEqual(fetch_env_var("FAVORITE_PLANET"), "mars")
