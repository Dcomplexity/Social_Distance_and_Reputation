import random
import math
import datetime
import os

from game_env import *
from network_env import *
from tools_file.log_file import *


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
    for edge in edges:
        i = edge[0]
        j = edge[1]
        r_i, r_j = pd_game_donation_game(popu[i].get_strategy(), popu[j].get_strategy(), b)
        popu[i].add_payoffs(r_i)
        popu[j].add_payoffs(r_j)
    # Backup the strategy in this round
    for i in range(total_num):
        popu[i].set_ostrategy()
    # Update strategy by imitating others' strategy
    for i in range(total_num):
        ind = popu[i]
        ind_payoffs = ind.get_payoffs()
        j = random.choice(popu[i].get_link())
        opponent = popu[j]
        opponent_payoffs = opponent.get_payoffs()
        opponent_ostrategy = opponent.get_ostrategy()
        t1 = 1 / (1 + math.e ** (10 * (ind_payoffs - opponent_payoffs)))
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
        strategy = []
        for i in range(total_num):
            strategy.append(popu[i].get_strategy())
        sample_strategy.append(np.mean(strategy))
    return np.mean(sample_strategy)


if __name__ == "__main__":
    log_file_name = "./logs/log_pd_lattice.txt"
    logger = create_logger(name="pd_lattice", file_name=log_file_name)

    abs_path = os.path.abspath(os.path.join(os.getcwd(), './'))
    dir_name = abs_path + '/results/'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    result_file_name = dir_name + "results_pd_lattice.txt"
    f = open(result_file_name, 'w')

    b_r = 2.0
    init_num = 10
    result = []
    for _ in range(init_num):
        logger.info(_)
        popu_r, network_r, total_number_r, edges_r = run(b_r)
        result.append(evaluation(popu_r, edges_r, b_r))
    result = np.mean(result)

    logger.info(result)
    f.write(str(result))
    f.close()



