from social_distance_network.game_env import *
from social_distance_network.network_env import *
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


def initialize_population(structure, mul_dimen, degree, group_size, group_base, group_length, dimen_l, alpha, beta):
    network, total_num, edges = generate_network(structure, mul_dimen, degree, group_size, group_base,
                                                 group_length, dimen_l, alpha, beta)
    popu = []
    for i in range(total_num):
        popu.append(Agent(i, network[i], random.randint(0, 1)))
    return popu, network, total_num, edges


# Public Goods Game
def evolution_one_step(popu, total_num, edges, r):
    for i in range(total_num):
        popu[i].set_payoffs(0)
    for i in range(total_num):
        pgg_agent = list()
        pgg_agent.append(i)
        for j in popu[i].get_link():
            pgg_agent.append(j)
        pgg_strategy = list()
        for j in pgg_agent:
            pgg_strategy.append(popu[j].get_strategy())
        pgg_payoffs = pgg_game(pgg_strategy, r)
        for k in range(len(pgg_agent)):
            j = pgg_agent[k]
            popu[j].add_payoffs(pgg_payoffs[k])

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


def run(r, structure, mul_dimen, degree, group_size, group_base, group_length, dimen_l, alpha, beta):
    run_time = 100
    popu, network, total_num, edges = initialize_population(structure, mul_dimen, degree, group_size, group_base,
                                                            group_length, dimen_l, alpha, beta)
    for _ in range(run_time):
        popu = evolution_one_step(popu, total_num, edges, r)
    return popu, network, total_num, edges


def evaluation(popu, edges, r):
    sample_time = 20
    sample_strategy = []
    total_num = len(popu)
    for _ in range(sample_time):
        popu = evolution_one_step(popu, total_num, edges, r)
        strategy = []
        for i in range(total_num):
            strategy.append(popu[i].get_strategy())
        sample_strategy.append(np.mean(strategy))
    return np.mean(sample_strategy)


if __name__ == "__main__":
    log_file_name = "./logs/log_pgg_network_my_type.txt"
    logger = create_logger(name="pgg_network_my_type", file_name=log_file_name)

    abs_path = os.path.abspath(os.path.join(os.getcwd(), './'))
    dir_name = abs_path + '/results/'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    result_file_name = dir_name + "results_pgg_network_my_type.txt"
    f = open(result_file_name, 'w')

    structure_r = "network_my_type"
    r_r = 7.0
    init_num = 10
    group_size_r = 50
    group_base_r = 2
    group_length_r = 6
    mul_dimen_r = 5
    dimen_l_r = 6
    degree_r = 8
    alpha_r = 1
    beta_r = 1
    result = []
    for _ in range(init_num):
        logger.info(_)
        popu_r, network_r, total_number_r, edges_r = run(r_r, structure_r, mul_dimen_r, degree_r, group_size_r,
                                                         group_base_r, group_length_r, dimen_l_r, alpha_r, beta_r)
        result.append(evaluation(popu_r, edges_r, r_r))
    result = np.mean(result)

    logger.info(result)
    f.write(str(result))
    f.close()