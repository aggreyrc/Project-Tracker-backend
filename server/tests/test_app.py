import unittest
import json
from app import app, db
from models import User, Project

class ProjectTrackerAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        self.client.post('/signup', json={
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com",
            "role": "member"
        })
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("Welcome to the Project Tracker API", data['message'])
    
    def test_signup(self):
        response = self.client.post('/signup', json={
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com",
            "role": "member"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("User created successfully", data['message'])
    
    def test_signup_duplicate_username(self):
        response = self.client.post('/signup', json={
            "username": "testuser",
            "password": "password123",
            "email": "duplicate@example.com",
            "role": "member"
        })
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertIn("Username already taken", data['error'])
    
    def test_login(self):
        response = self.client.post('/login', json={
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("Logged in successfully", data['message'])
    
    def test_login_invalid(self):
        response = self.client.post('/login', json={
            "username": "wronguser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn("Invalid credentials", data['error'])
    
    def test_get_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue('users' in data)
    
    def test_get_projects(self):
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue('projects' in data)

if __name__ == '__main__':
    unittest.main()
