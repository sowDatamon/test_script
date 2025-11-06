import unittest
from sender import build_message


class TestSender(unittest.TestCase):
    def test_build_message_sets_fields(self):
        msg = build_message("Asunto", "Cuerpo aquí", "from@example.com", ["a@example.com", "b@example.com"])
        self.assertEqual(msg["Subject"], "Asunto")
        self.assertEqual(msg["From"], "from@example.com")
        self.assertIn("a@example.com", msg["To"])
        self.assertIn("b@example.com", msg["To"])
        self.assertIn("Cuerpo aquí", msg.get_content())


if __name__ == "__main__":
    unittest.main()
