import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_nodes_from(["Hi","Test"])
G.add_edges_from([("Hi","Test")])
pos = nx.spring_layout(G, scale=2)
nx.draw_networkx_edge_labels(G,pos=pos,edge_labels={("Hi","Test"):'123'},font_color='red')
nx.draw(G)
plt.show()