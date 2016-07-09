import pants
import math
import random
import googlemaps as gmaps
from geopy.distance import vincenty

import maps

gmapsKey = 'AIzaSyC19ecttqnSP6DxyANqAPH6_JSLee88T5A'
gmapsClient = gmaps.Client(key = gmapsKey)

class PantsSolver(object):
    def __init__(self, nodes, distMetric):
        self.nodes = nodes
        self.distMetric = distMetric

    def solve(self):
        world = pants.World(self.nodes, self.distMetric)
        solver = pants.Solver()
        solution = solver.solve(world)
        solutions = solver.solutions(world)

        return (solution.distance, solution.tour)

class RouteSolver(object):
    def __init__(self, locations):
        self.locations = locations
        self.busstops = list(map(self.getNearestIntersections, locations))

    def getNearestIntersections(self, location):
        nearestIntersections = []
        for other_loc in self.locations:
            if(other_loc != location):
                nearestIntersections += maps.getRouteIntersections(gmapsClient, location, other_loc, 2500)
        return nearestIntersections

    def distanceBetweenPoints(self, a, b):
        return 5 * vincenty(a[0],b[0]).miles + vincenty(a[0],a[1]).miles + vincenty(b[0],b[1]).miles

    def solveIteration(self, nearestIntersections):
        pandasSolver = PantsSolver(nearestIntersections,
                                    self.distanceBetweenPoints)
        return pandasSolver.solve()

    def solveRandomly(self, iterCount):
        bestDist = float('inf')
        bestRoute = None

        for _ in range(iterCount):
            selectedIntersections = []

            for nodes in self.busstops:
                ## pick a random interesection
                selectedIntersections.append(random.choice(nodes))

            (solDist, solRoute) = self.solveIteration(selectedIntersections)
            if solDist < bestDist:
                bestDist = solDist
                bestRoute = solRoute

        return (bestDist, bestRoute)



nodes = []
nodes.append((37.391905, -122.090510))
nodes.append((37.392429, -122.083883))
nodes.append((37.400337, -122.081737))
nodes.append((37.392624, -122.079573))
nodes.append((37.396269, -122.076458))
nodes.append((37.406044, -122.077245))
nodes.append((37.402992, -122.075254))
nodes.append((37.412791, -122.095741))
nodes.append((37.415972, -122.104818))

routesSolver = RouteSolver(nodes)
print(routesSolver.solveRandomly(10))
