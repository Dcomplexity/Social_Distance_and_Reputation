from tools_file.log_file import *
from social_distance_network.network_build import *


def generate_network(structure, mul_dimen, degree, group_size, group_base, group_length, dimen_l, alpha, beta):
    if structure == "network_my_type":
        g_network = generate_network_connected(mul_dimen, degree, group_size, group_base, group_length, dimen_l, alpha)
        if g_network != None:
            adj_array = nx.to_numpy_array(g_network)
            adj_link = []
            for i in range(adj_array.shape[0]):
                adj_link.append(list(np.where(adj_array[i] == 1)[0]))
            population_num = group_size * (group_base ** (group_length - 1))
            g_edge = nx.Graph()
            for i in range(len(adj_link)):
                for j in range(len(adj_link[i])):
                    g_edge.add_edge(i, adj_link[i][j])
            return adj_link, population_num, g_edge.edges()
        else:
            return "Can not build a connected network"
    elif structure == "network_in_paper":
        g_network = generate_network_in_paper_connected(mul_dimen, degree, group_size, group_base, group_length, alpha, beta)
        if g_network != None:
            adj_array = nx.to_numpy_array(g_network)
            adj_link = []
            for i in range(adj_array.shape[0]):
                adj_link.append(list(np.where(adj_array[i] == 1)[0]))
            population_num = group_size * (group_base ** (group_length - 1))
            g_edge = nx.Graph()
            for i in range(len(adj_link)):
                for j in range(len(adj_link[i])):
                    g_edge.add_edge(i, adj_link[i][j])
            return adj_link, population_num, g_edge.edges()
        else:
            return "Can not build a connected network"
    elif structure == "network_hete":
        g_network = generate_hete_network_connected(mul_dimen, degree, group_size, group_base, group_length, alpha)
        if g_network != None:
            adj_array = nx.to_numpy_array(g_network)
            adj_link = []
            for i in range(adj_array.shape[0]):
                adj_link.append(list(np.where(adj_array[i] == 1)[0]))
            population_num = group_size * (group_base ** (group_length - 1))
            g_edge = nx.Graph()
            for i in range(len(adj_link)):
                for j in range(len(adj_link[i])):
                    g_edge.add_edge(i, adj_link[i][j])
            return adj_link, population_num, g_edge.edges()
        else:
            return "Can not build a connected network"
    elif structure == "er_random":
        g_network = generate_er_random_connected(mul_dimen, degree, group_size, group_base, group_length, dimen_l, alpha, beta)
        if g_network != None:
            adj_array = nx.to_numpy_array(g_network)
            adj_link = []
            for i in range(adj_array.shape[0]):
                adj_link.append(list(np.where(adj_array[i] == 1)[0]))
            population_num = group_size * (group_base ** (group_length - 1))
            g_edge = nx.Graph()
            for i in range(len(adj_link)):
                for j in range(len(adj_link[i])):
                    g_edge.add_edge(i, adj_link[i][j])
            return adj_link, population_num, g_edge.edges()
    else:
        return "No this type of structure"


if __name__ == "__main__":
    group_size_r = 10
    group_base_r = 2
    group_length_r = 10
    mul_dimen_r = 5
    dimen_l_r = 1
    degree_r = 8
    alpha_r = -1
    beta_r = -1
    total_num_r = group_size_r * (group_base_r ** (group_length_r - 1))
    adj_link_r, population_num_r, g_edge_r = generate_network("er_random", mul_dimen_r, degree_r, group_size_r,
                                                              group_base_r, group_length_r, dimen_l_r, alpha_r, beta_r)
    logger = create_logger("er_random", file_name="./logs/log_network.txt")
    logger.info(adj_link_r)
    logger.info(population_num_r)
    logger.info(g_edge_r)
