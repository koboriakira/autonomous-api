import unittest
from app.prompt.domain.model.prompt import Prompt

class TestPrompt(unittest.TestCase):
    def test_post_init(self):
        with self.assertRaises(ValueError):
            Prompt.of(
                messages=[],
                temperature=-1,
                )
        with self.assertRaises(ValueError):
            Prompt.of(
                messages=[],
                temperature=2.1,
                )
