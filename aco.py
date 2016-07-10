import pants
import math
import random
import googlemaps as gmaps
# from geopy.distance import vincenty
from pants.ant import Ant

import maps

gmapsKey = 'AIzaSyC19ecttqnSP6DxyANqAPH6_JSLee88T5A'
gmapsClient = gmaps.Client(key = gmapsKey)

def geoDistance(a,b):
    deltal = (b[1] - a[1]) * 0.0174533
    phi1 = a[0] * 0.0174533
    phi2 = b[0] * 0.0174533
    x = deltal * math.cos((phi1 + phi2) / 2.0)
    y = phi2 - phi1
    return (math.sqrt(x*x + y*y) * 3959)


class PantsSolver(object):
    def __init__(self, nodes, distMetric):
        self.nodes = nodes
        self.distMetric = distMetric

    def solve(self):
        world = pants.World(self.nodes, self.distMetric)
        ants = [Ant().initialize(world, world.nodes[0]) for i in range(10)]

        solver = pants.Solver()
        # solution = solver.solve(world)
        # solutions = solver.solutions(world)
        solver.find_solutions(ants)
        ants = sorted(ants)
        for i in range(1, len(ants)):
            assert ants[i - 1].distance <= ants[i].distance

        return (ants[0].distance, ants[0].tour)

def removeClose(locations):
    for location in locations:
        for other_loc in locations:
            if (other_loc != location):
                if(geoDistance(location, other_loc) < 0.3):
                    locations.remove(location)
                    return locations
    return None

class RouteSolver(object):
    def __init__(self, locations, destination):
        while (removeClose(locations)):
            pass

        self.locations = [destination] + locations
        print("Locations: ", self.locations)
        self.busstops = [[(destination, destination)]] + list(map(self.getNearestIntersections, locations))
        # print('Bus stops: ')
        # print(self.busstops)

    def getNearestIntersections(self, location):
        nearestIntersections = []
        for other_loc in self.locations:
            if(other_loc != location):
                nearestIntersections += maps.getRouteIntersections(gmapsClient, location, other_loc, 1000)
        return nearestIntersections

    def distanceBetweenPoints(self, a, b):
        # return 5 * gmapsClient.distance_matrix(a[0],b[0])['rows'][0]['elements'][0]['distance']['value'] + \
        #     gmapsClient.distance_matrix(a[0],a[1])['rows'][0]['elements'][0]['distance']['value'] + \
        #     gmapsClient.distance_matrix(b[0],b[1])['rows'][0]['elements'][0]['distance']['value']
        return 3 * geoDistance(a[0],b[0]) + geoDistance(a[0],a[1]) + geoDistance(b[0],b[1])

    def solveIteration(self, nearestIntersections):
        pandasSolver = PantsSolver(nearestIntersections,
                                    self.distanceBetweenPoints)
        return pandasSolver.solve()

    def solveRandomly(self, iterCount):
        distances = []
        routes = []
        if(len(self.locations) < 3):
            return ([], [])

        for _ in range(iterCount):
            selectedIntersections = []

            for nodes in self.busstops:
                ## pick a random interesection
                selectedIntersections.append(random.choice(nodes))

            (solDist, solRoute) = self.solveIteration(selectedIntersections)
            if solDist < bestDist:
                distances.append(solDist)
                routes.append(solRoute)

        return (distances, routes)

    def renderRoute(self, stops):
        listOfIntersections = []
        for i in range(1, len(stops)):
            listOfIntersections.append(maps.getFinalResult(
                gmapsClient,
                stops[i-1][0],
                stops[i][0]))
        return listOfIntersections

if __name__ == '__main__':
    homes = []
    homes.append((40.760909, -73.991073))
    homes.append((40.757850, -73.994989))
    homes.append((40.745536, -73.991057))
    homes.append((40.745745, -73.994093))
    homes.append((40.746582, -73.987929))
    homes.append((40.758566, -73.984723))
    homes.append((40.755478, -73.983392))
    homes.append((40.756746, -73.983006))
    homes.append((40.762304, -73.982706))
    print("HOMES:")
    for home in homes:
        print ("[{0}, {1}],".format(home[1], home[0]))


    routesSolver = RouteSolver(homes, (40.79011, -74.00000))
    solution = routesSolver.solveRandomly(10)
    print("SOLUTION:")
    print(solution)
    stops = solution[1][0]

    list_of_intersections = []
    for i in range(1,len(stops)):
        list_of_intersections += maps.getFinalResult(gmapsClient, stops[i-1][0], stops[i][0])

    print("SEND TO FRONTEND:")
    for interesection in list_of_intersections:
        print ("[{0}, {1}],".format(interesection[0], interesection[1]))
