import random
import math
import datetime
import os
import itertools
import pandas as pd

from sim_env.game_env import *
from sim_env.network_env import *
from sim_env.log_file import *


class Agent:
    def __init__(self, agent_id, link, strategy):
        self.agent_id = agent_id
        self.link = link
        self.strategy = strategy
        self.ostrategy = strategy
        self.payoffs = 0

    def get_id(self):
        return self.agent_id

    def get_link(self):
        return self.link

    def get_strategy(self):
        return self.strategy

    def get_ostrategy(self):
        return self.ostrategy

    def get_payoffs(self):
        return self.payoffs

    def set_strategy(self, other_strategy):
        self.strategy = other_strategy

    def set_ostrategy(self):
        self.ostrategy = self.strategy

    def set_payoffs(self, p):
        self.payoffs = p

    def add_payoffs(self, p):
        self.payoffs = self.payoffs + p


def initialize_population():
    network, total_num, edges = generate_network(structure='2d_grid')
    popu = []
    for i in range(total_num):
        popu.append(Agent(i, network[i], random.randint(0, 1)))
    return popu, network, total_num, edges


# Donation Game
def evolution_one_step(popu, total_num, edges, b):
    for i in range(total_num):
        popu[i].set_payoffs(0)
    # for edge in edges:
    #     i = edge[0]
    #     j = edge[1]
    #     r_i, r_j = pd_game_b(popu[i].get_strategy(), popu[j].get_strategy(), b)
    #     popu[i].add_payoffs(r_i)
    #     popu[j].add_payoffs(r_j)
    for i in range(total_num):
        play_agent_l = popu[i].get_link()
        for j in play_agent_l:
            r_i, r_j = pd_game_cost_b(popu[i].get_strategy(), popu[j].get_strategy(), b)
            popu[i].add_payoffs(r_i)
            popu[j].add_payoffs(r_j)
    for i in range(total_num):
        if popu[i].get_strategy() == 1 or popu[i].get_strategy() == 0:  # all will build the bridge
            neigh_agent = popu[i].get_link()
            poten_agent = []
            for j in neigh_agent:
                if popu[j].get_strategy() == 1:
                    poten_agent.append(j)
                if len(poten_agent) > 1:
                    poten_combination = itertools.combinations(poten_agent, 2)
                    for co_pair in poten_combination:
                        co_i = co_pair[0]
                        co_j = co_pair[1]
                        r_i, r_j = pd_game_b(popu[co_i].get_strategy(), popu[co_j].get_strategy(), b)
                        popu[co_i].add_payoffs(r_i)
                        popu[co_j].add_payoffs(r_j)
    # Backup the strategy in this round
    for i in range(total_num):
        popu[i].set_ostrategy()
    # Update strategy by imitating others' strategy
    for i in range(total_num):
        ind = popu[i]
        ind_payoffs = ind.get_payoffs()
        while True:
            j = random.choice(range(total_num))
            if j != i:
                break
        # j = random.choice(popu[i].get_link())
        opponent = popu[j]
        opponent_payoffs = opponent.get_payoffs()
        opponent_ostrategy = opponent.get_ostrategy()
        t1 = 1 / (1 + math.e ** (2.0 * (ind_payoffs - opponent_payoffs)))
        t2 = random.random()
        if t2 < t1:
            ind.set_strategy(opponent_ostrategy)
    return popu


def run(b):
    run_time = 100
    popu, network, total_num, edges = initialize_population()
    for _ in range(run_time):
        popu = evolution_one_step(popu, total_num, edges, b)
    return popu, network, total_num, edges


def evaluation(popu, edges, b):
    sample_time = 20
    sample_strategy = []
    total_num = len(popu)
    for _ in range(sample_time):
        popu = evolution_one_step(popu, total_num, edges, b)
        strategy_dist = [0 for _ in range(2)]
        for i in range(total_num):
            strategy_dist[popu[i].get_strategy()] += 1
        strategy_dist = np.array(strategy_dist) / total_num
        sample_strategy.append(strategy_dist)
    return np.mean(sample_strategy, axis=0)


if __name__ == "__main__":
    simulation_name = "pd_bridge_lattice"
    log_file_name = "./logs/log_%s.txt" % simulation_name
    logger = create_logger(name=simulation_name, file_name=log_file_name)

    abs_path = os.path.abspath(os.path.join(os.getcwd(), './'))
    dir_name = abs_path + '/results/'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    result_file_name = dir_name + "results_%s.csv" % simulation_name
    f = open(result_file_name, 'w')

    b_r_l = []
    result_l = []
    for b_r in np.arange(1.0, 3.1, 0.1):
        b_r = round(b_r, 2)
        b_r_l.append(b_r)
        logger.info("r value: " + str(b_r))
        init_num = 5
        result = []
        for _ in range(init_num):
            popu_r, network_r, total_num_r, edges_r = run(b_r)
            result.append(evaluation(popu_r, edges_r, b_r))
        result = np.mean(result, axis=0)
        logger.info("frac_co: " + str(result))
        result_l.append(result)
    result_pd = pd.DataFrame(result_l, index=b_r_l)
    result_pd.to_csv(f)
    f.close()



