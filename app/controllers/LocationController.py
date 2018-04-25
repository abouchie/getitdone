from app.controllers.BaseController import BaseController
from flask import render_template, jsonify, request, make_response, session

import json

class LocationController(BaseController):
    def __init__(self):
        super().__init__()

    def find_locations(self, request):
        bad_result = False
        data = request.form
        locations = [data['errand{}'.format(idx)] for idx in range(0, len(data))]

        results = []
        idx = 0
        for location in locations:
            result = self.get_location(location)

            if result['status'] == 'MULTIPLE' or result['status'] == 'EMPTY':
                bad_result = True

            result['original_search_query'] = location
            result['stop-key'] = 'stop{}'.format(idx)
            session['stop{}'.format(idx)] = result
            results.append(result)
            idx += 1

        if bad_result:
            response = make_response(render_template('bad-locations.html', locations=results))
        else:
            response = make_response(render_template('locations.html', locations=results))
        
        return response

    def get_location(self, location):
        response = self.api.places(query=location, language='en-US')
        print(response)

        result = {}
        if response["status"] == "OK":
            if(len(response['results']) > 1):
                result = {
                    'status': 'MULTIPLE',
                    'results': response["results"]
                }
            else:
                result = response["results"][0]
                result['status'] = 'OK'

        else:
            result['status'] = 'EMPTY'
                
        return result

    def refine_locations(self, request):
        pass
        # take refined results and get_location again

        # if all good, update session storage
        # then get start/end location
