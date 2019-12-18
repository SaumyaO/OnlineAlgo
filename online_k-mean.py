import matplotlib.pyplot as plt
import networkx as nx
from random import random

RequiredNumberOfClusters = 3

f = open('/Users/saumya/Downloads/socfb-nips-ego/socfb-nips-ego.edges', 'r')
lines = f.readlines()
f.close()

G = nx.Graph()
Gtemp = nx.Graph()
centroids = []
clusterGraphs =[]
clusterCount = 0

#init arrays
for x in range(0, RequiredNumberOfClusters+1):
    Gc = nx.Graph()
    clusterGraphs.append(Gc)

for x in range(0, RequiredNumberOfClusters):
    centroids.append(None)

def nodes_connected(u, v):
    return u in G.neighbors(v)

def MoveTempNodesToG(node):
    global G
    global Gtemp
    if (Gtemp.has_node(node)):
        neighbours = nx.node_connected_component(Gtemp,node)
        for neighbour in neighbours:
            G.add_node(neighbour)
        neighboursR = nx.node_connected_component(Gtemp,node)

        print(neighbours)

        for neighbour in neighbours:
            for neighbourR in neighboursR:
                if (not neighbour == neighbourR):
                    if (not G.has_edge(neighbour, neighbourR)):
                        G.add_edge(neighbour, neighbourR)

        for neighbour in list(neighbours):
            if (Gtemp.has_edge(neighbour, node)):
                if (not G.has_edge(neighbour, node)):
                    G.add_edge(neighbour, node)

        for neighbour in neighbours:
            Gtemp.remove_node(neighbour)

def SetCluster(node,partner):
    global clusterCount
    global RequiredNumberOfClusters
    global centroids
    global clusterGraphs
    if (clusterCount < RequiredNumberOfClusters):
        centroids[clusterCount] = node
        clusterGraphs[clusterCount].add_node(node)
        clusterCount = clusterCount + 1
    else:
        nearestCentroidIndex = -1
        shortestPath =-2
        for x in range(0, RequiredNumberOfClusters):
            pathLength = -2
            if(nodes_connected(centroids[x],node)):
                pathLength = nx.shortest_path_length(G,centroids[x],node)
            if(pathLength<shortestPath or shortestPath==-2):
                shortestPath = pathLength
                nearestCentroid = x

        if(shortestPath==-2):
            clusterGraphs[RequiredNumberOfClusters].add_node(node)
        else:
            clusterGraphs[nearestCentroid].add_node(node)

        if(clusterGraphs[nearestCentroid].has_node(partner)):
            clusterGraphs[nearestCentroid].add_edge(node, partner)

        for x in range(0, RequiredNumberOfClusters):
            centroids[x]=nx.center(clusterGraphs[x],None)[0]

        #run k-mean
        nodes = list(G.nodes)
        cursor = True
        cycles = 0

        while cursor:
            cursor = False
            cycles = cycles + 1
            for i in range(0, len(centroids)):
                clusterGraphs[i].clear()

            # create clusters
            for node in nodes:
                minDistance = -2
                nodeCentroid = None
                for i in range(0, len(centroids)):
                    distance = nx.shortest_path_length(G, node, centroids[i])
                    if(minDistance>distance or minDistance == -2):
                        minDistance=distance
                        nodeCentroid=i

                if (not clusterGraphs[nodeCentroid].has_node(node)):
                    clusterGraphs[nodeCentroid].add_node(node)

            # add cluser graph edges
            for i in range(0, len(centroids)):
                cNodesL = list(clusterGraphs[i].nodes)
                for cNodeL in cNodesL:
                    cNodesR = list(clusterGraphs[i].nodes)
                    for cNodeR in cNodesR:
                        if (not cNodesL == cNodeR):
                            if (G.has_edge(cNodeL, cNodeR)):
                                clusterGraphs[i].add_edge(cNodeL, cNodeR)

            for x in range(0, len(centroids)):
                newCentroid = nx.center(clusterGraphs[x], e=None)[0]
                if (newCentroid != centroids[x]):
                    centroids[x] = nx.center(clusterGraphs[x], e=None)[0]
                    cursor = True

nodeColor = []
colors = [(random(), random(), random()) for _i in range(len(centroids)+1)]

#online simulation
lineIndex =0;
for line in lines:
    if(not line.startswith("%")):
        lineIndex = lineIndex + 1
        edge = line.rstrip().split(' ')
        if(len(edge)>1):
            left = False
            right = False

            if(not G.has_node(edge[0])):
                left = True
            if (not G.has_node(edge[1])):
                right = True

            '''both are new nodes'''
            if(left and right and lineIndex>1):
                if(not Gtemp.has_node(edge[0])):
                    Gtemp.add_node(edge[0])
                if (not Gtemp.has_node(edge[1])):
                    Gtemp.add_node(edge[1])
                Gtemp.add_edge(edge[0], edge[1])
            else:
                if (left):
                    G.add_node(edge[0])
                if (right):
                    G.add_node(edge[1])
                G.add_edge(edge[0], edge[1])

                if(left):
                    SetCluster(edge[0],edge[1])
                    #move Gtemp nodes to G
                    MoveTempNodesToG(edge[0])

                if(right):
                    SetCluster(edge[1],edge[0])
                    # move Gtemp nodes to G
                    MoveTempNodesToG(edge[1])

        #plot graph
        nodes = list(G.nodes)
        nodeColor.clear()
        for node in nodes:
            color = False
            for x in range(0, len(centroids)):
                if (clusterGraphs[x].has_node(node)):
                    nodeColor.append(colors[x])
                    color=True
            if(not color):
                nodeColor.append(colors[len(centroids)])

        print("Line Index: " + str(lineIndex))
        print("Line : " + line)
        nx.draw(G,with_labels = True,node_color=nodeColor)
        plt.show()

print("Centroids:")
print(centroids)

print("Cluster Count: " + str(clusterCount))

print("Cluster diameters:")
for x in range(0, RequiredNumberOfClusters):
    print("Cluser " + str(x+1) + " diameter: " + str(nx.diameter(clusterGraphs[x], e=None)))

nodes = list(G.nodes)
nodeColor.clear()
for node in nodes:
    color = False
    for x in range(0, len(centroids)):
        if (clusterGraphs[x].has_node(node)):
            nodeColor.append(colors[x])
            color=True
    if(not color):
        nodeColor.append(colors[len(centroids)])

nx.draw(G,with_labels = True,node_color=nodeColor)
plt.show()

