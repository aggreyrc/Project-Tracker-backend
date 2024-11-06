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
    is_admin = db.Column(db.Boolean, default=False)  # True for admin, False for student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Permissions
    def can_add_project(self):
        """All users can add projects."""
        return True

    def can_delete_project(self):
        """Only admin users can delete projects."""
        return self.is_admin

    def can_manage_project_members(self):
        """Only admin users can add or remove project members."""
        return self.is_admin

    def can_manage_cohorts(self):
        """Only admin users can add or remove cohorts."""
        return self.is_admin

    def __repr__(self):
        return f"<User {self.username} (Admin: {self.is_admin})>"

# Project Model
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_url = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Changed from 'track' to 'type'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key linking Project to one Cohort
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    members = db.relationship(
        'ProjectMember',
        backref='project',
        lazy=True,
        cascade="all, delete-orphan"  # Delete project members when a project is deleted
    )

    def __repr__(self):
        return f"<Project {self.name}>"

# Cohort Model
class Cohort(db.Model):
    __tablename__ = 'cohorts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Changed from 'track' to 'type'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # Relationship with Project
    projects = db.relationship(
        'Project',
        backref='cohort',
        lazy=True,
        cascade="all, delete"  # Delete projects when a cohort is deleted
    )

    def __repr__(self):
        return f"<Cohort {self.name} (Type: {self.type})>"

# ProjectMember Model - Association between Projects and Cohorts
class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id', ondelete='CASCADE'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50))  # e.g., 'Developer', 'Lead', 'Reviewer'

    def __repr__(self):
        return f"<ProjectMember (Project ID: {self.project_id}, Cohort ID: {self.cohort_id}, Role: {self.role})>"




