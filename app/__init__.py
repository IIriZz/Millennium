# -*- coding: utf-8 -*-
# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vb3?Jfb38%&3n3MN3UBc39N3N$9n3?8n'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/data_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app, manage_session=False)
ROOMS = ['Lounge', 'Coding', 'Glorg', 'herjfkipajrgiuejope']


db.create_all()


from .routes import *
