import unittest
import json
from app import app, db
from models import User, Project
from werkzeug.security import generate_password_hash

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
