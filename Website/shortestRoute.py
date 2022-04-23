import osmnx as ox
import networkx as nx
import math
import folium
import time
import generateMap
from .functions import matching_panda

mainGraph = ""


def MapInit(origin_point, destination_point, carType, numOfSeats):
    # Starting timer
    start_time = time.time()

    # Generate shortest route and plot onto graph object
    output = shortest_route(origin_point, destination_point)
    route = output[0]
    outputGraph = output[2]
    road = ox.folium.plot_route_folium(outputGraph, route, color="Black")

    origin_lat = outputGraph.nodes[route[0]]['y']
    origin_long = outputGraph.nodes[route[0]]['x']
    dest_lat = outputGraph.nodes[route[-1]]['y']
    dest_long = outputGraph.nodes[route[-1]]['x']

    # Custom marker icon, images stored in cloudinary rather than files to save space
    icon2 = folium.features.CustomIcon(icon_image="https://res.cloudinary.com/whathellahor/image/upload/v1649331436/CSC1008/customMarker.png", icon_size=(80, 80))
    icon = folium.features.CustomIcon(icon_image="https://res.cloudinary.com/whathellahor/image/upload/v1649331436/CSC1008/customMarker.png", icon_size=(80, 80))

    # Plot the markers onto map
    folium.Marker(location=[dest_lat, dest_long], icon=icon2).add_to(road)
    folium.Marker(location=[origin_lat, origin_long], icon=icon).add_to(road)

    # Declaring tileset
    folium.TileLayer("cartodbpositron").add_to(road)

    # Adding driver logo, images stored in cloudinary rather than files to save space
    car = folium.features.CustomIcon(icon_image="https://res.cloudinary.com/whathellahor/image/upload/v1649246320/CSC1008/mainLogoNoBckgrd.png", icon_size=(50, 50))
    driverLocation = matching_panda(carType, numOfSeats, origin_point[0], origin_point[1])
    driver = [driverLocation[0],driverLocation[1]]
    # print(shortest_route("",origin_point,destination_point)[1])
    folium.Marker(location=driver, icon=car, icon_size=(80, 80)).add_to(road)

    # Save plotted route on map
    road.save("Website/templates/map.html")
    generateMap.generateHtml()
    print("---Executed with %s seconds ---" % (time.time() - start_time))

def shortest_route(origin_point, destination_point):
    #Load graphml file as a directional graph data structure
    mainGraph = ox.io.load_graphml("jurong.graphml")

    # Creates boundary box around start and end points to create a small radius of service roads to reach the end/start points
    minLat1 = origin_point[0] - (0.009 * 0.2)  # north
    maxLat1 = origin_point[0] + (0.009 * 0.2)  # south
    minLong1 = origin_point[1] - (0.009 * 0.2)  # east
    maxLong1 = origin_point[1] + (0.009 * 0.2)  # west

    minLat2 = destination_point[0] - (0.009 * 0.2)
    maxLat2 = destination_point[0] + (0.009 * 0.2)
    minLong2 = destination_point[1] - (0.009 * 0.2)
    maxLong2 = destination_point[1] + (0.009 * 0.2)

    patch_1 = ox.graph.graph_from_bbox(minLat1, maxLat1, minLong1, maxLong1, network_type='bike')
    patch_2 = ox.graph.graph_from_bbox(minLat2, maxLat2, minLong2, maxLong2, network_type='bike')

    mainGraph = nx.compose(mainGraph, patch_1)
    mainGraph = nx.compose(mainGraph, patch_2)

    origin_node = ox.distance.nearest_nodes(mainGraph, origin_point[1], origin_point[0])
    destination_node = ox.distance.nearest_nodes(mainGraph, destination_point[1], destination_point[0])

    graph = mainGraph

    opened = []  # list of nodes that are yet to be explored
    closed = []  # list of nodes that have been explored
    startNode = Node(origin_node)
    endNode = Node(destination_node)
    opened += [startNode]

    while len(opened) > 0:
        currNode = opened[minF(opened)]
        opened.remove(currNode)
        closed.append(currNode)

        if isDest(currNode, endNode) == True:
            break

        # Generate children as list of neighboring nodes to current node
        arrOfNeighbors = list(graph.neighbors(currNode.id))
        if currNode.id == 5178982355:
            arrOfNeighbors.remove(246121986)
        currNode.setChildren(arrOfNeighbors)
        for child in currNode.children:
            if child in closed:
                continue  # goes back to start of for loop

            # creating f,g,h values
            child.g = currNode.g + graph[currNode.id][child.id][0][
                'length']  # uses the distance between nodes as the cost
            child.h = euclideanDistance(graph, child, endNode)
            child.f = child.g + child.h

            # Check if child already in opened list
            temp = childIn(child, opened)  # to hold potential node with same id as child's to compare the g value

            if temp == False:
                opened.append(child)
            else:
                if child.g > temp.g:
                    continue

    if isDest(currNode, endNode) == False:
        return "No route found."
    route = backTrack(currNode)
    route.reverse()
    output = [route, get_route_distance(graph, route), mainGraph]
    return output

'''----------------------Helper Functions---------------------------------'''
# Function to determine a straight line distance from one point to another
def euclideanDistance(graph, node, dest):
    if node.id == dest.id:
        return 0
    dx = abs(graph.nodes[node.id]['x'] - graph.nodes[dest.id]['x'])
    dy = abs(graph.nodes[node.id]['y'] - graph.nodes[dest.id]['y'])

    return math.sqrt(dx * dx + dy * dy)

# Checks for whether the node is in the array
def childIn(node, arr):
    for i in arr:
        if node.id == i.id:
            return i
    return False

# Recursive backtracking algorithm to reach the root or parent node of any given node
def backTrack(node):
    prev = node.parent
    path = [node.id]
    while prev != -1:
        path.append(prev.id)
        prev = prev.parent
    return path

# Returns the node with lowest F value in the array 
def minF(arr):
    fArr = []
    for i in arr:
        fArr.append(i.f)
    return fArr.index(min(fArr))

# Checks if the node given is the same as the destination
def isDest(node, dest):
    if node.id == dest.id:
        return True
    return False


class Node:
    def __init__(self, obj):
        self.id = obj
        self.parent = -1
        self.children = []
        self.g = 0
        self.f = 0
        self.h = 0  # use euclidean algorithm to get distance

    def setChildren(self, lst):
        for i in lst:
            node = Node(i)
            self.children.append(node)
            node.parent = self

# Returns total distance of a route from start to end
def get_route_distance(mainGraph, route):
    totalDist = 0
    counter = 0
    while counter < len(route) - 1:
        totalDist += mainGraph[route[counter]][route[counter + 1]][0]['length']
        counter += 1

    return totalDist



