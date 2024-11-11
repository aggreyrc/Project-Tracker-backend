# #!/usr/bin/env python3

# from dotenv import load_dotenv
# load_dotenv()

# from flask import Flask
# from flask_migrate import Migrate
# from flask_restful import Api
# from flask_cors import CORS
# from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy

# import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db') 
#  # ☝️ Takes care of both Postgres and sqlite databases
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = b'|\xab_\xac<\xcb\xe2\xc8~\x110\x82\xeb\xfa\xc8~'
# app.json.compact = False


# db = SQLAlchemy()
# api = Api(app)
# CORS(app)

# migrate = Migrate(app, db)
# db.init_app(app)

# bcrypt = Bcrypt(app)

from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os

app = Flask(__name__)

# Configure Database URI with fallback for sqlite and correction for postgres URI scheme
uri = os.getenv('DATABASE_URL', 'sqlite:///app.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', b'|\xab_\xac<\xcb\xe2\xc8~\x110\x82\xeb\xfa\xc8~')

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your_email@example.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your_email_password')

# Initialize extensions
db = SQLAlchemy()
api = Api(app)
CORS(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
mail = Mail(app)  # Initialize Mail

# Initialize db with app
db.init_app(app)
