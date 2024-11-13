import pytest
from datetime import datetime, timedelta
from app import app, db
from models import User, Project, Cohort, ProjectMember

# Fixture to set up the test client for module scope, which is shared across tests in the module.
@pytest.fixture(scope='module')
def test_client():
    # Setting up the app test client
    with app.test_client() as client:
        # Using app context to interact with the database
        with app.app_context():
            db.create_all()  # Create all tables in the database before running tests
            yield client  # Provide the test client to the test functions
            db.drop_all()  # Drop all tables after the tests have been completed

# Fixture that resets the database before each test function (autouse=True ensures it's used automatically)
@pytest.fixture(scope='function', autouse=True)
def reset_db():
    with app.app_context():
        db.session.remove()  # Remove any active session
        db.drop_all()  # Drop all tables in the database to ensure clean state
        db.create_all()  # Recreate tables for the next test

# Test case for user creation and initial validation
def test_user_creation():
    with app.app_context():
        # Create a new user object
        user = User(username='testuser', email='testuser@example.com', role='student')
        user.set_password_hash('testpass')  # Hash the password
        user.validate_and_send_code()  # Generate and send verification code
        db.session.add(user)  # Add user to the session
        db.session.commit()  # Commit the changes to the database

        # Assertions to ensure the user has been created and validation logic works
        assert user.id is not None  # Check that the user has an ID (created)
        assert user.is_verified is False  # Ensure user is not verified initially
        assert user.verification_code is not None  # Ensure a verification code is generated

# Test case for user verification after registration
def test_user_verification():
    with app.app_context():
        # Create a user object and generate a verification code
        user = User(username='verifyuser', email='verifyuser@example.com', role='student')
        user.set_password_hash('testpass')  # Hash the password
        user.generate_verification_code()  # Generate a verification code
        db.session.add(user)  # Add the user to the database
        db.session.commit()  # Commit the user to the database

        # Assertions to ensure the verification process works
        assert user.verify_user(user.verification_code) is True  # Verify the user with the code
        assert user.is_verified is True  # Check that the user is marked as verified
        assert user.verification_code is None  # Ensure the verification code is cleared after successful verification

# Test case for project creation and validation
def test_project_creation():
    with app.app_context():
        # Create a user to own the project
        user = User(username='projectowner', email='owner@example.com', role='student')
        user.set_password_hash('testpass')  # Hash the password
        db.session.add(user)  # Add the user to the session
        db.session.commit()  # Commit the user to the database

        # Create a project associated with the created user
        project = Project(
            name='Project 1',
            description='A test project description.',
            github_url='http://github.com/project1',
            type='Web',
            user_id=user.id  # Link project to the user
        )
        project.validate()  # Validate the project
        db.session.add(project)  # Add the project to the session
        db.session.commit()  # Commit the project to the database

        # Assertions to ensure the project was created correctly
        assert project.id is not None  # Ensure the project has an ID (indicating it was created)
        assert project.name == 'Project 1'  # Verify the project name matches the expected value

# Test case for cohort creation and validation
def test_cohort_creation():
    with app.app_context():
        # Create a cohort object with relevant details
        cohort = Cohort(
            name='Cohort 1',
            description='Sample cohort description.',
            github_url='http://github.com/cohort1',
            type='Full Stack',
            start_date=datetime.utcnow(),
            end_date=(datetime.utcnow() + timedelta(days=30)).isoformat()  # Set an end date 30 days later
        )
        cohort.validate()  # Validate the cohort
        db.session.add(cohort)  # Add cohort to the session
        db.session.commit()  # Commit the cohort to the database

        # Assertions to ensure the cohort was created correctly
        assert cohort.id is not None  # Ensure the cohort has an ID
        assert cohort.name == 'Cohort 1'  # Verify the cohort name is correct

# Test case for creating a project member and validating the relationship with user and project
def test_project_member_creation():
    with app.app_context():
        # Create a user to be assigned as a project member
        user = User(username='memberuser', email='member@example.com', role='student')
        user.set_password_hash('testpass')  # Hash the password
        db.session.add(user)  # Add user to the session
        db.session.commit()  # Commit the user to the database

        # Create a cohort and a project for the user to be a member of
        cohort = Cohort(
            name='Cohort 2',
            description='Another sample cohort.',
            github_url='http://github.com/cohort2',
            type='Data Science',
            start_date=datetime.utcnow(),
            end_date=(datetime.utcnow() + timedelta(days=30)).isoformat()  # Set an end date 30 days later
        )
        db.session.add(cohort)  # Add cohort to the session
        db.session.commit()  # Commit the cohort to the database

        # Create a project for the user to work on
        project = Project(
            name='Project 2',
            description='Another test project description.',
            github_url='http://github.com/project2',
            type='Data Science',
            user_id=user.id,  # Link the project to the user
            cohort_id=cohort.id  # Link the project to the cohort
        )
        db.session.add(project)  # Add project to the session
        db.session.commit()  # Commit the project to the database

        # Create a project member and assign them to the project
        member = ProjectMember(
            name='Member 1',
            project_id=project.id,  # Link member to the project
            user_id=user.id,  # Link member to the user
            role='Developer'  # Assign a role to the member
        )
        member.validate()  # Validate the project member
        db.session.add(member)  # Add member to the session
        db.session.commit()  # Commit the member to the database

        # Assertions to ensure the project member was created and linked correctly
        assert member.id is not None  # Ensure the member has been created with an ID
        assert member.role == 'Developer'  # Check the member's role
        assert member.project_id == project.id  # Verify the project ID matches the project
        assert member.user_id == user.id  # Verify the user ID matches the user
