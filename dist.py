## Maps key: AIzaSyC19ecttqnSP6DxyANqAPH6_JSLee88T5A
import googlemaps as gmaps
from datetime import datetime
import json

gmapsKey = 'AIzaSyC19ecttqnSP6DxyANqAPH6_JSLee88T5A'
gmapsClient = gmaps.Client(key = gmapsKey)

origins = ["Perth, Australia", "Sydney, Australia",
           "Melbourne, Australia", "Adelaide, Australia",
           "Brisbane, Australia", "Darwin, Australia",
           "Hobart, Australia", "Canberra, Australia"]
destinations = ["Uluru, Australia",
                "Kakadu, Australia",
                "Blue Mountains, Australia",
                "Bungle Bungles, Australia",
                "The Pinnacles, Australia"]

matrix = gmapsClient.distance_matrix(origins, destinations)

print(matrix)