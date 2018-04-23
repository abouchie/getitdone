from app.controllers.BaseController import BaseController
from flask import render_template, jsonify, request, make_response, session

import json

class LocationController(BaseController):
    def __init__(self):
        super().__init__()

    def find_locations(self, request):
        data = request.form
        locations = [data['errand{}'.format(idx)] for idx in range(0, len(data))]

        results = []
        for location in locations:
            result = self._validate(location)
            if(type(result) == type([])):
                for options in result:
                    option['original_search_query'] = location
            else:
                result['original_search_query'] = location
            results.append(result)  
        
        session['locations'] = json.dumps(results)
        return make_response(render_template('locations.html', locations=results))

    def _validate(self, location):
        response = self.api.places(query=location, language='en-US')

        results = {}
        if(response["status"] == "OK"):
            if(len(response['results']) == 1):
                results = response["results"][0]
            else:
                # return array of options (first page only)
                results = response["results"]
        
        return results
