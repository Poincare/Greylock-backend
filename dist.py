## Maps key: AIzaSyC19ecttqnSP6DxyANqAPH6_JSLee88T5A
import googlemaps as gmaps
from datetime import datetime
import json

gmapsKey = 'AIzaSyC19ecttqnSP6DxyANqAPH6_JSLee88T5A'
gmapsClient = gmaps.Client(key = gmapsKey)

origins = [(40.760909, -73.991073)]
destinations = [(40.757850, -73.994989)]
matrix = gmapsClient.distance_matrix(origins, destinations)

print(matrix)
