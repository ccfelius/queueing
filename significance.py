import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from scipy import stats
from queueing.probabilities import *

print("\n START MEAN, STDEV, CONF INT")
for i in [1,2,4]:
    print(f'\nServer(s): {i}')
    data = pd.read_csv(f"data/500-{i}.txt", sep="\t")
    example1 = data[data["SIM_TIME"] == 500]
    ex2 = example1[example1['RHO'] == 0.1]['AVG_WAIT']
    ex2_9 = example1[example1['RHO'] == 0.9]['AVG_WAIT']

    print("MEAN rho 0.1, rho 0.9")
    print(ex2.mean())
    print(ex2_9.mean())
    print("\nSTDEV  rho 0.1, rho 0.9")
    print(ex2.std())
    print(conf_int(ex2.mean(), ex2.var(), 500, p=0.95))
    print(ex2_9.std())
    print(conf_int(ex2_9.mean(), ex2_9.var(), 500, p=0.95))
    print("\nEXP rho 0.1, rho 0.9")
    print(expw(1,i, 0.1))
    print(expw(1,i, 0.9))

print("\nDone")
