import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from scipy import stats
from queueing.probabilities import *

simtime = 5000
rho = 0.9

print("\n START MEAN, STDEV, CONF INT")
for i in [1,2,4]:
    print(f'\nServer(s): {i}')
    data = pd.read_csv(f"data/s{simtime}-{i}.txt", sep="\t")
    example1 = data[data["SIM_TIME"] == simtime]
    ex2_9 = example1[example1['RHO'] == rho]['AVG_WAIT']

    print("MEAN rho 0.9, sim=5000")
    print(ex2_9.mean())
    print("\nSTDEV, conf int rho 0.9, sim = 5000")
    print(ex2_9.std())
    print(conf_int(ex2_9.mean(), ex2_9.var(), 500, p=0.95))
    print("\nEXP rho 0.9")
    print(expw(1,i, 0.9))

print("\nDone")
