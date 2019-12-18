import operator

import matplotlib.pyplot as plt
import networkx as nx
from random import random
import copy
requiredNumberOfClusters =3

f = open('/Users/saumya/Downloads/rt-twitter-copen/rt-twitter-copen.mtx', 'r')   # read the dataset
lines = f.readlines() # output is a list of edges
f.close()

G = nx.Graph()   #initialize the graph

for line in lines:
    if(not line.startswith("%")): # ignore the % statement in the edgelist
        edge = line.rstrip().split(' ') # split by space node, rstrip removes special charater, edge out is an array
        if(len(edge)>1):# length of edge will be always be 2
            if(not G.has_node(edge[0])): # has_node return true or  false if node is added or not
                G.add_node(edge[0])
            if (not G.has_node(edge[1])):
                G.add_node(edge[1])
            G.add_edge(edge[0], edge[1])

clusters = []           # declare as an array of nx graph
Gt = copy.deepcopy(G)   # duplicates the Graph object

while True:
    edges = nx.edge_betweenness_centrality(Gt, normalized=True, weight=None) # evaluate the betweenness of each node

    print(edges)
    sorted_x = sorted(edges.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_x)
    maxbetweeness=-1         #  betweeness will be always positive
    edgeToRemove = None
    for key,val in edges.items():
        if(val>maxbetweeness):
            maxbetweeness=val
            edgeToRemove=key

    print("Edge removed: " + str(edgeToRemove) + " betweeness: " + str(maxbetweeness))
    print(Gt.remove_edge(edgeToRemove[0],edgeToRemove[1]))


#find number of clusters
    noOfClusters = 0
    nodes = list(Gt.nodes)
    Gc = nx.Graph()
    clusters.clear()     #to perform multiple time
    for node in nodes:
        if (not Gc.has_node(node)):
            noOfClusters = noOfClusters + 1
            Gc.add_node(node)
            cnodes = nx.node_connected_component(Gt, node) #returns whole tree including the start node
            print(cnodes)
            clusters.append(cnodes)
            for cnode in cnodes:
                if (not Gc.has_node(cnode)):
                    Gc.add_node(cnode)

    print("No of clusters: " + str(noOfClusters))
    if(requiredNumberOfClusters<=noOfClusters):
        break;

#assing cluster colours
colors = [(random(), random(), random()) for _i in range(requiredNumberOfClusters)]
nodes = list(G.nodes)
nodeColor = []

#find diameter of each cluster
clusterGraphs = []
for x in range(0, len(clusters)):
    Gx = nx.Graph()
    clusterGraphs.append(Gx)

edges = list(G.edges)
print(edges)
for edge in edges:
    for x in range(0, len(clusters)):
        if(clusters[x].__contains__(edge[0]) and clusters[x].__contains__(edge[1])):
            if (not clusterGraphs[x].has_node(edge[0])):
                clusterGraphs[x].add_node(edge[0])
            if (not clusterGraphs[x].has_node(edge[1])):
                clusterGraphs[x].add_node(edge[1])
            clusterGraphs[x].add_edge(edge[0], edge[1])

n=0
maxDiameter = -1
for g in clusterGraphs:
    print("Cluser " + str(n+1) + ":")
    print(clusters[n])
    diameter = nx.diameter(g)
    if(diameter>maxDiameter):
        maxDiameter = diameter
    print("Cluster graph diameter: "+ str(diameter))
    n = n +1

print("Max Diameter: " + str(maxDiameter))

for node in nodes:
    for x in range(0, len(clusters)):
        if(clusters[x].__contains__(node)):
            nodeColor.append(colors[x])

nx.draw(G,with_labels = False,node_color=nodeColor, node_size = 50)
plt.show()
