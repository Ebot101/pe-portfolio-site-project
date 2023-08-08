import unittest
import os

os.environ['FLASK_ENV'] = 'testing'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')        
        assert response.status_code == 200

        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        assert ".jpeg" or ".jpg" or ".png" in html
        assert "main.css" in html
        assert "logo.svg" in html
        assert "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" in html
        

    def test_timeline(self):
        response = self.client.get('/api/timeline_post')        
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # timeline posts
        response = self.client.post('/api/timeline_post', data={"email": "john@example.com", "content": "Hello world, I'm John!", "name":"John Doe"})        
        assert response.status_code == 200
        html = response.get_data(as_text=True)         
        assert "Hello world" in html

        # timeline page
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "timeline.css" in html
        assert "logo.svg" in html
        assert "https://fonts.gstatic.com" in html


    def test_malformed_timeline_post(self):
        response = self.client.post('/api/timeline_post', data={"email": "john@example.com", "content": "Hello world, I'm John!"})        
        assert response.status_code == 400
        html = response.get_data(as_text=True)    
        assert "Invalid name" in html

        response = self.client.post('/api/timeline_post', data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post('/api/timeline_post', data={"name": "John Doe", "email": "", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html


