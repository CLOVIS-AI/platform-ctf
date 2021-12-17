from .utils import DBTestCase
from ..config import TestingConfig


class TestConfig(DBTestCase):

    def test_testing_config(self):
        configuration = TestingConfig()
        self.assertEqual(configuration.BASE_INSTANCE_DATA, "/tmp/data/instances")

    def test_testing_config_via_app_creation(self):
        self.assertEqual(self.app.configuration.BASE_INSTANCE_DATA, "/tmp/data/instances")
