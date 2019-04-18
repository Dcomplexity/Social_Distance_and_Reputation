import networkx as nx
import numpy as np
from tools_file.log_file import *


def average_degree(graph, total_num):
    degree_hist = nx.degree_histogram(graph)
    degree_sum = 0
    for i in range(len(degree_hist)):
        degree_sum += degree_hist[i] * i
    return degree_sum / total_num


def generate_network(structure, xdim=40, ydim=40, nodes_num=1600, edge_num=2):
    if structure == "2d_grid":
        g_network = nx.grid_2d_graph(xdim, ydim, periodic=True)
        adj_array = nx.to_numpy_array(g_network)
        adj_link = []
        population_num = 0
        for i in range(adj_array.shape[0]):
            adj_link.append(list(np.where(adj_array[i] == 1)[0]))
        population_num = xdim * ydim
        g_edge = nx.Graph()
        for i in range(len(adj_link)):
            for j in range(len(adj_link[i])):
                g_edge.add_edge(i, adj_link[i][j])
        return adj_link, population_num, g_edge.edges()
    elif structure == "ba_graph":
        g_network = nx.barabasi_albert_graph(n=nodes_num, m=edge_num)
        adj_array = nx.to_numpy_array(g_network)
        adj_link = []
        population_num = 0
        for i in range(adj_array.shape[0]):
            adj_link.append(list(np.where(adj_array[i] == 1)[0]))
        population_num = nodes_num
        g_edge = nx.Graph()
        for i in range(len(adj_link)):
            for j in range(len(adj_link[i])):
                g_edge.add_edge(i, adj_link[i][j])
        return adj_link, population_num, g_edge.edges()
    else:
        return "No this type of structure"


if __name__ == "__main__":
    adj_link_r, population_num_r, g_edge_r = generate_network("ba_graph")
    logger = create_logger("ba_graph", file_name="./logs/log_network.txt")
    logger.info(adj_link_r)
    logger.info(population_num_r)
    logger.info(g_edge_r)
