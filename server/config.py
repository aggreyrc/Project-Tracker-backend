#!/usr/bin/env python3

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db') 
 # ☝️ Takes care of both Postgres and sqlite databases
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'|\xab_\xac<\xcb\xe2\xc8~\x110\x82\xeb\xfa\xc8~'
app.json.compact = False


db = SQLAlchemy()
api = Api(app)
CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)