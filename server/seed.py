from faker import Faker
from models import db, User
from app import app
import random



# Initialize Faker instance for generating random data
fake = Faker()

# Constants defining the number of records to create for each model
NUM_USERS = 10


# Clear existing data and create fresh tables
with app.app_context():
    # Drop all existing tables and recreate them
    db.drop_all()
    db.create_all()
    
    
     # Seed Users
   
    users = []  # List to keep track of created user instances
    for _ in range(NUM_USERS):
        user = User(
            username=fake.name(),  # Random user name
            email=fake.unique.email(),  # Unique random email
            password=fake.password(length=10),  # Random password with specified length
            role=fake.random_element(elements=["student", "admin"]),  # Random role, either student or admin
            # cohort=random.choice(cohorts).name,  # Assign user to a random cohort
            is_admin = fake.random_element(elements=["false", "true"]),
            created_at = fake.date_this_decade()
        )
        db.session.add(user)  # Add user to the session
        users.append(user)  # Append user to list for later reference
    db.session.commit()  # Commit all user records to the database