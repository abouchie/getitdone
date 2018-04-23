from app.controllers.BaseController import BaseController
from flask import render_template, jsonify, request, make_response

import json

class LocationController(BaseController):
    def __init__(self):
        super().__init__()

    def find_locations(self, request):
        locations = request.get_json()
        print(locations)

        results = []
        for location in locations:
            result = self._validate(location)
            results.append(result[0]['formatted_address'])
        
        return json.dumps(results)
        #return render_template('errands.html', errands=results)


    def _validate(self, location):
        response = self.api.places(query=location, language='en-US')

        results = {}
        if(response["status"] == "OK"):
            results = response["results"]

            if(len(results) == 1):
                return results
            else:
                pass
                #handle multiple results
        else:
            pass
            #handle error
