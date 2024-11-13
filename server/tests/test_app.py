import unittest
import json
from app import app, db
from models import User, Project

class ProjectTrackerAPITestCase(unittest.TestCase):
    
    # Setup for the entire class: creating the in-memory database and initializing the app.
    @classmethod
    def setUpClass(cls):
        cls.app = app  # Assign the Flask app to the class variable
        cls.client = cls.app.test_client()  # Initialize the test client
        cls.app.config['TESTING'] = True  # Enable testing mode in Flask
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
        
        # Create all tables for the database
        with cls.app.app_context():
            db.create_all()

    # Teardown for the entire class: dropping all tables after tests are completed.
    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()  # Drop all tables after tests are done

    # Setup for each individual test: creating a test user
    def setUp(self):
        self.client.post('/signup', json={
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com",
            "role": "member"
        })

    # Teardown for each individual test: clean up the session and re-create the database
    def tearDown(self):
        with app.app_context():
            db.session.remove()  # Remove any active session
            db.drop_all()  # Drop all tables to reset the database
            db.create_all()  # Recreate tables for the next test
    
    # Test case for the home endpoint
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)  # Check that the status code is 200
        data = json.loads(response.data)  # Parse the JSON response
        self.assertIn("Welcome to the Project Tracker API", data['message'])  # Ensure the message is in the response
    
    # Test case for the signup endpoint
    def test_signup(self):
        response = self.client.post('/signup', json={
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com",
            "role": "member"
        })
        self.assertEqual(response.status_code, 201)  # Check for successful user creation (status code 201)
        data = json.loads(response.data)  # Parse the response data
        self.assertIn("User created successfully", data['message'])  # Verify that the success message is present
    
    # Test case to ensure duplicate usernames are handled correctly
    def test_signup_duplicate_username(self):
        response = self.client.post('/signup', json={
            "username": "testuser",
            "password": "password123",
            "email": "duplicate@example.com",
            "role": "member"
        })
        self.assertEqual(response.status_code, 409)  # Check for conflict (status code 409)
        data = json.loads(response.data)  # Parse the response data
        self.assertIn("Username already taken", data['error'])  # Ensure the error message is correct
    
    # Test case for the login endpoint (valid credentials)
    def test_login(self):
        response = self.client.post('/login', json={
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)  # Ensure login is successful (status code 200)
        data = json.loads(response.data)  # Parse the response data
        self.assertIn("Logged in successfully", data['message'])  # Ensure the login success message is present
    
    # Test case for the login endpoint (invalid credentials)
    def test_login_invalid(self):
        response = self.client.post('/login', json={
            "username": "wronguser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)  # Unauthorized error for invalid credentials (status code 401)
        data = json.loads(response.data)  # Parse the response data
        self.assertIn("Invalid credentials", data['error'])  # Ensure the error message is correct
    
    # Test case for retrieving all users from the /users endpoint
    def test_get_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)  # Ensure status code is 200 (OK)
        data = json.loads(response.data)  # Parse the response data
        self.assertTrue('users' in data)  # Ensure the 'users' key exists in the response data
    
    # Test case for retrieving all projects from the /projects endpoint
    def test_get_projects(self):
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)  # Ensure status code is 200 (OK)
        data = json.loads(response.data)  # Parse the response data
        self.assertTrue('projects' in data)  # Ensure the 'projects' key exists in the response data

# Entry point for running the tests
if __name__ == '__main__':
    unittest.main()
