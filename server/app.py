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

        users_list=[]
        for user in User.query.all():
            user_dict = {
                "username":user.username,
                "email":user.email,
                "is_admin":user.is_admin,
            }
            users_list.append(user_dict)

        return make_response(users_list,200)
    
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

class UserByID(Resource):

    # Fetching a user by id
    def get(self,id):
        user = User.query.filter(User.id == id).first()

        if user:
            return make_response(user.to_dict(),200)
        return make_response({"error":"User not found"},404)

    # Updating a user using the user's id
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
                    }

                    response = make_response(user_dict,200)

                    return response
                
            except ValueError:
                return make_response({"errors": ["validation errors"]},400)
        
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

if __name__ == '__main__':
    app.run(port=5555, debug=True)