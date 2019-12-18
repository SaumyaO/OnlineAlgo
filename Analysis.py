import networkx as nx
import operator
import community
import matplotlib.pyplot as plt

f = open('/Users/saumya/Downloads/socfb-nips-ego/socfb-nips-ego.edges', 'r') # input the network Dataset
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

""" To get the detail about the nodes and edges and the average degree of the graph"""

print(nx.info(G))

degree_distribution = dict(nx.degree(G))

print(degree_distribution)
sorted_DD = sorted(degree_distribution.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_DD)
plt.hist(nx.degree(G))
plt.show()

""" To get the Clustering Co-efficient of the Graph"""


clustering_coeffcicent = nx.average_clustering(G)
print("Clustering Co-efficient " + str(clustering_coeffcicent))

"""To plot the degree distribution of any graph"""

def plot_degree_dist(G):
    degrees = [G.degree(n) for n in G.nodes()]
    plt.hist(degrees)
    plt.show()

plot_degree_dist(nx.gnp_random_graph(100, 0.5, directed=True))

""" Triadic Closure is a measure of the tendency of edges in a graph to form triangles.It's a measure of the degree to which nodes in a graph tend to cluster together"""

triangles = dict(nx.triangles(G))
sum =0
for key in triangles:
    sum = sum + triangles[key]
print("Total Triangles:" + str(sum))