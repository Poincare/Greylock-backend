import pants
import math
import random
from geopy.distance import vincenty

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
        self.nearestIntersections = list(map(self.getNearestIntersections, locations))

    def getNearestIntersections(self, location):
        ## TODO replace with the thing that actually gets the
        ## nearest intersection.
        return [location]

    def distanceBetweenPoints(self, a, b):
        return vincenty(a,b).miles

    def solveIteration(self, nearestIntersections):
        pandasSolver = PantsSolver(nearestIntersections,
                                    self.distanceBetweenPoints)
        return pandasSolver.solve()

    def solveRandomly(self, iterCount):
        bestDist = float('inf')
        bestRoute = None

        for _ in range(iterCount):
            selectedIntersections = []

            for intersections in self.nearestIntersections:
                ## pick a random interesection
                selectedIntersections.append(random.choice(intersections))

            (solDist, solRoute) = self.solveIteration(selectedIntersections)
            if solDist < bestDist:
                bestDist = solDist
                bestRoute = solRoute

        return (bestDist, bestRoute)

nodes = []
for _ in range(20):
  x = random.uniform(-10, 10)
  y = random.uniform(-10, 10)
  nodes.append((x, y))

routesSolver = RouteSolver(nodes)
print(routesSolver.solveRandomly)
