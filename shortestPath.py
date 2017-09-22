import numpy
from geopy.distance import great_circle
import math
import random
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot 
from datetime import datetime



class Airport:

	def __init__(self, name, city, country, IATA, lat, lon ):
		self.name = name
		self.city = city
		self.country = country
		self.IATA = IATA
		self.lat = lat
		self.lon = lon
		self.routes = []

	def getIATA(self):
		return self.IATA
	
	def getName(self):
		return self.name
	
	def getCountry(self):
		return self.country

	def getCoord(self):
		return self.lat,self.lon

	def getRoutes(self):
		return self.routes

	def addRoute(self, destIATA):
		self.routes.append(destIATA)

airportFile = open("airports.dat.txt")
airportGraph = dict()
for line in airportFile:
	stuff = line.split(',')
	apName = stuff[1][1:-1]
	apCity = stuff[2][1:-1]
	apCountry = stuff[3][1:-1]
	iata = stuff[4][1:-1 ]
	lat = stuff[6]
	lon = stuff[7]
	if stuff[4] != "\N":
		airportGraph[iata] = Airport(apName,apCity,apCountry,iata,lat,lon)	
airportFile.close()




routesFile = open("routes.dat.txt")
for line in routesFile:
	stuff = line.split(',')
	srcIATA = stuff[2]
	destIATA = stuff[4]
	if srcIATA in airportGraph and destIATA in airportGraph and srcIATA != "\N" and destIATA != "\N":
		airportGraph[srcIATA].addRoute(destIATA)
routesFile.close()

src = raw_input("Enter source aiport: ").upper()
dest = raw_input("Enter destination airport: ").upper()

def heuristic_cost_estimate(src,dest):
        srcCoord = airportGraph[src].getCoord()
        destCoord = airportGraph[dest].getCoord()
        return great_circle(srcCoord,destCoord).miles

def reconstruct_path(cameFrom,current):
        total_path = [current]
        while current in cameFrom:
                current = cameFrom[current]
                total_path.append(current)
        return total_path






closedSet = set()
openSet = {src}
cameFrom = dict()
Inf = float("inf")
gScore = dict()
gScore = gScore.fromkeys(airportGraph.keys(),Inf)
fScore = gScore

gScore[src] = 0
fScore[src] = heuristic_cost_estimate(src,dest)


while openSet:
        current = random.sample(openSet,1)[0]
        for node in openSet:
                 if fScore[node] < fScore[current]:
                        current = node

        print("Current is now "+current)
        if current == dest:
                paths = reconstruct_path(cameFrom,current)
                print(paths)
                break;


        openSet.remove(current)
        closedSet.add(current)

        for neighbor in airportGraph[current].getRoutes():
                if neighbor in closedSet:
                        continue
                if neighbor not in openSet:
                        openSet.add(neighbor)

                
                tentative_gScore = gScore[current] + great_circle(airportGraph[current].getCoord(),airportGraph[neighbor].getCoord()).miles
                #print("tent is "+ str(tentative_gScore))
                if tentative_gScore >= gScore[neighbor]:
                        continue


                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + heuristic_cost_estimate(neighbor,dest)


m = Basemap(projection = 'mill',lon_0=0)
m.drawcoastlines()
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua')

for i in range(len(paths)-1 ,0, -1):
        src = airportGraph[paths[i]]
        dest = airportGraph[paths[i-1]]
        srcLat,srcLon = src.getCoord()
        destLat,destLon = dest.getCoord()
        m.drawgreatcircle(float(srcLon),float(srcLat),float(destLon),float(destLat),linewidth =2,color='b')
        print("from "+src.getName()+" to "+dest.getName())
matplotlib.pyplot.show()
#for path in paths:
 #       print(airportGraph[path].getName())                









