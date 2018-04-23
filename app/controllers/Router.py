from flask import request

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
    [
        "stop_0" : {
            "name": name
            "address": address
        },
        "stop_1" : {
            "name": name
            "address": address
        },
        ...,
        "stop_N" : {
            "name": name
            "address": address
        }
    ]
'''
@app.route("/get-directions", methods=["POST"])
def get_directions():
    return controllers['direction'].get_directions(request)
