from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize extensions
db = SQLAlchemy()
api = Api()
bcrypt = Bcrypt()

def create_app():
    # Load environment variables
    load_dotenv()

    # Initialize Flask app
    app = Flask(__name__)

    # App configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # Handle both PostgreSQL and SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = b'|\xab_\xac<\xcb\xe2\xc8~\x110\x82\xeb\xfa\xc8~'
    app.json.compact = False

    # Initialize extensions with app context
    db.init_app(app)
    api.init_app(app)
    CORS(app)
    bcrypt.init_app(app)

    # Setup Flask-Migrate
    migrate = Migrate(app, db)

    return app
