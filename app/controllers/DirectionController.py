from app.controllers.BaseController import BaseController
from flask import render_template, jsonify, request, make_response, session
from datetime import datetime, timedelta

import sys, itertools, json


class DirectionController(BaseController):
    def __init__(self):
        super().__init__()

    def get_directions(self, request):
        ##### FOR TESTING PURPOSES ####
        stops = session.get('locations')
        stops = json.loads(stops)

        data = {
            'origin': {
                'formatted_address': '126 Park Ave, Hoboken, NJ 07030, USA',
                'name': 'Home'
            },
            'destination': {
                'formatted_address': '126 Park Ave, Hoboken, NJ 07030, USA',
                'name': 'Home'
            },
            'stops': stops
        }
        ##### FOR TESTING PURPOSES ####

        locations = [stop for stop in stops]
        locations.insert(0, data['origin'])
        locations.append(data['destination'])

        distances = self.calculate_shortest_paths(locations)
        route_order, time = self.get_shortest_route_order(stops, distances)
        route = self.build_route(locations, route_order)

        time = str(timedelta(seconds=time))

        session['route'] = json.dumps(route)
        return make_response(render_template('route.html',
                                             route=route,
                                             time=time))
        
    def _get_dist_matrix(self, origins, destinations):
        return self.api.distance_matrix(origins,
                                        destinations,
                                        mode="driving",
                                        language=self.language,
                                        departure_time=datetime.now())

    # returns travel time in seconds
    def _get_dist(self, x, y, matrix):
        result = matrix["rows"][x]["elements"][y]
        return result["duration_in_traffic"]["value"]

    def calculate_shortest_paths(self, locations):
        addresses = [loc['formatted_address'] for loc in locations]
        matrix = self._get_dist_matrix(addresses, addresses)
        sz = len(locations)

        # create 2-d array with edge (x, y) weights
        dist = [[self._get_dist(x, y, matrix) for x in range(sz)] for y in range(sz)]

        for x in range(sz):
            dist[x][x] = 0

        for k in range(sz):
            for i in range(sz):
                for j in range(sz):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

    def calculate_permutations(self, count):
        indices = [x for x in range(1, count + 1)]
        return list(itertools.permutations(indices))

    def _calculate_route(self, indices, distances):
        #indices = random permutation of indices (1 - #stops)
        dist = distances[0][indices[0]] #add dist['start']['stop1']
        for x in range(len(indices) - 1):
            dist += distances[indices[x]][indices[x+1]]
        dist += distances[indices[-1]][-1] # add dist['stopN']['end']
        return dist

    def get_shortest_route_order(self, stops, distances):
        min_dist = sys.maxsize
        perms = self.calculate_permutations(len(stops))
        route_indices = []
        for perm in perms:
            temp_dist = self._calculate_route(perm, distances)
            if temp_dist < min_dist:
                route_indices = perm
                min_dist = temp_dist

        route_indices = list(route_indices)
        # insert 'start' index, append 'end' index
        route_indices.insert(0, 0)
        route_indices.append(len(distances) - 1)
        return route_indices, min_dist

    def build_route(self, locations, indices):
        return [locations[x] for x in indices]
