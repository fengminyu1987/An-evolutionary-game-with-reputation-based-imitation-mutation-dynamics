# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 23:55:15 2023

@author: 22159
"""

import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import json
import warnings
import math

warnings.filterwarnings('ignore')

n = 10000
G = nx.grid_graph((100, 100), periodic=True)
ETime = 10000
game = 'PG'
rlist = [0.1, 0.3, 0.5, 0.7, 1.0]
sigma = 0.5

# Get the strategy of the node according to s (False for cooperation, True for defection)
def fun_s(x): return random.uniform(0, 1) > x
# Calculate the fc based on the dictionary of strategy


def fun_f(x): return (len(x) - sum(list(map(lambda x: x[-1], list(x.values()))))) / len(x)


result = {}
for k in range(5):
    c = 1-rlist[k]
    r = 1+rlist[k]
    if game == "PG":
        pom = [[1, c], [r, 0]]

    Strategy = {}
    f_c = []
    rep = {}
    fit = {}

    for i in G.nodes:
        rep[i] = [1]
        fit[i] = [0]
        Strategy[i] = [fun_s(random.uniform(0, 1))]
    f_c.append(fun_f(Strategy))

    for t in range(ETime):
        print("\rc={:.1f},r={:.1f},t={:.0f},fc={:.3f}".format(
            c, r, t, f_c[t]), end='')
        for x in G.nodes:
            x_nei = list(G.neighbors(x))
            Ux = 0
            for i in x_nei:
                Ux += pom[Strategy[x][t]][Strategy[i][t]]
            if Strategy[x][t] == False:
                if rep[x][t] < 2:
                    rep[x][t] += sigma
                if rep[x][t] > 2:
                    rep[x][t] = 2
            else:
                if rep[x][t] - sigma < 0:
                    rep[x][t] = 0
                else:
                    rep[x][t] -= sigma
            rep[x].append(rep[x][t])
            fit[x][t] = (rep[x][t]) * Ux
            fit[x].append(fit[x][t])

            y = random.choice(x_nei)
            y_nei = list(G.neighbors(y))
            Uy = 0
            for i in y_nei:
                Uy += pom[Strategy[y][t]][Strategy[i][t]]
            if Strategy[y][t] == False:
                if rep[y][t] < 2:
                    rep[y][t] += sigma
                else:
                    rep[y][t] = 2
            else:
                if rep[y][t] - sigma < 0:
                    rep[y][t] = 0
                else:
                    rep[y][t] -= sigma
            fit[y][t] = (rep[y][t]) * Uy

            m = random.uniform(0, 1)
            H = {}
            if m < 0.2:
                m_p = random.uniform(0, 1)
                if m_p < 0.5:
                    Strategy[x].append(False)
                else:
                    Strategy[x].append(True)
            else:
                H = 1 / (1 + math.exp((fit[x][t]-fit[y][t])/0.7))
                if random.random() < H:
                    Strategy[x].append(Strategy[y][t])
                else:
                    Strategy[x].append(Strategy[x][t])
        f_c.append(fun_f(Strategy))
    result['c={:.1f},r={:.1f}'.format(c, r)] = f_c

json_str = json.dumps(result)
js='t_f_SL_SDG_05.json'
with open(js, 'w') as json_file:
    json_file.write(json_str)