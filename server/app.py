#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv()

from flask import request, make_response, session, Flask
from flask_migrate import Migrate
from flask_restful import Resource,Api
from flask_cors import CORS
from flask_mail import Mail

from models import User,Project,Cohort, ProjectMember, db,bcrypt
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db') 
                                    # ☝️ Takes care of both Postgres and sqlite databases
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.json.compact = False

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your_email@example.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your_email_password')

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)
bcrypt.init_app(app)
api = Api(app)
mail = Mail(app)


# Home page....................................................................
class Home(Resource):
     
     def get(self):
          
          return {
               "message": " 🗂️ Welcome to the Project Tracker API 🗂️"
          },200

api.add_resource(Home, '/')


# Authentication process.......................................................
# Signing up
class Signup(Resource):
    
    def post(self):

        username  = request.get_json().get('username')
        password = request.get_json().get('password')

        if not username or not password:
            return {'error':'Username and password required'},400
        
        # checking if username exits
        existing_user =User.query.filter_by(username=username).first()
        if existing_user:
            return {'error':'Username already taken'},409
        
        # Creating new user
        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        return {'message':'User created successfully'},201
        
api.add_resource(Signup, '/signup', endpoint='signup')


# Staying logged in
class CheckSession(Resource):

    def get(self):

        if 'user_id' in session:
            user = User.query.get(session['user_id'])

            if user:
                return {'message': 'User authenticated'}, 200
        return {}, 401

    

api.add_resource(CheckSession, '/check_session', endpoint='checks_session')


# Logging in
class Login(Resource):
        
        def post(self):
     
            username = request.get_json().get('username')
            password = request.get_json().get('password')

            user = User.query.filter(User.username == username).first()

            if not user or not user.check_password(password):
                return {'error':'Invalid credentials'},401
            
            session['user_id'] = user.id
            return {'message': 'Logged in successfully'},200
        
        
api.add_resource(Login, '/login', endpoint='login')

# Logging out
class Logout(Resource):
    
    def delete(self):

       session.pop('user_id', None)
       return {}, 204
    
api.add_resource(Logout,'/logout', endpoint='logout')

# ..............................................................................
# C.R.U.D actions for each model

#User
class Users(Resource):

    # fetching all the users
    def get(self):

        try: 
            page = int(request.args.get('page',1)) #defaults to page number 1
            per_page = int(request.args.get('per_page',10)) #defaults to listing 10 users per page

            # Limit maximum users per page
            per_page = min(per_page,100)

            # sorting the users in ascending order
            users_query = User.query.order_by(User.id.asc())

            # calculates the number of user records in the database
            total_users = users_query.count()

            # fetches users with pagination
            users_paginated = User.query.paginate(page=page, per_page=per_page)

            users_list = []
            for user in users_paginated.items:
                user_dict = {
                    "username":user.username,
                    "email":user.email,
                    "is_admin":user.is_admin,
                }
                users_list.append(user_dict)



            pagination_metadata = {
                "total":total_users,
                "pages":users_paginated.pages,
                "page":users_paginated.page,
                "per_page":users_paginated.per_page,
                "has_next":users_paginated.has_next,
                "has_prev":users_paginated.has_prev
            }

            return make_response({
                "users":users_list,
                "pagination":pagination_metadata
            },200)

        except ValueError:
            return make_response({"error":"Invalid page or per_page parameter"},400)

  
api.add_resource(Users, '/users')


# User by ID
class UserByID(Resource):

    # Fetching a user by id
    def get(self,id):
        user = User.query.filter(User.id == id).first()

        if user:
            return make_response(user.to_dict(),200)
        return make_response({"error":"User not found"},404)

    # Updating a user using their id
    def patch(self,id):
        
        user = User.query.filter(User.id == id).first()

        data = request.get_json()

        if user:
            
            try:
                for attr in data:
                    setattr(user, attr, data[attr])

                    db.session.add(user)
                    db.session.commit()

                    user_dict = {
                        "username":user.username,
                        "email":user.email,
                        "password":user.password,
                        "is_admin":user.is_admin,
                    }

                    response = make_response(user_dict,200)

                    return response
                
            except ValueError:
                return make_response({"errors": ["validation errors"]},400)
        
        # error response when the user is not found
        return make_response({"error": "User not found"},404)


    # Deleting a user by their ID
    def delete(self,id):

        user =  User.query.filter(User.id == id).first()

        if not user:
            return make_response({"error":"User not found"},404)

        db.session.delete(user)
        db.session.commit()

        response_dict = {"Message": "User successfully deleted"}

        return make_response(response_dict,200)
        
api.add_resource(UserByID, '/user/<int:id>')  



# CRUD FOR PROJECT MODEL

class Projects(Resource):
    
    # Fetching all projects
    def get(self):

        try:

            page = int(request.args.get('page',1))
            per_page = int(request.args.get('per_page',10))

            per_page = min(per_page,100)

            projects_query = Project.query.order_by(Project.id.asc())

            total_projects = projects_query.count()

            projects_paginated = Project.query.paginate(page=page, per_page=per_page)

            projects_list = []

            for project in projects_paginated.items:
                project_dict = {
                    "name":project.name,
                    "descrition":project.description,
                    "github_url":project.github_url,
                    "type":project.type,
                    "cohort_id":project.cohort_id,
                    "members":project.member.name
                }
                projects_list.append(project_dict)

            pagination_metadata = {
                "total":total_projects,
                "pages":projects_paginated.pages,
                "page":projects_paginated.page,
                "per_page":projects_paginated.per_page,
                "has_next":projects_paginated.has_next,
                "has_prev":projects_paginated.has_prev
            }    

            return make_response({
                "projects":projects_list,
                "pagination":pagination_metadata
            },200)
        
        except  ValueError:
            return make_response({"error":"Invalid page or per_page parameter"},400)

    
    # Creating a project
    def post(self):
        try:
            data = request.get_json()
            new_project = Project(
                name=data['name'],
                description=data['description'],
                github_url=data['github_url'],
                type = data['type'],
                track = data['track'],
                cohort_id = data['cohort_id'],
                # created_at=data['created_at'],
            )
            db.session.add(new_project)
            db.session.commit()
            return make_response(new_project.to_dict(), 200)
        except:
            return make_response({"error": "Invalid data"}, 400)
        
api.add_resource(Projects, '/projects')

class ProjectById(Resource):
    
    # Fetching a project by id
    def get(self, id):
        project = Project.query.filter_by(id=id).first()
        if project:
            return make_response(project.to_dict(), 200)
        else:
            return make_response({"error": "Project not found"}, 404)
        
    # Deleting a project
    def delete(self, id):
        project = Project.query.filter_by(id=id).first()
        if project:
            db.session.delete(project)
            db.session.commit()
            return make_response({"Message": "Project Deleted Successfully"}, 200)
        else:
            return make_response({"error": "Project not found"}, 404)
        
    # Updating a project
    def patch(self, id):
        project = Project.query.filter_by(id=id).first()
        
        data = request.get_json()
        
        if project:
            try:
                for attr in data:
                    setattr(project, attr, data[attr])
                    
                    db.session.add(project)
                    db.session.commit()
                    
                    return make_response(project.to_dict(), 200)
            except ValueError:
                return make_response({"errors": ["validation errors"]}, 400)
        else:
            return make_response({"error": "Project not found"}, 404)

api.add_resource(ProjectById, '/projects/<int:id>')


# Cohort
class Cohorts(Resource):

    # fetching all the cohorts in pages
    def get(self):
         
         try:
            # setting default page and cohort listing per page
             page = int(request.args.get('page',1))
             per_page = int(request.args.get('per_page',10))

             per_page = min(per_page, 100)

             cohorts_query = Cohort.query.order_by(Cohort.id.asc())

             total_cohorts = cohorts_query.count()

             cohorts_paginated = Cohort.query.paginate(page=page, per_page=per_page)

             cohorts_list = []
             for cohort in cohorts_paginated.items:
                 cohort_dict = {
                     "name":cohort.name,
                     "description":cohort.description,
                     "type":cohort.type,
                 }

             pagination_metadata = {
                "total": total_cohorts,
                "pages": cohorts_paginated.pages,
                "page":cohorts_paginated.page,
                "per_page":cohorts_paginated.per_page,
                "has_next":cohorts_paginated.has_next,
                "has_prev":cohorts_paginated.has_prev
             }
             
             return make_response({
                "cohorts":cohorts_list,
                "pagination":pagination_metadata
            },200) 
         
         except ValueError:
             return make_response({"error":"Invalid page or per_page parameter"},400)
         
        #  Adding new cohorts
    def post(self):
           
        try:
            data = request.get_json()

            new_cohort = Cohort(
                name=data['name'],
                description = data['description'],
                type = data['type'],

            )

            db.session.add(new_cohort)
            db.session.commit()

            return make_response(new_cohort.to_dict(),201)
        
        except:
            return make_response({"errors":["validation errors"]}),403

api.add_resource(Cohorts, '/cohorts')   

# cohort by ID
class CohortByID(Resource):

    # Fetching a cohort by ID
    def get(self,id):

        cohort = Cohort.query.filter(Cohort.id == id).first()

        if cohort:
            return make_response(cohort.to_dict(),200)
        return make_response({"error": "Cohort not found"},404)

    # Updating user by ID
    def patch(self,id):
        
        cohort = Cohort.query.filter(Cohort.id == id).first()

        data = request.get_json()

        if cohort:

            try: 
                for attr in data:
                    setattr(cohort,attr,data[attr])

                    db.session.add(cohort)
                    db.session.commit()

                cohort_dict = {
                    "name":cohort.name,
                    "description":cohort.description,
                    "track":cohort.track,
                }  

                response = make_response(cohort_dict,200)

                return response  
            
            except ValueError:
                return make_response({"errors":["validation errors"]},400)
            
        return make_response({"error": "Cohort not found"},404)
 
    # Deleting a cohort by their ID
    def delete(self,id):
        
        cohort = Cohort.query.filter(Cohort.id == id).first()

        if not cohort:
            return make_response({"error": "Cohort not found"},404)
        
        db.session.delete(cohort)
        db.session.commit()

        response_dict = {"Message": "Cohort successfully deleted"}

        return make_response(response_dict,200)
    

api.add_resource(CohortByID, '/cohorts/<int:id>')   


# Project Members CRUD
class ProjectMembers(Resource):

    def get(self):

        try:
        
            page = int(request.args.get('page',1))
            per_page = int(request.args.get('page_page',10))

            per_page = min(per_page,100)

            project_members_query = ProjectMember.query.order_by(ProjectMember.id.asc())

            total_project_members = project_members_query.count()

            project_members_paginated = ProjectMember.query.paginate(page=page, per_page=per_page)

            project_members_list = []
            for project_member in project_members_paginated.items:
                project_member_dict = {
                    "name":project_member.name,
                    "role":project_member.role,
                    "project_id":project_member.project_id,
                    "cohort_id":project_member.cohort_id,
                    # "cohort":project_member.cohort.name,
                    # "project":project_member.cohort.name,
                }
                project_members_list.append(project_member_dict)

            pagination_metadata = {
                "total":total_project_members,
                "pages":project_members_paginated.pages,
                "page":project_members_paginated.page,
                "per_page":project_members_paginated.per_page,
                "has_next":project_members_paginated.has_next,
                "has_prev":project_members_paginated.has_prev
            }   

            return make_response({
                "project_members":project_members_list,
                "pagination":pagination_metadata
            },200) 
    
        except ValueError:
             return make_response({"error":"Invalid page or per_page parameter"},400)

    
    def post(self):
        
        try:
            data = request.get_json()

            new_project_member = ProjectMember(
                name = data['name'],
                role = data['role'],
                cohort_id = data['cohort_id'],
                project_id = data['project_id']

            )
            db.session.add(new_project_member)
            db.session.commit()

            return make_response(new_project_member.to_dict(),201)
        
        except:
            return make_response({"errors":["validation errors"]}),403

api.add_resource(ProjectMembers, '/projectmembers')



class ProjectMemberById(Resource):

    pass



if __name__ == '__main__':
    app.run(port=5555, debug=True)