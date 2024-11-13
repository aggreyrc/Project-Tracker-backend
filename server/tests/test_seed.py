import pytest
from faker import Faker
from datetime import datetime, timezone
from models import User, Project, Cohort, ProjectMember, db
from app import app
from seed import seed_data

fake = Faker()

@pytest.fixture(scope='module')
def test_client():
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_data()
        
        yield app.test_client()

        db.session.remove()
        db.drop_all()

def test_users_created(test_client):
    with app.app_context():
        users = User.query.all()
        assert len(users) == 20, f"Expected 20 users, but found {len(users)}"
        
        admin_user = User.query.filter_by(is_admin=True).first()
        assert admin_user is not None, "No admin user was created"

        for user in users:
            assert user.password_hash is not None, f"User {user.username} does not have a password hash"

def test_projects_created(test_client):
    with app.app_context():
        projects = Project.query.all()
        assert len(projects) == 25, f"Expected 25 projects, but found {len(projects)}"

        for project in projects:
            assert project.github_url.startswith("https://github.com/example"), f"Project {project.name} has an incorrect GitHub URL"
            assert project.cohort_id is not None, f"Project {project.name} is not assigned to a cohort"
            assert project.user_id is not None, f"Project {project.name} does not have a creator"

def test_project_members_created(test_client):
    with app.app_context():
        project_members = ProjectMember.query.all()
        assert len(project_members) > 0, "No project members were created"
        
        for member in project_members:
            assert member.name is not None, "Project member has no name"
            assert member.project_id is not None, f"Project member {member.name} is not linked to any project"
            assert member.user_id is not None, f"Project member {member.name} is not linked to any user"
            assert member.cohort_id is not None, f"Project member {member.name} is not linked to any cohort"

def test_user_roles(test_client):
    with app.app_context():
        admins = User.query.filter_by(is_admin=True).all()
        students = User.query.filter_by(is_admin=False).all()

        for admin in admins:
            assert admin.role == "admin", f"Admin user {admin.username} does not have 'admin' role"
        
        for student in students:
            assert student.role == "student", f"Student user {student.username} does not have 'student' role"

def test_verification_code(test_client):
    with app.app_context():
        users = User.query.all()
        
        for user in users:
            assert user.verification_code is not None, f"User {user.username} does not have a verification code"

def test_admin_verification_code(test_client):
    with app.app_context():
        admin_user = User.query.filter_by(is_admin=True).first()
        student_user = User.query.filter_by(is_admin=False).first()

        assert admin_user.generate_verification_code() is not None, "Admin user verification code not generated"
        assert student_user.generate_verification_code() is not None, "Student user verification code not generated"
