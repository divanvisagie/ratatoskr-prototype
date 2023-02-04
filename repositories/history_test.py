import unittest
import history

class TestHistoryRepository(unittest.TestCase):
    def test_save_new_app(self):
        history.save_app("Notion")
        id = history.get_app_id_by_name("Notion")
        self.assertTrue(id > 0)
    
    def test_get_app_id_by_name(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()