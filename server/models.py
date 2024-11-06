from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

# User Model for Authentication
class User(db.Model):
    _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def _repr_(self):
        return f"<User {self.name} (Role: {self.role})>"

    @staticmethod
    def validate_email(email):
        # Simple email format check
        if '@' not in email:
            raise ValueError("Invalid email format.")
    
    def validate(self):
        if len(self.name) < 3:
            raise ValueError("Name must be at least 3 characters long.")
        if len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self.validate_email(self.email)


# Cohort Model
class Cohort(db.Model):
    _tablename_ = 'cohorts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    track = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # Relationships
    projects = db.relationship('Project', backref='cohort', lazy=True, cascade="all, delete-orphan")

    def _repr_(self):
        return f"<Cohort {self.name} (Track: {self.track})>"

    def validate(self):
        if len(self.name) < 3:
            raise ValueError("Cohort name must be at least 3 characters long.")
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date.")

# Project Model
class Project(db.Model):
    _tablename_ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_url = db.Column(db.String(200), nullable=False)
    track = db.Column(db.String(50), nullable=False)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    members = db.relationship('ProjectMember', backref='project', lazy=True, cascade="all, delete-orphan")

    def _repr_(self):
        return f"<Project {self.name} (Cohort ID: {self.cohort_id})>"

    def validate(self):
        if len(self.name) < 3:
            raise ValueError("Project name must be at least 3 characters long.")
        if len(self.description) < 10:
            raise ValueError("Description must be at least 10 characters long.")
        if not self.github_url.startswith('http'):
            raise ValueError("Invalid GitHub URL format.")

# ProjectMember Model - Join table for Many-to-Many relationship between Projects and Users
class ProjectMember(db.Model):
    _tablename_ = 'project_members'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50))  # e.g., 'Developer', 'Lead', 'Reviewer'

    def _repr_(self):
        return f"<ProjectMember (Project ID: {self.project_id}, User ID: {self.user_id}, Role: {self.role})>"

    def validate(self):
        if len(self.role) < 3:
            raise ValueError("Role must be at least 3 characters long.")

# Additional function to handle integrity error (to be used when committing to DB)
def handle_integrity_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            db.session.rollback()  # Rollback in case of error
            raise ValueError("Integrity error: Something went wrong with the database.")
    return wrapper

# Example usage for validation before adding or updating
@handle_integrity_error
def add_user(user):
    user.validate()
    db.session.add(user)
    db.session.commit()
