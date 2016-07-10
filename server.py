from flask import Flask, request
import json
import aco
import maps

app = Flask('Transyt')

# constants
iterationCount = 10

@app.route('/')
def index():
    return "this is where the maps page should render"

@app.route('/compute_routes.json', methods=['GET'])
def computeRoutes():
    error = None
    addresses = json.loads(request.args.get('addresses'))
    locationsList = list(map(maps.addressToLatLngTuple, addresses))
    locationTuples = list(map(lambda x: [x.latitude, x.longitude], locationsList))
    routeSolver = aco.RouteSolver(locationTuples)

    (distances, routes) = routeSolver.solveRandomly(iterationCount)
    indices = list(range(len(routes)))
    sortedIndices = sorted(indices, key = lambda x: distances[x])
    sortedRoutes = []
    for index in sortedIndices:
        sortedRoutes.append(routes[index])
    sortedRenderedRoutes = map(routeSolver.renderRoute, sortedRoutes)
    ret = {
        "path": list(sortedRenderedRoutes),
        "points": locationTuples,
    }
    return json.dumps(ret)

if __name__ == '__main__':
    app.run(port=2000, debug=True)
