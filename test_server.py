import unittest
import json
from server import app

class TestJarvisServer(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_index_page(self):
        """Test serving main web app index.html."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'JARVIS', response.data)

    def test_info_endpoint(self):
        """Test system info endpoint."""
        response = self.client.get('/api/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'JARVIS AI Voice Assistant')
        self.assertEqual(data['author']['name'], 'Ansh Tyagi')

    def test_sound_asset_endpoint(self):
        """Test audio notification asset serving."""
        response = self.client.get('/api/sounds/ding_start.mp3')
        self.assertEqual(response.status_code, 200)

    def test_date_command(self):
        """Test date command execution."""
        response = self.client.post('/api/process_command', 
                                   data=json.dumps({'command': 'what is the date'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('date', data['response'].lower())

    def test_joke_command(self):
        """Test joke command execution."""
        response = self.client.post('/api/process_command', 
                                   data=json.dumps({'command': 'tell me a joke'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(len(data['response']) > 0)

    def test_weather_command(self):
        """Test weather command execution response speed."""
        response = self.client.post('/api/process_command', 
                                   data=json.dumps({'command': 'weather in Delhi'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('delhi', data['response'].lower())

    def test_weather_landran(self):
        """Test weather command for Landran to verify no HTML markup leak."""
        response = self.client.post('/api/process_command', 
                                   data=json.dumps({'command': 'weather in Landran'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertNotIn('<DOCTYPE', data['response'].upper())
        self.assertNotIn('<HTML', data['response'].upper())
        self.assertIn('landran', data['response'].lower())

if __name__ == '__main__':
    unittest.main()
