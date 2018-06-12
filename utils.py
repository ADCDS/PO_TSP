import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def read_instances():
    return pd.read_csv('instances/75.csv', delimiter=',')


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
            # if edges[i][j].solution_value != 0:
            if edges[i][j].solution_value != 0:
                G.add_edge(i, j)

    # draw graph
    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, labels=labels)

    # show graph
    plt.show()


def find_loops(edges):
    visited_nodes = list(list())
    unvisited_nodes = list(range(len(edges)))

    i = 0
    while len(unvisited_nodes) > 0:
        current_node = unvisited_nodes[0]
        visited_nodes.append(list())

        while current_node not in visited_nodes[i]:
            unvisited_nodes.remove(current_node)
            visited_nodes[i].append(current_node)

            for j in range(len(edges)):
                # if edges[current_node][j].solution_value == 1:
                if edges[current_node][j] != 0:
                    current_node = j
                    break
        i += 1

    return visited_nodes
