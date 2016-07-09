from flask import Flask, request
import json
import aco

app = Flask('Transyt')

# constants
iterationCount = 10

@app.route('/')
def index():
    return "this is where the maps page should render"

@app.route('/compute_routes.json', methods=['GET'])
def computeRoutes():
    error = None
    locationsJSONStr = request.args.get('locations', '')
    locationsList = json.loads(locationsJSONStr)
    locationTuples = map(locationsList, lambda x: (x[0], x[1]))
    routeSolver = aco.RouteSolver(locationTuples)
    (distances, routes) = routeSolver.solveRandomly(iterationCount)
    indices = list(range(len(routes)))
    sortedIndices = sorted(indices, key = lambda x: distances[x])
    sortedRoutes = []
    for index in sortedIndices:
        sortedRoutes.append(routes[index])
    return json.dumps(sortedRoutes)

if __name__ == '__main__':
    app.run(debug=True)
