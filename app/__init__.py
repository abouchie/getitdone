from flask import Flask, session
from flask_sessionstore import Session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import googlemaps, os, uuid

print("Creating app")
app = Flask(__name__)
gmaps = googlemaps.Client(key=os.getenv("API_KEY", "no key provided"))

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = str(uuid.uuid4())
db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
sess = Session(app)
sess.app.session_interface.db.create_all()


from app.models.Users import AnonUser, User
db.create_all()

login_manager = LoginManager()
login_manager.anonymous_user = AnonUser.create
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    print('trying to get user from session')
    if 'user_id' in session:
        return User.from_id(session['user_id'])
    return None

# import controllers to register routes after app config
from app.controllers import Router