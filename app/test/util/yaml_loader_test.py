from unittest import TestCase
from app.util.yaml_loader import YamlLoader

class YamLoaderTest(TestCase):
    def test_load(self):
        _ = YamlLoader.load('healthcheck','define.yaml')
        self.assertTrue(True)
