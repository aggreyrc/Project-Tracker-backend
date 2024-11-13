import pytest
from faker import Faker
from datetime import datetime, timezone
from models import User, Project, Cohort, ProjectMember, db
from app import app
from seed import seed_data

fake = Faker()

# Fixture to set up the test client and populate the database with seeded data
@pytest.fixture(scope='module')
def test_client():
    with app.app_context():
        # Drop and recreate all tables, then seed the database with initial data
        db.drop_all()
        db.create_all()
        seed_data()
        
        # Yield the test client to be used in test cases
        yield app.test_client()

        # Clean up the database after tests are done
        db.session.remove()
        db.drop_all()

# Test to verify that the correct number of users are created and each has a password hash
def test_users_created(test_client):
    with app.app_context():
        users = User.query.all()
        assert len(users) == 20, f"Expected 20 users, but found {len(users)}"
        
        # Ensure at least one admin user is created
        admin_user = User.query.filter_by(is_admin=True).first()
        assert admin_user is not None, "No admin user was created"

        # Ensure each user has a password hash set
        for user in users:
            assert user.password_hash is not None, f"User {user.username} does not have a password hash"

# Test to verify that the correct number of projects are created and they have valid attributes
def test_projects_created(test_client):
    with app.app_context():
        projects = Project.query.all()
        assert len(projects) == 25, f"Expected 25 projects, but found {len(projects)}"

        # Ensure each project has a valid GitHub URL, is assigned to a cohort, and has a creator
        for project in projects:
            assert project.github_url.startswith("https://github.com/example"), f"Project {project.name} has an incorrect GitHub URL"
            assert project.cohort_id is not None, f"Project {project.name} is not assigned to a cohort"
            assert project.user_id is not None, f"Project {project.name} does not have a creator"

# Test to verify that project members are correctly linked to projects, users, and cohorts
def test_project_members_created(test_client):
    with app.app_context():
        project_members = ProjectMember.query.all()
        assert len(project_members) > 0, "No project members were created"
        
        # Ensure each project member has a name, is linked to a project, user, and cohort
        for member in project_members:
            assert member.name is not None, "Project member has no name"
            assert member.project_id is not None, f"Project member {member.name} is not linked to any project"
            assert member.user_id is not None, f"Project member {member.name} is not linked to any user"
            assert member.cohort_id is not None, f"Project member {member.name} is not linked to any cohort"

# Test to verify that user roles are correctly set for admins and students
def test_user_roles(test_client):
    with app.app_context():
        # Query for admin and student users
        admins = User.query.filter_by(is_admin=True).all()
        students = User.query.filter_by(is_admin=False).all()

        # Ensure admins have the 'admin' role
        for admin in admins:
            assert admin.role == "admin", f"Admin user {admin.username} does not have 'admin' role"
        
        # Ensure students have the 'student' role
        for student in students:
            assert student.role == "student", f"Student user {student.username} does not have 'student' role"

# Test to ensure each user has a verification code
def test_verification_code(test_client):
    with app.app_context():
        users = User.query.all()
        
        # Ensure each user has a verification code
        for user in users:
            assert user.verification_code is not None, f"User {user.username} does not have a verification code"

# Test to ensure verification codes are generated for both admin and student users
def test_admin_verification_code(test_client):
    with app.app_context():
        # Query for admin and student users
        admin_user = User.query.filter_by(is_admin=True).first()
        student_user = User.query.filter_by(is_admin=False).first()

        # Ensure the verification code is generated for both admin and student users
        assert admin_user.generate_verification_code() is not None, "Admin user verification code not generated"
        assert student_user.generate_verification_code() is not None, "Student user verification code not generated"
