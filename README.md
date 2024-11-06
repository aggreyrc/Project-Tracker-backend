# Project-Tracking

## Overview
The Student Project Tracker is a Flask-based web application designed to help manage student projects, cohort groups, and project members. The application allows users to create, view, and manage projects, with different permissions for admin and student roles.

Admins: Can add, delete, and manage projects, project members, and cohorts.
Students: Can add projects but have limited permissions on other resources.
Features
User Management: Admin and student roles with distinct permissions.
Project Management: Admins and students can add projects; only admins can delete projects.
Cohort Management: Cohorts can have multiple projects, and admins can manage them.
Project Members: Each project member belongs to one project and one cohort.
## Models
User
The User model represents users with fields for username, email, password, and a boolean is_admin attribute for role designation.

# Attributes:
username (string): Username of the user.
email (string): Unique email address of the user.
password (string): Password hash for the user.
is_admin (boolean): Indicates if the user is an admin.
Permissions:
can_add_project: Allows all users to add projects.
can_delete_project: Allows only admins to delete projects.
can_manage_project_members: Allows only admins to manage project members.
can_manage_cohorts: Allows only admins to manage cohorts.
## Project
The Project model represents a project associated with a cohort.

# Attributes:
name (string): Name of the project.
description (text): Project description.
github_url (string): URL of the project's GitHub repository.
type (string): Type of the project (e.g., web, mobile, data science).
cohort_id (foreign key): Links to a cohort.
created_at (datetime): Date and time the project was created.
Relationships:
members: List of ProjectMember records associated with the project.
## Cohort
The Cohort model represents a group of students or project members.

# Attributes:
name (string): Unique name of the cohort.
type (string): Type of the cohort (e.g., full stack, data science).
start_date (date): Cohort start date.
end_date (date): Cohort end date.
Relationships:
projects: List of projects associated with the cohort.

## ProjectMember
The ProjectMember model represents a member of a project.

# Attributes:
project_id (foreign key): ID of the associated project.
cohort_id (foreign key): ID of the associated cohort.
joined_at (datetime): Date and time the member joined the project.
role (string): Role of the member in the project (e.g., Developer, Lead, Reviewer).
## Setup and Installation
Prerequisites
Python 3.10+
Flask and Flask-SQLAlchemy