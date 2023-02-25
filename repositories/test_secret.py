import logging
import os
import sys
import unittest
sys.path.insert(1, os.getcwd())
from secret import SecretRepository, Secret

logger = logging.getLogger(__name__)

class TestSecret(unittest.TestCase):
    def test_secret(self):
        repo = SecretRepository()
        
        secret = Secret(0, 1, "test_question", "test_answer")
        repo.save(secret)

        actual = repo.get_app_secret_for_user(0, 1, "test")
        logger.info(f'comparing {actual} to {secret}')
        self.assertEqual(actual.app_id, secret.app_id)
        self.assertEqual(actual.user_id, secret.user_id)


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    unittest.main()