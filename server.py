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
    destination = request.args.get('destination')
    locationsList = list(map(maps.addressToLatLngTuple, addresses))
    locationTuples = list(map(lambda x: [x.latitude, x.longitude], locationsList))
    destinationLatLng = maps.addressToLatLngTuple(destination)
    routeSolver = aco.RouteSolver(locationTuples, [destinationLatLng.latitude,
                                                   destinationLatLng.longitude])

    (distances, routes, bestDistance) = routeSolver.solveRandomly(iterationCount)
    indices = list(range(len(routes)))
    sortedIndices = sorted(indices, key = lambda x: distances[x])
    sortedRoutes = []
    sortedDistances = []
    for index in sortedIndices:
        sortedRoutes.append(routes[index])
        sortedDistances.append(distances[index])

    sortedRenderedRoutes = map(routeSolver.renderRoute, sortedRoutes)
    destinationTuple = [destinationLatLng.latitude,
                        destinationLatLng.longitude]
    locationTuples.append([destinationLatLng.latitude, destinationLatLng.longitude]);
    ret = {
        "paths": list(sortedRenderedRoutes),
        "points": locationTuples,
        "best_distance": int(bestDistance),
        "naive_distance": int(maps.getTotalNaive(locationTuples)),
    }
    return json.dumps(ret)

if __name__ == '__main__':
    app.run(port=2000, debug=True)
