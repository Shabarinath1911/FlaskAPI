import unittest
from main import app  # assuming your file is named main.py

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_world(self):
        response = self.app.get('/')
        self.assertEqual(response.data, b'Hello, World!')

    def test_get_data(self):
        response = self.app.get('/api/data')
        json_data = response.get_json()
        self.assertEqual(json_data['name'], 'John Doe')
        self.assertEqual(json_data['age'], 30)
        self.assertEqual(json_data['city'], 'New York')

    # def test_add_data(self):
    #     response = self.app.post('/api/add', json={'name': 'Jane Doe', 'age': 25})
    #     json_data = response.get_json()
    #     self.assertEqual(json_data['message'], 'Data received!')
    #     self.assertEqual(json_data['data']['name'], 'Jane Doe')
    #     self.assertEqual(json_data['data']['age'], 25)
    #
    # def test_add_data_no_input(self):
    #     response = self.app.post('/api/add', json=None)
    #     json_data = response.get_json()
    #     self.assertEqual(json_data['error'], 'No data provided')
    #     self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
