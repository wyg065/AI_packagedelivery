import networkx as nx
import matplotlib.pyplot as plt
import random as rand
from random import choice
import math
import copy

#Car Class and Constructor
class Car(object):
    name = "car"
    packageCapacity = 4        
    location = None
    packageList = [1, 1, 3]
    location = (0,0)
    packageList = []
    travelDistance = 0
    
def make_car(graph, packages, n):
    car = Car()
    car.name = n    
    car.location = choice(graph.nodes())
    car.packageList = copy.deepcopy(packages)
    car.travelDistance = 0
    return car

#Package Class and Constructor
class Package(object):
    source = None
    destination = None
    pickedUp = 0
    delivered = 0

def make_package(graph):  
    package = Package()
    package.source = choice(graph.nodes())
    package.destination = choice(graph.nodes())
    package.pickedUp = 0
    package.delivered = 0 
    return package

def makeMap(m, n, gapfreq):
    """ Creates a graph in the form of a grid, with mXn nodes.
    The graph has irregular holes poked into it by random deletion.

    :param m: number of nodes on one dimension of the grid
    :param n: number of nodes on the other dimension
    :param gapfreq: the fraction of nodes to delete (see function prune() below)
    :return: a networkx graph with nodes and edges.

    The default edge weight is  (see below).  The edge weights can be changed by
    designing a list that tells the frequency of weights desired.
      100% edge weights 1:  [(1,100)]
      50% weight 1; 50% weight 2: [(1,50),(2,100)]
      33% each of 1,2,5: [(1,33),(2,67),(5,100)]
      a fancy distribution:  [(1,10),(4,50),(6,90),(10,100)]
      (10% @ 1, 40% @ 4, 40% @ 6, 10% @ 10)
    """
    g = nx.grid_2d_graph(m, n)
    weights = [(1,100)]
    prune(g, gapfreq)
    setWeights(g, weights)
    return g


def setWeights(g, weights):
    """ Use the weights list to set weights of graph g
    :param g: a networkx graph
    :param weights: a list of pairs [(w,cf) ... ]
    :return: nothing

    weights are [(w,cf) ... ]
    w is the weight, cf is the cumulative frequency

    This function uses a uniform random number to index into the weights list.
    """
    for (i, j) in nx.edges(g):
        c = rand.randint(1,100)
        w = [a for (a,b) in weights if b >= c] # drop all pairs whose cf is < c
        g.edge[i][j]['weight'] = w[0]  # take the first weight in w
    return


def draw(g):
    """ Draw the graph, just for visualization.  Also creates a jpg in $CWD
    :param g: a networkx graph
    :return:
    """
    pos = {n: n for n in nx.nodes(g)}
    nx.draw_networkx_nodes(g, pos, node_size=40)
    edges = nx.edges(g)
    nx.draw_networkx_edges(g, pos, edgelist=edges, width=3)
    plt.axis('off')
    plt.savefig("simplegrid.png")  # save as png
    plt.show()  # display
    return


def prune(g, gapf):
    """ Poke random holes the graph g by deleting random nodes, with probability gapf.
    Then clean up by deleting all but the largest connected component.

    Interesting range (roughly):  0.1 < gapf < 0.3
    values too far above 0.3 lead to lots of pruning, but rather smaller graphs

    :param g: a networkx graph
    :param gapf: a fraction in [0,1]
    :return: nothing
    """
    # creating gaps...
    for node in nx.nodes(g):
        if rand.random() < gapf:
            g.remove_node(node)
    # deleting all but the largest connected component...
    comps = sorted(nx.connected_components(g), key=len, reverse=False)
    while len(comps) > 1:
        nodes = comps[0]
        for node in nodes:
            g.remove_node(node)
        comps.pop(0)
        
        
def getPackage(car, package, graph):
    print(car.name)
    carPath = nx.astar_path(graph, car.location, package.source)
    car.location = package.source    
    car.travelDistance += len(carPath)
    package.pickedUp = 1
    car.packageList.append(package)
    print("Package Received")    
    #print(package.source)
    #print statement for graph here
    g2 = nx.Graph()
    g2.add_nodes_from(graph)
    i = 1
    while i < len(carPath):
        g2.add_edge(carPath[i-1], carPath[i])
        i += 1
    draw(g2)
    
def deliverPackage(car, package, graph):
    print(car.name)
    carPath = nx.astar_path(graph, car.location, package.destination)
    car.location = package.destination
    car.travelDistance += len(carPath)
    package.delivered = 1
    
    car.packageList.remove(package)
    
    print("Package Delivered") 
    #print(package.destination)
    #print statement for graph here
    g2 = nx.Graph()
    g2.add_nodes_from(graph)
    i = 1
    while i < len(carPath):
        g2.add_edge(carPath[i-1], carPath[i])
        i += 1
    draw(g2)
    

def toGarage(car, garage, graph):
    print(car.name)
    carPath = nx.astar_path(graph, car.location, garage)
    car.location = garage
    car.travelDistance += len(carPath)
    car.inGarage = 1
    print("returned to garage") 
    #print statement for graph here
    g2 = nx.Graph()
    g2.add_nodes_from(graph)
    i = 1
    while i < len(carPath):
        g2.add_edge(carPath[i-1], carPath[i])
        i += 1
    draw(g2)

    
def closestPackageFromList(car, packages, city):
    bestPackage = packages[1]
    closestPackageDistance = math.inf
    i = 0    
    while i < len(packages):
        carPath = nx.astar_path(city, car.location, packages[i].source)        
        if len(carPath) < closestPackageDistance:
            bestPackage = packages[i]
            closestPackageDistance = len(carPath)
        i += 1
    return bestPackage
    
    

def closestPackageOrDestinationFromList(car, packages, city):
    bestPackage = make_package(city)
    closestPackageDistance = math.inf
    
    i = 0    
    while i < len(packages):
        carPath = nx.astar_path(city, car.location, packages[i].source)
        if len(carPath) < closestPackageDistance:
            if (len(car.packageList) < car.packageCapacity):
                bestPackage = packages[i]
                closestPackageDistance = len(carPath)
        i += 1
        
    i = 0
    while i < len(car.packageList):
        carPath = nx.astar_path(city, car.location, car.packageList[i].destination)        
        if len(carPath) < closestPackageDistance:
            bestPackage = car.packageList[i]
            closestPackageDistance = len(carPath)
        i += 1
        
    return bestPackage

    
def closestPackageWithHypotenuse(car, packages, city):
    bestPackage = packages[1]
    closestPackageDistance = math.inf
    i = 0
    while i < len(packages):
        
        carPath = math.hypot(car.location[0] - packages[i].source[0], car.location[1] - packages[i].source[1])        
        #carPath = (car.location[0] - packages[i].source[0])^2 + (car.location[0] - packages[i].source[0])^2
        #carPath = math.sqrt(carPath)        
        #print(carPath)
        if carPath < closestPackageDistance:
            bestPackage = packages[i]
            closestPackageDistance = carPath
        i += 1
    #print(bestPackage.source)
    bestPath = nx.astar_path(city, car.location, bestPackage.source)  
    g2 = nx.Graph()
    g2.add_nodes_from(city)
    i = 1
    while i < len(bestPath):
        g2.add_edge(bestPath[i-1], bestPath[i])
        i += 1
    draw(g2)
        
    return bestPackage
    
def deliverPackagesInOrder(car, packageList, city, garage):
    i = 0
    while i < len(packageList):
        getPackage(car, packageList[i], city)
        deliverPackage(car, packageList[i], city)
        i += 1
    toGarage(car, garage, city)

def distanceToPackage(car, package, city):
    carPath = nx.astar_path(city, car.location, package.source)        
    return len(carPath)

def shortestCarToPackagePath(carList, packageList, city):
    numberOfCars = len(carList)
    i = 0
    j = 0
    p = len(packageList) 
            
    pickupInfo = (carList[0], packageList[0])
    
    if(numberOfCars == 1):
        return pickupInfo
    else:
        while(i < p): 
            j = 0
            while(j < len(carList)):
                if(distanceToPackage(carList[j], packageList[i], city) <= distanceToPackage(pickupInfo[0], pickupInfo[1], city)):
                    pickupInfo = carList[j], packageList[i]
                j += 1         
            i += 1
        return pickupInfo

def shortestCarToDestinationPath(carList, city): 
    i = 0;
    j = 0;
    #deliverInfo = ((0,0),(0,0)) 
    
    #while (i < len(carList)):
    for i in range(len(carList)):
       
        if (not carList[i].packageList):
            continue
        else:
            j = 0;
            deliverInfo = (carList[i], carList[i].packageList[j])
        
            while(j < len(carList[i].packageList)):
                carPath = nx.astar_path(city, carList[i].location,carList[i].packageList[j].source)
                tempLen = len(carPath)
                carPath = nx.astar_path(city, deliverInfo[0].location, deliverInfo[1].destination)
                bestLen = len(carPath)
                
                if(tempLen < bestLen):
                    deliverInfo = (carList[i], carList[i].packageList[j])
                j += 1
            i += 1
            
    try :
        return deliverInfo
    except :
        deliverInfo = ((0,0),(0,0)) 
        return deliverInfo
    

def deliverPackagesClosestFirst(car, packageList, city, garage):
    while len(packageList) > 1:
        bestPackage = closestPackageFromList(car, packageList, city)
        getPackage(car, bestPackage, city)
        deliverPackage(car, bestPackage, city)
        packageList.remove(bestPackage)
    toGarage(car, garage, city)
    

def deliverPackagesClosestFirstDestination(car, packageList, city, garage):
    while (len(packageList) + len(car.packageList)) > 1:
        bestPackage = closestPackageOrDestinationFromList(car, packageList, city)
        if (bestPackage.pickedUp):
            deliverPackage(car, bestPackage, city)
        else:
            packageList.remove(bestPackage)
            getPackage(car, bestPackage, city)
    toGarage(car, garage, city)
    
    
def deliverAllPackagesAllCars(carList, packageList, city, garage):
    allPackageCount = len(packageList)
    currentCar = None
    currentPackage = None
    carPackageCount = 0
    
    while (allPackageCount > 0):
        carPackageCount = 0
        allPackageCount = 0
        
        for car in carList:
            allPackageCount += len(car.packageList)
            carPackageCount += len(car.packageList)
        allPackageCount += len(packageList)
        
        if (allPackageCount <= 0):
            for car in carList:
                toGarage(car, garage, city)
            return
        
        if (len(packageList) > 0):
            temp = shortestCarToPackagePath(carList, packageList, city)
            currentCar = temp[0]
            currentPackage = temp[1]
        else:
            temp3 = shortestCarToDestinationPath(carList, city)
            currentCar = temp3[0]
            currentPackage = temp3[1]
            
            
        if (carPackageCount > 0):
            temp2 = shortestCarToDestinationPath(carList, city)
            lengthToBestDestination = len(nx.astar_path(city, temp2[0].location, temp2[1].destination))
            lengthToBestPackage = len(nx.astar_path(city, currentCar.location, currentPackage.source))
            if (lengthToBestDestination <= lengthToBestPackage or currentPackage==None):
                currentCar = temp2[0]
                currentPackage = temp2[1]
                
                
        if (currentPackage.pickedUp):
            deliverPackage(currentCar, currentPackage, city)
        else:
            packageList.remove(currentPackage)
            getPackage(currentCar, currentPackage, city)
            
    
        
        
# script to use the above functions
dim = 20
gapfreq = 0.35
city = makeMap(dim, dim, gapfreq)   # a square graph
draw(city)

p1 = make_package(city)
p2 = make_package(city)
p3 = make_package(city)
p4 = make_package(city)
p5 = make_package(city)
p6 = make_package(city)
p7 = make_package(city)
p8 = make_package(city)
p9 = make_package(city)
p10 = make_package(city)

packages = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
packages2 = copy.deepcopy(packages)
packages3 = []
packages4 = copy.deepcopy(packages3)
packages5 = copy.deepcopy(packages3)

car1 = make_car(city, packages3, "jimmy")
car2 = make_car(city, packages4, "thomas")
car3 = make_car(city, packages5, "carter")

garage = choice(city.nodes())

car1.packageCapacity = 3;
car2.packageCapacity = 3;
car3.packageCapacity = 3;

car1.location = garage
car2.location = garage
car3.location = garage

cars = [car1, car2, car3]

deliverAllPackagesAllCars(cars, packages, city, garage)
print(car1.name + " travel distance: " + str(car1.travelDistance))
print(car2.name + " travel distance: " + str(car2.travelDistance))
print(car3.name + " travel distance: " + str(car3.travelDistance))
print("total travel distance: " + str(car1.travelDistance + car2.travelDistance + car3.travelDistance))