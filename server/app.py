#!/usr/bin/env python3

from flask import request, make_response, session
from flask_restful import Resource
from models import User, Project, Cohort, ProjectMember
from config import app,api,db


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

        username  = request.get_json()['username']
        password = request.get_json()['password']

        if username and password:

            new_user = User(username = username)
            new_user.password_hash = password
        
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            return new_user.to_dict(), 201
        
        return {'error': 'Invalid username and password '},400
        
api.add_resource(Signup, '/signup', endpoint='signup')


# Staying logged in
class CheckSession(Resource):

    def get(self):

        if session.get('user_id'):

            user = User.query.filter(User.id == session['user_id']).first()

            return user.to_dict(),200
        
        return {},204
    

api.add_resource(CheckSession, '/check_session', endpoint='checks_session')


# Logging in
class Login(Resource):
        
        def post(self):
     
            username = request.get_json()['username']
            password = request.get_json()['password']

            user = User.query.filter(User.username == username).first()

            if user.authenticate(password):

                session['user_id'] = user.id
                return user.to_dict(), 200
 
            return {}, 204
        
api.add_resource(Login, '/login', endpoint='login')

# Logging out
class Logout(Resource):
    
    def delete(self):
        session['user_id'] = None
        return{},204
    
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

            # sorting the users in asccending order
            users_query = User.query.order_by(User.id.asc())

            total_users = users_query.count()
            users_paginated = User.query.paginated(page=page, per_page=per_page)

            users_list = []
            for user in users_paginated.item:
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

  
    
    # Adding new users
    def post(self):

        try:
            data =  request.get_json()

            new_user = User(
                username = data['username'],
                email = data['email'],
                is_admin = data.get('is_admin',False),
            )

            db.session.add(new_user)
            db.session.commit()

            return make_response(new_user.to_dict(),201)
    
        except:
            return make_response({"errors":["validation errors"]}),403

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
        projects = Project.query.all()
        projects_list = []
        for project in projects:
            project_dict = {
                "id":project.id,
                "title":project.title,
                "description":project.description,
                "github_url": project.github_url,
                "created_at": project.created_at
            }
        projects_list.append(project_dict)
        return make_response(projects_list,200)
    
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
                created_at=data['created_at'],
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
            

if __name__ == '__main__':
    app.run(port=5555, debug=True)