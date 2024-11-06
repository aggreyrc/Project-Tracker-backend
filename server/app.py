from dotenv import load_dotenv
load_dotenv()

from flask import Flask,request, make_response, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Projects, Cohort, Project_members, bcrypt
from flask_cors import CORS


app = Flask(__name__)
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

bcrypt=Bcrpt(app)

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

# C.R.U.D

#User
class Users(Resource):

    
    def get(self):

        users_list=[]
        for user in User.query.all():
            user_dict = {
                "name":user.name,
                "email":user.email,
                "role":user.role,
            }
            users_list.append(user_dict)

        return make_response(users_list,200)
    

def post(self):

    try:
        data =  request.get_json()

        new_user = User(
            name = data['name'],
            email = data['email'],
            role = data['role'],
        )

        db.session.add(new_user)
        db.session.commit()

        return make_response(new_user.to_dict(),201)
    
    except:
        make_response({"errors":["validation errors"]}),403




if __name__ == '__main__':
    app.run(port=5555, debug=True)