import matplotlib.pyplot as plt
import networkx as nx
from random import random
import operator


no_of_centrioid = 3

centroids =[]

x = open('/Users/saumya/Downloads/rt-twitter-copen/rt-twitter-copen.mtx', 'r')
lines = x.readlines()
x.close()

Gmain = nx.Graph()


for line in lines:
    if(not line.startswith("%")):
        edge = line.rstrip().split(' ')
        if(len(edge)>1):
            if(not Gmain.has_node(edge[0])):
                Gmain.add_node(edge[0])
            if (not Gmain.has_node(edge[1])):
                Gmain.add_node(edge[1])
            Gmain.add_edge(edge[0], edge[1])

centrality = nx.degree_centrality(Gmain)

print(centrality)
sorted_x = sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_x)


count = 0
for key,value in sorted_x:
    if count != no_of_centrioid:
        centroids.append(key)
        count = count + 1


print(centroids)

f = open('/Users/saumya/Downloads/rt-twitter-copen/rt-twitter-copen.mtx', 'r')
lines = f.readlines()
f.close()

G = nx.Graph()


for line in lines:
    if(not line.startswith("%")):
        edge = line.rstrip().split(' ')
        if(len(edge)>1):
            if(not G.has_node(edge[0])):
                G.add_node(edge[0])
            if (not G.has_node(edge[1])):
                G.add_node(edge[1])
            G.add_edge(edge[0], edge[1])

clusterGraphs = []

for x in range(0, len(centroids)):
    Gc = nx.Graph()
    clusterGraphs.append(Gc)

nodes = list(G.nodes)

cursor = True
cycles =0

while cursor:
    cursor = False
    cycles = cycles +1
    for x in range(0, len(centroids)):
        clusterGraphs[x].clear()

#create clusters
    for node in nodes:
        minDistance = -2
        nodeCentroid = None
        for x in range(0, len(centroids)):
            distance =nx.shortest_path_length(G, node, centroids[x])
            if(minDistance>distance or minDistance == -2):
                minDistance=distance
                nodeCentroid=x

        if (not clusterGraphs[nodeCentroid].has_node(node)):
            clusterGraphs[nodeCentroid].add_node(node)

#add cluser graph edges
    for x in range(0, len(centroids)):
        cNodesL = list(clusterGraphs[x].nodes)
        for cNodeL in cNodesL:
            cNodesR = list(clusterGraphs[x].nodes)
            for cNodeR in cNodesR:
                if(not cNodesL == cNodeR):
                    if(G.has_edge(cNodeL,cNodeR)):
                        clusterGraphs[x].add_edge(cNodeL, cNodeR)


    for x in range(0, len(centroids)):
        newCentroid = nx.center(clusterGraphs[x], e=None)[0]
        if(newCentroid != centroids[x]):
            centroids[x]=nx.center(clusterGraphs[x], e=None)[0]
            cursor=True

nodeColor = []
colors = [(random(), random(), random()) for _i in range(len(centroids))]

for node in nodes:
    for x in range(0, len(centroids)):
        if(clusterGraphs[x].has_node(node)):
            nodeColor.append(colors[x])

#print results
for x in range(0, len(centroids)):
    print("Cluster " + str(x+1) + ":")
    print("Centroid :" + str(centroids[x]))
    cnodes = list(clusterGraphs[x].nodes)
    print("Nodes:")
    print(cnodes)
    print("Diameter:" + str(nx.diameter(clusterGraphs[x], e=None)))
    print(nx.info(G))
    print("\n")

#draw result graph with clusters
pos = nx.spring_layout(G,k=0.15,iterations= 50)
nx.draw(G,pos, with_labels = False,node_color=nodeColor,node_size = 50)
plt.show()

