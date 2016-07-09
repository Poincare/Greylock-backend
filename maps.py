## Maps key: AIzaSyC19ecttqnSP6DxyANqAPH6_JSLee88T5A
import googlemaps as gmaps
from datetime import datetime
import json

gmapsKey = 'AIzaSyC19ecttqnSP6DxyANqAPH6_JSLee88T5A'
gmapsClient = gmaps.Client(key = gmapsKey)

# Returns the first point on the route between two points
def getRouteIntersections(gmapsClient, origin, destination, maxWalk):
    now = datetime.now()
    directions_result = gmapsClient.directions(origin, destination,
                                               mode='walking',
                                               departure_time=now)
    maxWalk = 2500
    validIntersections = []
    totalDist = 0
    for leg in directions_result[0]['legs']:
        for step in leg['steps']:
            if totalDist < 2500:
                validIntersections.append((origin,
                                           (step['end_location']['lat'],
                                            step['end_location']['lng']
                                           )))
                totalDist += step['distance']['value']
            else:
                return validIntersections

    return validIntersections

def testGetRouteIntersection():
    routeIntersectionCoord = getRouteIntersections(
        gmapsClient, \
        "101 McLellan Drive, South San Francisco, CA", \
        "5000 N Ballard Rd, Appleton, WI", \
        50
    )

    print(routeIntersectionCoord)

if __name__ == "__main__":
    testGetRouteIntersection()
