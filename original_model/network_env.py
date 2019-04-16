import networkx as nx
import numpy as np
from tools_file.log_file import *


def generate_network(structure, xdim=100, ydim=100):
    if structure == "2d_grid":
        g_network = nx.grid_2d_graph(xdim, ydim, periodic=True)
        adj_array = nx.to_numpy_array(g_network)
        adj_link = []
        population_num = 0
        for i in range(adj_array.shape[0]):
            adj_link.append(np.where(adj_array[i] == 1)[0])
        population_num = xdim * ydim
        g_edge = nx.Graph()
        for i in range(len(adj_link)):
            for j in range(len(adj_link[i])):
                g_edge.add_edge(i, adj_link[i][j])
        return adj_link, population_num, g_edge.edges()
    else:
        return "No this type of structure"


if __name__ == "__main__":
    adj_link_r, population_num_r, g_edge_r = generate_network("2d_grid")
    logger = create_logger("game_env", file_name="./logs/log_network.txt")
    logger.debug(adj_link_r)
    logger.info(population_num_r)
    logger.info(g_edge_r)
