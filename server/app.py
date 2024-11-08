
import os

from flask import request, make_response, session, Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Resource,Api
# from flask_bcrypt import Bcrypt
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy

from models import User, db



# db = SQLAlchemy()


# bcrypt = Bcrypt()
# cors = CORS()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db') 
 # ☝️ Takes care of both Postgres and sqlite databases
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'|\xab_\xac<\xcb\xe2\xc8~\x110\x82\xeb\xfa\xc8~'
app.json.compact = False

# Initialize extensions with the app
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# migrate.init_app(app, db)
# api.init_app(app)
# bcrypt.init_app(app)
# cors.init_app(app)




# Home page....................................................................
class Home(Resource):
     
     def get(self):
          
          return {
               "message": " 🗂️ Welcome to the Project Tracker API 🗂️"
          },200

api.add_resource(Home, '/')

if __name__ == '__main__':
     port = int(os.environ.get("PORT", 5555))
     app.run(host="0.0.0.0", port=port, debug=True)
