from faker import Faker
from models import db, User, Project, Cohort, ProjectMember
from app import app
import random

# Initialize Faker instance for generating random data
fake = Faker()

# Constants defining the number of records to create for each model
NUM_USERS = 10
NUM_PROJECTS = 40 
NUM_COHORTS = 3
NUM_PROJECT_MEMBERS = 15

# Clear existing data and create fresh tables
with app.app_context():
    # Drop all existing tables and recreate them
    db.drop_all()
    db.create_all()

    
    # Seed Cohorts
 
    cohorts = []  # List to keep track of created cohort instances
    for _ in range(NUM_COHORTS):
        cohort = Cohort(
            name=f"{fake.word().capitalize()} Cohort",  # Random cohort name
            track=fake.random_element(elements=["Web", "Data Science", "DevOps"]),  # Random track
            start_date=fake.date_this_decade(),  # Random start date
            end_date=fake.date_this_decade()     # Random end date
        )
        db.session.add(cohort)  # Add cohort to the session
        cohorts.append(cohort)  # Append cohort to list for later reference
    db.session.commit()  # Commit all cohort records to the database

  
    # Seed Users
   
    users = []  # List to keep track of created user instances
    for _ in range(NUM_USERS):
        user = User(
            name=fake.name(),  # Random user name
            email=fake.unique.email(),  # Unique random email
            password=fake.password(length=10),  # Random password with specified length
            role=fake.random_element(elements=["student", "admin"]),  # Random role, either student or admin
            cohort=random.choice(cohorts).name  # Assign user to a random cohort
        )
        db.session.add(user)  # Add user to the session
        users.append(user)  # Append user to list for later reference
    db.session.commit()  # Commit all user records to the database

    # Seed Projects
  
    projects = []  # List to keep track of created project instances
    for _ in range(NUM_PROJECTS):
        project = Project(
            name=f"{fake.word().capitalize()} Project",  # Random project name
            description=fake.paragraph(),  # Random description
            github_url=f"https://github.com/{fake.user_name()}/{fake.word()}",  # Random GitHub URL
            track=fake.random_element(elements=["Web", "Data Science", "DevOps"]),  # Random track
            cohort=random.choice(cohorts).name,  # Assign project to a random cohort
            owner_id=random.choice(users).id  # Randomly select an owner from created users
        )
        db.session.add(project)  # Add project to the session
        projects.append(project)  # Append project to list for later reference
    db.session.commit()  # Commit all project records to the database

    
    # Seed Project Members

    for _ in range(NUM_PROJECT_MEMBERS):
        project_member = ProjectMember(
            project_id=random.choice(projects).id,  # Randomly assign a project
            user_id=random.choice(users).id,  # Randomly assign a user
            role=fake.random_element(elements=["Developer", "Lead", "Reviewer"]),  # Random role
            joined_at=fake.date_this_year()  # Random join date within the current year
        )
        db.session.add(project_member)  # Add project member to the session
    db.session.commit()  # Commit all project member records to the database

print("Group 5, seeding complete!")
