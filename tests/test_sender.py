import unittest
from sender import build_message


class TestSender(unittest.TestCase):
    def test_build_message_sets_fields(self):
        msg = build_message("prueba", "pruebas de envio", "neybassj@gmail.com", ["sow@datamon.es"])
        # CORRECCIÓN: Cambiado "testing" a "Subject"
        self.assertEqual(msg["Subject"], "prueba") 
        self.assertEqual(msg["From"], "neybassj@gmail.com")
        self.assertIn("sow@datamon.es", msg["To"])
        self.assertIn("pruebas de envio", msg.get_content())


if __name__ == "__main__":
    unittest.main()