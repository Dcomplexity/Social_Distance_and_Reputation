import numpy as np
from sim_env.log_file import *


def pd_game_donation_game(st_x, st_y, b):
    if st_x == 1 and st_y == 1:
        return b-1, b-1
    elif st_x == 1 and st_y == 0:
        return -1, b
    elif st_x == 0 and st_y == 1:
        return b, -1
    elif st_x == 0 and st_y == 0:
        return 0, 0
    else:
        return "Error"


def pd_game_c_cost_donation(st_x, st_y, b):
    if (st_x == 1 or st_x == 2) and (st_y == 1 or st_y == 2):
        return b-1, b-1
    elif (st_x == 1 or st_x == 2) and (st_y == 0):
        return -1, b
    elif (st_x == 0) and (st_y == 1 or st_y == 2):
        return b, -1
    elif (st_x == 0) and (st_y == 0):
        return 0, 0
    else:
        return "Error"


def pd_game_cost_donation(st_x, st_y, b):
    if (st_x == 2 or st_x == 3) and (st_y == 2 or st_y == 3):
        return b-1, b-1
    elif (st_x == 2 or st_x == 3) and (st_y == 0 or st_y == 1):
        return -1, b
    elif (st_x == 0 or st_x == 1) and (st_y == 2 or st_y == 3):
        return b, -1
    elif (st_x == 0 or st_x == 1) and (st_y == 0 or st_y == 1):
        return 0, 0
    else:
        return "Error"


def pd_game_b(st_x, st_y, b):
    if st_x == 1 and st_y == 1:
        return 1, 1
    elif st_x == 1 and st_y == 0:
        return 0, b
    elif st_x == 0 and st_y == 1:
        return b, 0
    elif st_x == 0 and st_y == 0:
        return 0, 0
    else:
        return "Error"


def pd_game_c_cost_b(st_x, st_y, b):
    if (st_x == 1 or st_x == 2) and (st_y == 1 or st_y == 2):
        return 1, 1
    elif (st_x == 1 or st_x == 2) and (st_y == 0):
        return 0, b
    elif (st_x == 0) and (st_y == 1 or st_y == 2):
        return b, 0
    elif (st_x == 0) and (st_y == 0):
        return 0, 0
    else:
        return "Error"


def pd_game_cost_b(st_x, st_y, b):
    if (st_x == 2 or st_x == 3) and (st_y == 2 or st_y == 3):
        return 1, 1
    elif (st_x == 2 or st_x == 3) and (st_y == 0 or st_y == 1):
        return 0, b
    elif (st_x == 0 or st_x == 1) and (st_y == 2 or st_y == 3):
        return b, 0
    elif (st_x == 0 or st_x == 1) and (st_y == 0 or st_y == 1):
        return 0, 0
    else:
        return "Error"


def pd_game_regular_value(st_x, st_y, r, s, t, p):
    if st_x == 1 and st_y == 1:
        return r, r
    elif st_x == 1 and st_y == 0:
        return s, t
    elif st_x == 0 and st_y == 1:
        return t, s
    elif st_x == 0 and st_y == 0:
        return p, p
    else:
        return "Error"


def pgg_game(st_l, r):
    agent_num = len(st_l)
    pf = np.sum(st_l) * r / agent_num
    pf_l = np.array([pf for _ in range(agent_num)]) - np.array(st_l)
    return pf_l


if __name__ == "__main__":
    pf_r = pgg_game([0, 1, 1], 2.0)
    logger = create_logger("game_env", file_name="./logs/log_game_env.txt")
    logger.info(pf_r)
    print(pf_r)
