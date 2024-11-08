from datetime import datetime
from app import bcrypt
from sqlalchemy_serializer import SerializerMixin
from app import db


# User Model for Authentication
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # True for admin, False for student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String, nullable=False)
    

    # relationships
    projects = db.relationship('Project',back_populates='user', cascade="all, delete-orphan")

    # serialize_rules
    serialize_rules = ('-projects.user')

    def __repr__(self):
        return f"<User {self.username} (Admin: {self.is_admin}) (Role: {self.role}) >"
   

    @staticmethod
    def validate_email(email):
        # Simple email format check
        if '@' not in email:
            raise ValueError("Invalid email format.")
    
    def validate(self):
        if len(self.username) < 3:
            raise ValueError("Name must be at least 3 characters long.")
        if len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self.validate_email(self.email)

    # For authentication
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)



# Project Model
class Project(db.Model, SerializerMixin):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key linking Project to one Cohort
    user_id= db.Column(db.Integer,db.ForeignKey('users.id') , nullable=False)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'), nullable=False)

    # Relationships
    user = db.relationship('User',back_populates='projects', cascade="all, delete-orphan") 
    members = db.relationship('ProjectMember', back_populates='project',cascade="all, delete-orphan")  
    cohort = db.relationship('Cohort', back_populates="projects", cascade="all, delete-orphan")

    # serialize_rules
    serialize_rules = ('-user.projects',) 

    def __repr__(self):
        return f"<Project {self.name}>"
    


# Cohort Model
class Cohort(db.Model, SerializerMixin):
    __tablename__ = 'cohorts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    # Relationship 
    projects = db.relationship('Project',back_populates='cohort',cascade="all, delete-orphan")

    # serialize_rules
    serialize_rules = ('-projects.members',)

    def __repr__(self):
        return f"<Cohort {self.name} (Type: {self.type})>"



    def validate(self):
        if len(self.name) < 3:
            raise ValueError("Project name must be at least 3 characters long.")
        if len(self.description) < 10:
            raise ValueError("Description must be at least 10 characters long.")
        if not self.github_url.startswith('http'):
            raise ValueError("Invalid GitHub URL format.")





# ProjectMember Model - Join table for Many-to-Many relationship between Projects and Users
class ProjectMember(db.Model, SerializerMixin):
    __tablename__ = 'project_members'
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50))  # e.g., 'Developer', 'Lead', 'Reviewer'

    # Foreign id
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id', ondelete='CASCADE'), nullable=False)
   
    # relationship
    project = db.relationship('Project', back_populates='project_members', lazy=True)

    # serialize_rules
    serialize_rules = ('-project.members',) 


    def __repr__(self):
        return f"<ProjectMember (Project ID: {self.project_id}, Cohort ID: {self.cohort_id}, Role: {self.role})>"


    def validate(self):
        if len(self.role) < 3:
            raise ValueError("Role must be at least 3 characters long.")



