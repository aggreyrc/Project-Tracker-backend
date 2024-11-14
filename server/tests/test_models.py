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


