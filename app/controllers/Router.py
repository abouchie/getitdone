from flask import request, session

from app import app
from app.controllers.HomeController import HomeController
from app.controllers.LocationController import LocationController
from app.controllers.DirectionController import DirectionController

controllers = {
    'home': HomeController(),
    'location': LocationController(),
    'direction': DirectionController()
}

'''
    this should check for login status and redirect to login page if not logged in
    otherwise redirect to location entry page
'''
@app.route("/")
def index():
    return controllers['home'].index()

@app.route("/save-errand-locations", methods=["POST"])
def save_errand_locations():
    return controllers['location'].save_errand_locations(request)

@app.route("/find-locations", methods=["POST"])
def find_locations():
    return controllers['location'].find_locations(request)

@app.route("/refine-locations", methods=["POST"])
def refine_locations():
    return controllers['location'].refine_locations(request)

@app.route("/get-directions", methods=["POST"])
def get_directions():
    return controllers['direction'].get_directions(request)
