import pytest
from datetime import datetime, timedelta
from app import app, db
from models import User, Project, Cohort, ProjectMember

@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture(scope='function', autouse=True)
def reset_db():
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

def test_user_creation():
    with app.app_context():
        user = User(username='testuser', email='testuser@example.com', role='student')
        user.set_password_hash('testpass')
        user.validate_and_send_code()
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.is_verified is False
        assert user.verification_code is not None

def test_user_verification():
    with app.app_context():
        user = User(username='verifyuser', email='verifyuser@example.com', role='student')
        user.set_password_hash('testpass')
        user.generate_verification_code()
        db.session.add(user)
        db.session.commit()

        assert user.verify_user(user.verification_code) is True
        assert user.is_verified is True
        assert user.verification_code is None

def test_project_creation():
    with app.app_context():
        user = User(username='projectowner', email='owner@example.com', role='student')
        user.set_password_hash('testpass')
        db.session.add(user)
        db.session.commit()

        project = Project(
            name='Project 1',
            description='A test project description.',
            github_url='http://github.com/project1',
            type='Web',
            user_id=user.id
        )
        project.validate()
        db.session.add(project)
        db.session.commit()

        assert project.id is not None
        assert project.name == 'Project 1'

def test_cohort_creation():
    with app.app_context():
        cohort = Cohort(
            name='Cohort 1',
            description='Sample cohort description.',
            github_url='http://github.com/cohort1',
            type='Full Stack',
            start_date=datetime.utcnow(),
            end_date=(datetime.utcnow() + timedelta(days=30)).isoformat()
        )
        cohort.validate()
        db.session.add(cohort)
        db.session.commit()

        assert cohort.id is not None
        assert cohort.name == 'Cohort 1'

def test_project_member_creation():
    with app.app_context():
        user = User(username='memberuser', email='member@example.com', role='student')
        user.set_password_hash('testpass')
        db.session.add(user)
        db.session.commit()

        cohort = Cohort(
            name='Cohort 2',
            description='Another sample cohort.',
            github_url='http://github.com/cohort2',
            type='Data Science',
            start_date=datetime.utcnow(),
            end_date=(datetime.utcnow() + timedelta(days=30)).isoformat()
        )
        db.session.add(cohort)
        db.session.commit()

        project = Project(
            name='Project 2',
            description='Another test project description.',
            github_url='http://github.com/project2',
            type='Data Science',
            user_id=user.id,
            cohort_id=cohort.id
        )
        db.session.add(project)
        db.session.commit()

        member = ProjectMember(
            name='Member 1',
            project_id=project.id,
            user_id=user.id,
            role='Developer'
        )
        member.validate()
        db.session.add(member)
        db.session.commit()

        assert member.id is not None
        assert member.role == 'Developer'
        assert member.project_id == project.id
        assert member.user_id == user.id
