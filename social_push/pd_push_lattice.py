import random
import math
import datetime
import os

from social_push.game_env import *
from social_push.network_env import *
from sim_env.log_file import *


class Agent:
    def __init__(self, agent_id, link, strategy):
        self.agent_id = agent_id
        self.link = link
        self.strategy = strategy
        self.ostrategy = strategy
        self.payoffs = 0
        self.reputation = 0.0

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

    def get_reputation(self):
        return self.reputation

    def set_strategy(self, other_strategy):
        self.strategy = other_strategy

    def set_ostrategy(self):
        self.ostrategy = self.strategy

    def set_payoffs(self, p):
        self.payoffs = p

    def set_reputation(self, new_rep):
        self.reputation = new_rep

    def update_reputation(self, l_r, new_rep):
        self.reputation = self.reputation + l_r * (new_rep - self.reputation)

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
    potential_agent = []
    for i in range(total_num):
        potential_agent.append(popu[i].get_link())
    w = 0.6
    for i in range(total_num):
        k = i
        while True:
            while True:
                j = random.choice(potential_agent[k])
                if j != i:
                    break
            r_i, r_j = pd_game_b(popu[i].get_strategy(), popu[j].get_strategy(), b)
            popu[i].add_payoffs(r_i)
            popu[j].add_payoffs(r_j)
            if random.random() < w and popu[i].get_strategy() == 1 and popu[j].get_strategy() == 1:
                k = j
            else:
                break
    # Backup the strategy in this round
    for i in range(total_num):
        popu[i].set_ostrategy()
    # Update strategy by imitating others' strategy
    for i in range(total_num):
        ind = popu[i]
        ind_payoffs = ind.get_payoffs()
        # while True:
        #     j = random.choice(range(total_num))
        #     if j != i:
        #         break
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
    simulation_name = "pd_push_lattice"
    log_file_name = "./logs/log_%s.txt" % simulation_name
    logger = create_logger(name=simulation_name, file_name=log_file_name)

    abs_path = os.path.abspath(os.path.join(os.getcwd(), './'))
    dir_name = abs_path + '/results/'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    result_file_name = dir_name + "results_%s.csv" % simulation_name
    f = open(result_file_name, 'w')

    for b_r in np.arange(1.0, 3.1, 0.2):
        logger.info("r value: " + str(b_r))
        init_num = 5
        result = []
        for _ in range(init_num):
            popu_r, network_r, total_numbeb_r, edges_r = run(b_r)
            result.append(evaluation(popu_r, edges_r, b_r))
        result = np.mean(result)
        logger.info("frac_co: " + str(result))
        f.write(str(b_r) + '\t' + str(result) + '\n')
    f.close()



