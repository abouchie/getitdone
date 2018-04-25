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

@app.route("/")
def index():
    return controllers['home'].index()
    #return render_template("home.html")

'''
    incoming request should be stringify-ed list of locations:
    [ 'location_1', 'location_2', 'location_N']
'''
@app.route("/find-locations", methods=["POST"])
def find_locations():
    return controllers['location'].find_locations(request)

'''
    incoming request should be JSON of following format:
    {
        "origin" : {},
        "destination" : {},
        "stops" : [
            "stop0" : {
                "name": name
                "address": address
            },
            "stop1" : {
                "name": name
                "address": address
            },
            "stopN" : {
                "name": name
                "address": address
            }
        ]
    }
'''

@app.route("/refine-locations", methods=["POST"])
def refine_locations():
    return controllers['location'].refine_locations(request)

@app.route("/get-directions", methods=["POST"])
def get_directions():
    return controllers['direction'].get_directions(request)
