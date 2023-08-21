import unittest
from unittest.mock import MagicMock
from chatbot import predict_class, get_response

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock()
        self.mock_model.predict.return_value = [[0.8, 0.2]]

    def test_predict_class(self):
        sentence = "Szia"
        expected_result = [{'intent': 'üdvözlet', 'probability': '0.99987185'}]

        result = predict_class(sentence)

        self.assertEqual(result, expected_result)

    def test_get_response(self):
        intents_list = [{'intent': 'üdvözlet', 'probability': '0.99987185'}]
        intents_json = {
            'intents': [
                {'tag': 'üdvözlet', 'patterns': ['Szia'], 'responses': ['Szia. Mond el, hogy érzed magad ma?']}
            ]
        }
        username = "patrik114500"

        expected_response = "Szia. Mond el, hogy érzed magad ma?"

        response = get_response(intents_list, intents_json, username)

        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()