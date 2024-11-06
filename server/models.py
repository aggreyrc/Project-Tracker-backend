from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Boolean: True for admin, False for student
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def can_add_project(self):
        """Check if the user can add a project."""
        return self.role in ['student', 'admin']

    def can_delete_project(self):
        """Check if the user can delete a project."""
        return self.role == 'admin'

    def can_edit_project(self):
        """Check if the user can edit a project."""
        return self.role == 'admin'

    def can_delete_project_member(self):
        """Check if the user can delete a project member."""
        return self.role == 'admin'

    def can_delete_cohort(self):
        """Check if the user can delete a cohort."""
        return self.role == 'admin'

    def __repr__(self):
        return f"<User {self.name} (Role: {self.role})>"

# Project Model
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_url = db.Column(db.String(200), nullable=False)
    track = db.Column(db.String(50), nullable=False)
    cohort = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    members = db.relationship(
        'ProjectMember',
        backref='project',
        lazy=True,
        cascade="all, delete-orphan"  # Delete project members when a project is deleted
    )
    cohorts = db.relationship(
        'Cohort',
        backref='project',
        lazy=True,
        cascade="all, delete"  # Delete cohorts when a project is deleted
    )

    def __repr__(self):
        return f"<Project {self.name} (Cohort: {self.cohort})>"

# Cohort Model
class Cohort(db.Model):
    __tablename__ = 'cohorts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    track = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"<Cohort {self.name} (Track: {self.track})>"

# ProjectMember Model - Join table for Many-to-Many relationship between Users and Projects
class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50))  # e.g., 'Developer', 'Lead', 'Reviewer'

    def __repr__(self):
        return f"<ProjectMember (Project ID: {self.project_id}, User ID: {self.user_id}, Role: {self.role})>"
