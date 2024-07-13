import unittest
from app.utils import upload_avatar

class TestUtils(unittest.TestCase):
    def test_upload_avatar(self):
        # Мок об'єктів для тесту
        file = "path/to/mock/file.jpg"
        result = upload_avatar(file)
        self.assertIsNotNone(result)
        self.assertIn("url", result)

if __name__ == "__main__":
    unittest.main()
