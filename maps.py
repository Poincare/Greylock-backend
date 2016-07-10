## Maps key: AIzaSyC19ecttqnSP6DxyANqAPH6_JSLee88T5A
import googlemaps as gmaps
from datetime import datetime
import json
import geopy

gmapsKey = 'AIzaSyC19ecttqnSP6DxyANqAPH6_JSLee88T5A'
gmapsClient = gmaps.Client(key = gmapsKey)

# Returns the first point on the route between two points
def getRouteIntersections(gmapsClient, origin, destination, maxWalk):
    now = datetime.now()
    directions_result = gmapsClient.directions(origin, destination,
                                               mode='driving',
                                               departure_time=now)
    validIntersections = []
    totalDist = 0
    for leg in directions_result[0]['legs']:
        for step in leg['steps']:
            if totalDist < maxWalk:
                validIntersections.append(((step['end_location']['lat'],
                                            step['end_location']['lng']
                                           ), origin))
                totalDist += step['distance']['value']
            else:
                return validIntersections

    return validIntersections

def addressToLatLngTuple(address):
    location = geopy.Nominatim().geocode(address)
    return location

# Returns list of intersections in a route to give to FrontEnd
def getFinalResult(gmapsClient, origin, destination):
    now = datetime.now()
    directions_result = gmapsClient.directions(origin, destination,
                                               mode='driving',
                                               departure_time=now)
    validIntersections = []
    for leg in directions_result[0]['legs']:
        for step in leg['steps']:
            validIntersections.append((step['end_location']['lat'],
                                        step['end_location']['lng']))
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
