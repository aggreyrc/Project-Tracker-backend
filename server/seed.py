from config import create_app, db  # Import create_app from config
from models import User, Project, Cohort, ProjectMember
from datetime import datetime
from faker import Faker

# Initialize Faker
fake = Faker()

def clear_tables():
    db.session.query(User).delete()
    db.session.query(Cohort).delete()
    db.session.query(Project).delete()
    db.session.query(ProjectMember).delete()
    db.session.commit()
    print("Tables cleared!")

def seed_users():
    # Create sample users
    users = [
        User(username="admin_user", email="admin@example.com", password="adminpass", is_admin=True, role="admin"),
        User(username="student_user", email="student@example.com", password="studentpass", is_admin=False, role="student")
    ]
    
    # Keep track of existing emails (for the initial two users)
    existing_emails = {user.email for user in users}
    
    # Add the predefined users to the database
    db.session.bulk_save_objects(users)

    # Generate additional random users using Faker
    new_users = []
    for _ in range(8):  # Generates 8 additional users
        username = fake.user_name()
        email = fake.email()

        # Ensure unique email by checking the existing_emails set
        while email in existing_emails:
            email = fake.email()  # Keep generating until a unique one is found
        
        existing_emails.add(email)  # Add to the set after ensuring it's unique
        password = fake.password()
        is_admin = fake.boolean(chance_of_getting_true=20)  # 20% chance to be admin
        role = "admin" if is_admin else "student"

        new_user = User(username=username, email=email, password=password, is_admin=is_admin, role=role)
        new_users.append(new_user)

    db.session.bulk_save_objects(new_users)
    db.session.commit()
    print("Users seeded!")

def seed_cohorts():
    # Create sample cohorts
    cohorts = [
        Cohort(name="Web Development Cohort", description="A cohort focused on web development.", github_url="https://github.com/webdev-cohort", type="Full-Time", start_date=datetime(2024, 1, 15), end_date=datetime(2024, 6, 15)),
        Cohort(name="Data Science Cohort", description="A cohort for data science enthusiasts.", github_url="https://github.com/datasci-cohort", type="Part-Time", start_date=datetime(2024, 2, 1), end_date=datetime(2024, 7, 1))
    ]
    
    # Generate additional random cohorts using Faker
    new_cohorts = []
    for _ in range(3):  # Generates 3 additional cohorts
        name = fake.bs().title()
        description = fake.paragraph()
        github_url = fake.url()
        cohort_type = fake.random_element(["Full-Time", "Part-Time"])
        start_date = fake.date_this_year(before_today=True)
        end_date = fake.date_this_year(after_today=True)

        # Check if the cohort name already exists
        if not Cohort.query.filter_by(name=name).first():
            cohort = Cohort(name=name, description=description, github_url=github_url, type=cohort_type, start_date=start_date, end_date=end_date)
            new_cohorts.append(cohort)
        else:
            print(f"Skipping cohort with existing name: {name}")
    
    db.session.bulk_save_objects(new_cohorts)
    db.session.commit()
    print("Cohorts seeded!")

def seed_projects():
    # Create sample projects
    projects = [
        Project(name="Web Application", description="A full-stack web application.", github_url="https://github.com/webapp", type="Full-Stack", track="Web Development", cohort_id=1),
        Project(name="Machine Learning Model", description="A machine learning model for prediction.", github_url="https://github.com/mlmodel", type="Data Science", track="Data Science", cohort_id=2)
    ]
    
    # Generate additional random projects using Faker
    new_projects = []
    for _ in range(5):  # Generates 5 additional projects
        name = fake.bs().title()
        description = fake.paragraph()
        github_url = fake.url()
        project_type = fake.random_element(["Full-Stack", "Data Science", "Web Development"])
        track = fake.random_element(["Web Development", "Data Science", "Machine Learning"])
        cohort_id = fake.random_int(min=1, max=2)  # Randomly assigns to one of the cohorts

        # Check if the project name already exists
        if not Project.query.filter_by(name=name).first():
            project = Project(name=name, description=description, github_url=github_url, type=project_type, track=track, cohort_id=cohort_id)
            new_projects.append(project)
        else:
            print(f"Skipping project with existing name: {name}")
    
    db.session.bulk_save_objects(new_projects)
    db.session.commit()
    print("Projects seeded!")

def seed_project_members():
    # Create sample project members (joining users to projects)
    project_members = [
        ProjectMember(project_id=1, cohort_id=1, role="Developer"),
        ProjectMember(project_id=1, cohort_id=1, role="Lead"),
        ProjectMember(project_id=2, cohort_id=2, role="Data Scientist"),
        ProjectMember(project_id=2, cohort_id=2, role="Researcher")
    ]
    
    # Generate additional random project members using Faker
    new_members = []
    for _ in range(6):  # Generates 6 additional project members
        project_id = fake.random_int(min=1, max=5)  # Randomly assigns to one of the projects
        cohort_id = fake.random_int(min=1, max=2)  # Randomly assigns to one of the cohorts
        role = fake.random_element(["Developer", "Researcher", "Lead", "Data Scientist", "Tester"])

        member = ProjectMember(project_id=project_id, cohort_id=cohort_id, role=role)
        new_members.append(member)
    
    db.session.bulk_save_objects(new_members)
    db.session.commit()
    print("Project members seeded!")

def run_seed():
    # Use app context to run the seed functions
    app = create_app()  # Create the app instance
    with app.app_context():
        clear_tables()
        seed_users()
        seed_cohorts()
        seed_projects()
        seed_project_members()
        print("Database seeded successfully!")

if __name__ == "__main__":
    run_seed()
