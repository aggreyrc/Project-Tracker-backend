from faker import Faker
from datetime import datetime, timedelta, timezone
import random
from models import User, Project, Cohort, ProjectMember,db,bcrypt
from app import app

def seed_data():
    # Initialize Faker
    fake = Faker()

    # Creating the application context
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        

        # Create users
        print('\nADDING USERS...')
        admin_created = False  # Flag to track if an admin has been created
        total_users = 20  # Total number of users to create

        for _ in range(total_users):
            username = fake.user_name()
            email = f"{username.lower()}@example.com"
            password_hash = bcrypt.generate_password_hash("password123").decode('utf-8')
    
            # Ensure at least one admin user is created
            is_admin = True if not admin_created else random.choice([True, False])
            if is_admin:
                admin_created = True  # Mark that an admin has been created
    
            # Create the user
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                is_admin=is_admin,
                is_verified=True
            )
    
            # Assign role
            user.role = "admin" if user.is_admin else "student"
    
            db.session.add(user)

        #  Commit the users to the database after the loop to avoid committing multiple times
        db.session.commit()
 
      
        
        # Create cohorts
        print('\nADDING COHORTS...')
        cohorts = []
        for _ in range(8):
            cohort_name = fake.company()
            github_url = f"https://github.com/example/{cohort_name.lower().replace(' ', '-')}"
            start_date = datetime.now(timezone.utc) - timedelta(days=random.randint(365*2, 365*5))
            end_date = start_date + timedelta(days=random.randint(365, 365*2))
            cohort = Cohort(
                name=cohort_name,
                description=fake.text(),
                github_url=github_url,
                type=fake.random_element(elements=("Full Stack Development", "Data Science")),
                start_date=start_date,
                end_date=end_date
            )
            db.session.add(cohort)
            cohorts.append(cohort)
        db.session.commit()    
        
        # Create projects
        print('\nADDING PROJECTS...')
        projects =[]
        project_types = ["Web Development", "Mobile App", "Machine Learning"]
        
        for cohort in cohorts[:15]:  # Only create 15 projects
            project_name = fake.company()
            project_description = fake.text()
            project_type = random.choice(project_types)

            project = Project(
                name=project_name,
                description=project_description,
                github_url=f"https://github.com/example/{cohort.name.lower().replace(' ', '-')}/{project_name.lower().replace(' ', '-')}",
                type=project_type,
                cohort_id=cohort.id,
                created_at=datetime.now(timezone.utc),
                image_url=f"https://example.com/images/{project_name.lower()}.png",
                user_id=random.choice([u.id for u in User.query.all()])
            )
            db.session.add(project)
            projects.append(project)
        db.session.commit()    
        
        # Create project members
        print('\nADDING PROJECT MEMBERS...')
        users = User.query.all()

        for project in projects:  # Assuming projects is a list of created projects
           for _ in range(3):  # Add 3 members to each project (adjust number as needed)
               user = random.choice(users)  # Select a random user from the list of users
               member_name = fake.name()
               member_role = fake.job()

               # Create a new project member
               project_member = ProjectMember(
                    name=member_name,
                    project_id=project.id,  # Link to the project
                    joined_at=datetime.now(timezone.utc),
                    role=member_role,
                    user_id=user.id,  # Make sure to assign a valid user_id
                    cohort_id=random.choice(cohorts).id  # Assign a random cohort if needed
               )

               db.session.add(project_member)

          # Commit project members to the database
        db.session.commit()
    

        # Debugging verification code
        admin_user = User.query.filter_by(is_admin=True).first()
        student_user = User.query.filter_by(is_admin=False).first()

        print('\nDebugging user code...')
        # Check if admin_user exists before trying to access its method
        if admin_user:
            print(admin_user.generate_verification_code())
        else:
            print("Admin user not found!")

        # Check if student_user exists before trying to access its method
        if student_user:
            print(student_user.generate_verification_code())
        else:
            print("Student user not found!")

        print("\nSeeding completed successfully!")

if __name__ == "__main__":
    seed_data()
