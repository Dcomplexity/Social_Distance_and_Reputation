import random
import math
import datetime
import os
import itertools
import pandas as pd

import sys
sys.path.append("..")

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
        popu.append(Agent(i, network[i], np.random.choice([0, 1, 2, 3])))  #  3 for random individual
    return popu, network, total_num, edges


# Donation Game
def evolution_one_step(popu, total_num, edges, b, cost):
    for i in range(total_num):
        popu[i].set_payoffs(0)
    # for edge in edges:
    #     i = edge[0]
    #     j = edge[1]
    #     r_i, r_j = pd_game_cost_b(popu[i].get_strategy(), popu[j].get_strategy(), b)
    #     popu[i].add_payoffs(r_i)
    #     popu[j].add_payoffs(r_j)
    for i in range(total_num):
        play_agent_l = popu[i].get_link()
        for j in play_agent_l:
            i_action = popu[i].get_strategy()
            j_action = popu[j].get_strategy()
            if popu[i].get_strategy() == 3:
                if random.random() < 0.5:
                    i_action = 0
                else:
                    i_action = 1
            if popu[j].get_strategy() == 3:
                if random.random() < 0.5:
                    j_action = 0
                else:
                    j_action = 1
            r_i, r_j = pd_game_c_cost_b(i_action, j_action, b)
            popu[i].add_payoffs(r_i)
            popu[j].add_payoffs(r_j)
    for i in range(total_num):
        if popu[i].get_strategy() == 2:
            neigh_agent = popu[i].get_link()
            poten_agent = []
            for j in neigh_agent:
                if popu[j].get_strategy() == 1 or popu[j].get_strategy() == 2:
                    poten_agent.append(j)
                if len(poten_agent) > 1:
                    poten_combination = itertools.combinations(poten_agent, 2)
                    for co_pair in poten_combination:
                        popu[i].add_payoffs(-cost)
                        co_i = co_pair[0]
                        co_j = co_pair[1]
                        co_i_action = popu[co_i].get_strategy()
                        co_j_action = popu[co_j].get_strategy()
                        if popu[co_i].get_strategy() == 3:
                            if random.random() < 0.5:
                                co_i_action = 0
                            else:
                                co_i_action = 1
                        if popu[co_j].get_strategy() == 3:
                            if random.random() < 0.5:
                                co_j_action = 0
                            else:
                                co_j_action = 1
                        r_i, r_j = pd_game_c_cost_b(co_i_action, co_j_action, b)
                        popu[co_i].add_payoffs(r_i)
                        popu[co_j].add_payoffs(r_j)
    # Backup the strategy in this round
    for i in range(total_num):
        popu[i].set_ostrategy()
    # Update strategy by imitating others' strategy
    for i in range(total_num):
        ind = popu[i]
        w1 = 0.01
        w2 = random.random()
        if w2 < w1:
            potential_strategy = [0, 1, 2, 3]
            potential_strategy.remove(ind.get_ostrategy())
            ind.set_strategy(np.random.choice(potential_strategy))
        else:
            ind_payoffs = ind.get_payoffs()
            # while True:
            #     j = random.choice(range(total_num))
            #     if j != i:
            #         break
            j = random.choice(popu[i].get_link())
            opponent = popu[j]
            opponent_payoffs = opponent.get_payoffs()
            opponent_ostrategy = opponent.get_ostrategy()
            t1 = 1 / (1 + math.e ** (2.0 * (ind_payoffs - opponent_payoffs)))
            t2 = random.random()
            if t2 < t1:
                ind.set_strategy(opponent_ostrategy)
    return popu


def run(b, cost, run_time):
    run_time = run_time
    popu, network, total_num, edges = initialize_population()
    for _ in range(run_time):
        popu = evolution_one_step(popu, total_num, edges, b, cost)
    return popu, network, total_num, edges


def evaluation(popu, edges, b, cost, sample_time):
    sample_time = sample_time
    sample_strategy = []
    total_num = len(popu)
    for _ in range(sample_time):
        popu = evolution_one_step(popu, total_num, edges, b, cost)
        strategy_dist = [0 for _ in range(4)]
        for i in range(total_num):
            strategy_dist[popu[i].get_strategy()] += 1
        strategy_dist = np.array(strategy_dist) / total_num
        sample_strategy.append(strategy_dist)
    # return np.mean(sample_strategy, axis=0)
    return sample_strategy


if __name__ == "__main__":
    simulation_name = "pd_c_cost_b_random_ind_lattice"
    log_file_name = "./logs/log_%s.txt" % simulation_name
    logger = create_logger(name=simulation_name, file_name=log_file_name)

    abs_path = os.path.abspath(os.path.join(os.getcwd(), './'))
    dir_name = abs_path + '/results/'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    result_file_name = dir_name + "results_%s.csv" % simulation_name
    f = open(result_file_name, 'w')

    run_time_r = 800
    sample_time_r = 200
    init_num = 10
    cost_r_l = []
    for i in np.arange(0.0, 1.01, 0.1):
        cost_r_l.append(round(i, 2))
    b_r_l = []
    for i in np.arange(1.0, 3.01, 0.1):
        b_r_l.append(round(i, 2))
    result_l = []
    for cost_r in cost_r_l:
        for b_r in b_r_l:
            logger.info('cost value: ' + str(cost_r))
            logger.info("b value: " + str(b_r))
            result = []
            for _ in range(init_num):
                popu_r, network_r, total_num_r, edges_r = run(b_r, cost_r, run_time_r)
                #result.append(evaluation(popu_r, edges_r, b_r, cost_r))
                sample_result = evaluation(popu_r, edges_r, b_r, cost_r, sample_time_r)
                for sample_i in sample_result:
                    result_l.append(sample_i)
            # result = np.mean(result, axis=0)
            # logger.info("frac_co: " + str(result))
            # result_l.append(result)
    init_num_l = list(range(init_num))
    sample_l = list(range(sample_time_r))  # 200 for sample time
    m_index = pd.MultiIndex.from_product([cost_r_l, b_r_l, init_num_l, sample_l], names=['cost', 'b', 'init', 'sample'])
    result_pd = pd.DataFrame(result_l, index=m_index)
    result_pd.to_csv(f)
    f.close()



