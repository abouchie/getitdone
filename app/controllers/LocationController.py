from app.controllers.BaseController import BaseController
from flask import render_template, jsonify, request, make_response, session

import json

class LocationController(BaseController):
    def __init__(self):
        super().__init__()

    def save_errand_locations(self, request):
        data = request.form
        session['errands'] = [data['errand_{}'.format(idx)] for idx in range(0, len(data))]
        return make_response(render_template('set-trip-type.html'))

    def find_locations(self, request):
        bad_result = False

        session['errands'] = self.get_errands(session['errands'])
        session['origin'] = self.get_location(request.form['origin'])
        session['destination'] = self.get_location(request.form['destination'])

        results = {
            'origin': session['origin'],
            'destination': session['destination'],
            'errands': session['errands']
        }
        bad_result = self._contains_bad_result(results)

        return self._build_location_response(bad_result, results)


    def get_errands(self, locations):
        results = []
        index = 0
        for location in locations:
            found = self.get_location(location)
            found['errand_index'] = index
            results.append(found)
            index += 1
        return results


    def _contains_bad_result(self, results):
        for errand in results['errands']:
            if self._is_bad_result(errand):
                return True
        
        if self._is_bad_result(results['origin']):
            return True
        else:
            return self._is_bad_result(results['destination'])

    def _is_bad_result(self, result):
        return result['status'] == 'MULTIPLE' or result['status'] == 'EMPTY'

    def get_location(self, location):
        response = self.api.places(query=location, language='en-US')
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
        
        result['original_search_query'] = location

        return result

    def refine_locations(self, request):
        bad_result = False
        data = request.form
        results = { 'errands': [] }

        for key in data:
            if key == 'origin':
                session['origin'] = self.get_location(request.form[key])
            elif key == 'destination':
                session['destination'] = self.get_location(request.form[key])
            else: # key == 'errand_#'
                print(key)
                result = self.get_location(data[key])
                index = int(key[-1]) # grabs last char from 'errand_#'
                result['errand_index'] = index
                session['errands'][index] = result

        results = {
            'origin': session['origin'],
            'destination': session['destination'],
            'errands': session['errands']
        }
        bad_result = self._contains_bad_result(results)

        return self._build_location_response(bad_result, results)

    def _build_location_response(self, bad_result, results):
        if bad_result:
            return make_response(render_template('bad-locations.html', locations=results))
        else:
            return make_response(render_template('locations.html', locations=results))

