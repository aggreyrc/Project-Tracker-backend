


import random
import string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_mail import Mail, Message
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt, app, mail


# User Model for Authentication
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # True for admin, False for student
    is_verified = db.Column(db.Boolean, default=False)  # Field to track verification status
    verification_code = db.Column(db.String(6), nullable=True)  # Field to store verification code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Serialization rules: excluding sensitive fields
    serialize_rules = ('-password', '-verification_code')

    def __repr__(self):
        return f"<User {self.username} (Admin: {self.is_admin}, Verified: {self.is_verified})>"

    # Generate a random 6-digit verification code
    def generate_verification_code(self):
        code = ''.join(random.choices(string.digits, k=6))
        self.verification_code = code
        db.session.commit()
        return code

    # Validate email format
    @staticmethod
    def validate_email(email):
        if '@' not in email:
            raise ValueError("Invalid email format.")

    # Validate username and password, and send verification code
    def validate_and_send_code(self):
        if len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        if len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self.validate_email(self.email)
        
        # Generate and send verification code
        code = self.generate_verification_code()
        send_verification_email(self.email, code)

    # Verify code entered by user
    def verify_user(self, code_entered):
        if self.verification_code == code_entered:
            self.is_verified = True
            self.verification_code = None  # Clear the code after successful verification
            db.session.commit()
            return True
        return False


# Function to send the verification email
def send_verification_email(recipient_email, code):
    msg = Message(
        subject="Your Verification Code",
        sender="yourapp@example.com",  # Replace with your actual sender email
        recipients=[recipient_email],
        body=f"Your verification code is: {code}"
    )
    mail.send(msg)


# Project Model
class Project(db.Model, SerializerMixin):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_url = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # project type
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(255), nullable=True)  # New column for optional image URL

    # Relationships
    cohort = db.relationship('Cohort', back_populates='projects')
    project_members = db.relationship(
        'ProjectMember',
        back_populates='project',  # Explicitly defining bidirectional relationship
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Project {self.name}>"

    # Validators
    def validate(self):
        if len(self.name) < 3:
            raise ValueError("Project name must be at least 3 characters long.")
        if len(self.description) < 10:
            raise ValueError("Description must be at least 10 characters long.")
        if not self.github_url.startswith('http'):
            raise ValueError("Invalid GitHub URL format.")


# Cohort Model
class Cohort(db.Model, SerializerMixin):
    __tablename__ = 'cohorts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(50), nullable=False)
    github_url = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # Relationship with Project
    projects = db.relationship(
        'Project',
        back_populates='cohort',
        lazy=True,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Cohort {self.name} (Type: {self.type})>"

    # Validators
    def validate(self):
        if len(self.name) < 3:
            raise ValueError("Cohort name must be at least 3 characters long.")
        if not self.github_url.startswith('http'):
            raise ValueError("Invalid GitHub URL format.")


# ProjectMember Model - Join table for Many-to-Many relationship between Projects and Users
class ProjectMember(db.Model, SerializerMixin):
    __tablename__ = 'project_members'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # No foreign key, purely associative
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50))  # e.g., 'Developer', 'Lead', 'Reviewer'

    # Relationships
    project = db.relationship('Project', back_populates='project_members', lazy=True)  # Using back_populates

    def __repr__(self):
        return f"<ProjectMember (Project ID: {self.project_id}, User ID: {self.user_id}, Role: {self.role})>"

    # Validators
    def validate(self):
        if len(self.role) < 3:
            raise ValueError("Role must be at least 3 characters long.")


# Integrity error handler decorator
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
    user.validate_and_send_code()  # Validate and send code during user registration
    db.session.add(user)
    db.session.commit()
