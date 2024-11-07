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
    cohorts = []
    for _ in range(NUM_COHORTS):
        cohort = Cohort(
            name=f"{fake.word().capitalize()} Cohort",
            description=fake.sentence(),
            github_url=f"https://github.com/{fake.word()}",
            type=fake.random_element(elements=["Web", "Data Science", "DevOps"]),
            start_date=fake.date_this_decade(),
            end_date=fake.date_this_decade()
        )
        db.session.add(cohort)
        cohorts.append(cohort)
    db.session.commit()

    # Seed Users
    users = []
    for _ in range(NUM_USERS):
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            password=bcrypt.generate_password_hash(fake.password(length=10)).decode('utf-8'),
            is_admin=fake.boolean(chance_of_getting_true=30)  # 30% chance the user is admin
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Seed Projects
    projects = []
    for _ in range(NUM_PROJECTS):
        project = Project(
            name=f"{fake.word().capitalize()} Project",
            description=fake.paragraph(),
            github_url=f"https://github.com/{fake.user_name()}/{fake.word()}",
            type=fake.random_element(elements=["Web", "Data Science", "DevOps"]),
            track=fake.random_element(elements=["Frontend", "Backend", "Fullstack"]),
            cohort_id=random.choice(cohorts).id
        )
        db.session.add(project)
        projects.append(project)
    db.session.commit()

    # Seed Project Members
    for _ in range(NUM_PROJECT_MEMBERS):
        project_member = ProjectMember(
            project_id=random.choice(projects).id,
            cohort_id=random.choice(cohorts).id,
            role=fake.random_element(elements=["Developer", "Lead", "Reviewer"]),
            joined_at=fake.date_this_year()
        )
        db.session.add(project_member)
    db.session.commit()

print("Group 5, seeding complete!")
