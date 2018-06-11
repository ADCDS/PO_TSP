import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def read_instances():
    return pd.read_csv('instances/25.csv', delimiter=',')


def draw_graph(graph, edges):

    # extract nodes from graph
    nodes = range(graph.shape[0])

    # create networkx graph
    G = nx.MultiDiGraph()

    # add nodes
    for node in nodes:
        G.add_node(node, pos=(graph.iloc[node]['x'], graph.iloc[node]['y']), label=node)

    # add edges
    for i in range(len(edges)):
        for j in range(len(edges[i])):
            if edges[i][j].solution_value != 0:
                G.add_edge(i, j)

    # draw graph
    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, labels=labels)

    # show graph
    plt.show()




def find_loops(edges):
    visited_nodes = list()
    current_node = 0

    while current_node not in visited_nodes:
        visited_nodes.append(current_node)
        for j in range(len(edges)):
            if edges[current_node][j].solution_value == 1:
                current_node = j
                break

    return visited_nodes
