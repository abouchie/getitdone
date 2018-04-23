from flask import Flask
import googlemaps
import os

print("Creating app")
app = Flask(__name__)
gmaps = googlemaps.Client(key=os.getenv("API_KEY", "no key provided"))
#app.config.from_object('config')

# import controllers to register routes
from app.controllers import Router