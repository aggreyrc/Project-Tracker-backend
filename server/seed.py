# from config import db, bcrypt, app  # Import the app from your config file
from models import User, Project, Cohort, ProjectMember,db,bcrypt
from datetime import datetime, timedelta,timezone
from app import app


def seed_data():
    # Creating the application context
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Creating sample users
        print('\nADDING USERS...')
        admin_user = User(
            username="Isaac Odhiambo",
            email="odhiamboisaac@gmail.com",
            password_hash=bcrypt.generate_password_hash("admin123").decode('utf-8'),
            is_admin=True,
            is_verified=True, # Set as verified for admin access
            role="admin"
        )

        student_user = User(
            username="Odiwuor Jakababa",
            email="odiwuorisaach@gmail.com",
            password_hash=bcrypt.generate_password_hash("student123").decode('utf-8'),
            is_admin=False,
            is_verified=True,  # Set as verified for normal student
            role="student"
        )

        # Adding users to the session
        db.session.add(admin_user)
        db.session.add(student_user)
        db.session.commit()

        # Debugging verification code
        print('\nDebugging user code...')
        admin_verification_code = admin_user.generate_verification_code()
        print(admin_verification_code)

        student_verification_code = student_user.generate_verification_code()
        print(student_verification_code)


        # Creating sample cohorts
        print('\nADDING COHORTS...')
        cohort1 = Cohort(
            name="Cohort 2024",
            description="This is the 2024 cohort.",
            github_url="https://github.com/example/cohort2024",
            type="Full Stack Development",
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31)
        )

        cohort2 = Cohort(
            name="Cohort 2025",
            description="This is the 2025 cohort.",
            github_url="https://github.com/example/cohort2025",
            type="Data Science",
            start_date=datetime(2025, 1, 1),
            end_date=datetime(2025, 12, 31)
        )

        # Adding cohorts to the session
        db.session.add(cohort1)
        db.session.add(cohort2)
        db.session.commit()

        # Creating sample projects with image URLs
        print('\nADDING PROJECTS..')
        project1 = Project(
            name="Project Alpha",
            description="This is the Alpha project for cohort 2024.",
            github_url="https://github.com/example/projectalpha",
            type="Web Development",
            cohort_id=cohort1.id,
            created_at=datetime.now(timezone.utc),
            image_url="https://example.com/images/project_alpha.png",
            user_id=1,
        


        )

        project2 = Project(
            name="Project Beta",
            description="This is the Beta project for cohort 2025.",
            github_url="https://github.com/example/projectbeta",
            type="Machine Learning",
            cohort_id=cohort2.id,
            created_at=datetime.now(timezone.utc),
            image_url="https://example.com/images/project_beta.png",
            user_id=2,
            
        )

        # Adding projects to the session
        db.session.add(project1)
        db.session.add(project2)
        db.session.commit()

        # Creating sample project members
        print('\nADDING PROJECT MEMBERS...')
        project_member1 = ProjectMember(
            name="Monalisa Sabina",
            project_id=project1.id,
            user_id=admin_user.id,  # Assuming admin is part of this project
            role="Team Lead",
            joined_at=datetime.now(timezone.utc)
        )

        project_member2 = ProjectMember(
            name="Vitalis",
            project_id=project1.id,
            user_id=student_user.id,
            role="Developer",
            joined_at=datetime.now(timezone.utc)
        )

        project_member3 = ProjectMember(
            name="Aggey",
            project_id=project2.id,
            user_id=student_user.id,
            role="Data Scientist",
            joined_at=datetime.now(timezone.utc) + timedelta(days=1)
        )

        # Adding project members to the session
        db.session.add(project_member1)
        db.session.add(project_member2)
        db.session.add(project_member3)
        db.session.commit()


        print('\nTESTING')
        print('Getting Users')
        users_list = User.query.all()
        print(users_list)

        print('\nGetting projects')
        projects_list = Project.query.all()
        print(projects_list)

        print('\nGetting cohorts')
        cohorts_list = Cohort.query.all()
        print(cohorts_list)

        print('\nGetting project members')
        project_members_list = ProjectMember.query.all()
        print(project_members_list)
      

        print("\nSeeding completed successfully!")




if __name__ == "__main__":
    seed_data()
