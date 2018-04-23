from flask import Flask, session
from flask.ext.session import Session

import googlemaps
import os

print("Creating app")
app = Flask(__name__)
gmaps = googlemaps.Client(key=os.getenv("API_KEY", "no key provided"))

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'super secret key'
Session(app)

#app.config.from_object('config')

# import controllers to register routes
from app.controllers import Router