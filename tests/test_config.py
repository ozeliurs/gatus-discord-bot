import os
import unittest
from unittest import mock

class TestConfig(unittest.TestCase):

    def setUp(self):
        # Save original environment
        self.original_env = os.environ.copy()

    def tearDown(self):
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)

    def reload_config(self):
        # Reload the config module to reflect env changes
        import importlib
        import src.config
        importlib.reload(src.config)
        return src.config

    def test_gatus_api_url_not_set(self):
        os.environ.pop("GATUS_API_URL", None)
        config = self.reload_config()
        self.assertIsNone(config.GATUS_API_URL)

    def test_gatus_api_url_with_http(self):
        os.environ["GATUS_API_URL"] = "http://example.com"
        config = self.reload_config()
        self.assertEqual(config.GATUS_API_URL, "http://example.com/api")

    def test_gatus_api_url_with_https(self):
        os.environ["GATUS_API_URL"] = "https://example.com"
        config = self.reload_config()
        self.assertEqual(config.GATUS_API_URL, "https://example.com/api")

    def test_gatus_api_url_without_protocol(self):
        os.environ["GATUS_API_URL"] = "example.com"
        config = self.reload_config()
        self.assertEqual(config.GATUS_API_URL, "http://example.com/api")

    def test_gatus_api_url_with_trailing_slash(self):
        os.environ["GATUS_API_URL"] = "http://example.com/"
        config = self.reload_config()
        self.assertEqual(config.GATUS_API_URL, "http://example.com/api")

    def test_gatus_api_url_with_api(self):
        os.environ["GATUS_API_URL"] = "http://example.com/api"
        config = self.reload_config()
        self.assertEqual(config.GATUS_API_URL, "http://example.com/api")

    def test_discord_bot_token(self):
        os.environ["DISCORD_BOT_TOKEN"] = "test_token"
        config = self.reload_config()
        self.assertEqual(config.DISCORD_BOT_TOKEN, "test_token")

    def test_discord_bot_token_not_set(self):
        os.environ.pop("DISCORD_BOT_TOKEN", None)
        config = self.reload_config()
        self.assertIsNone(config.DISCORD_BOT_TOKEN)
