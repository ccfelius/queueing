""" with this file the mean waiting times of MM1/ MMc are plotted """
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from scipy import stats

simulations = 500
simtime = 500

s1 = []
s2 = []
s4 = []
s1_dev = []
s2_dev = []
s4_dev = []
rhos= [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.975]



for i in [1, 2]:
    data = pd.read_csv(f"data/MM1SJS_{i}.txt", sep="\t")
    example = data[data["SIM_TIME"] == simtime]

    for r in rhos:
        if i == 1:
            s1.append(example[example['RHO'] == r]['AVG_WAIT'].mean())
            s1_dev.append(1.96 * example[example['RHO'] == r]['AVG_WAIT'].std() /
                          math.sqrt(simulations))
        elif i == 2:
            s2.append(example[example['RHO'] == r]['AVG_WAIT'].mean())
            s2_dev.append(1.96 * example[example['RHO'] == r]['AVG_WAIT'].std() /
                          math.sqrt(simulations))
        else:
            s4.append(example[example['RHO'] == r]['AVG_WAIT'].mean())
            s4_dev.append(1.96 * example[example['RHO'] == r]['AVG_WAIT'].std() /
                          math.sqrt(simulations))


fig, ax = plt.subplots()
ax.plot(rhos, s1, color="lightskyblue", label="MM1")
ax.plot(rhos, s2, color="deeppink", label="MM1 shortest first")
ax.fill_between(rhos, [a - b for a, b in zip(s1, s1_dev)], [a + b for a, b in zip(s1, s1_dev)], color='lightskyblue', alpha=.1)
ax.fill_between(rhos, [a - b for a, b in zip(s2, s2_dev)], [a + b for a, b in zip(s2, s2_dev)], color='deeppink', alpha=.1)
plt.legend()
plt.ylabel('Mean waiting time (time units)')
plt.xlabel('ρ')
plt.savefig("MM1_SJ.png", dpi=300)
plt.show()

print("DONE")

print("\n START MEAN, STDEV, CONF INT")
for i in [1,2,4]:
    print(f'Server(s): {i}')
    data = pd.read_csv(f"data/sim_tim_500_n{i}.txt", sep="\t")
    example = data[data["SIM_TIME"] == 150]
    example1 = data[data["SIM_TIME"] == 500]
    ex = example[example['RHO'] == 0.1]['AVG_WAIT']
    ex2 = example1[example1['RHO'] == 0.1]['AVG_WAIT']
    ex_9 = example[example['RHO'] == 0.9]['AVG_WAIT']
    ex2_9 = example1[example1['RHO'] == 0.9]['AVG_WAIT']

    print("\nMEAN 150, 500, rho 0.1, rho 0.9")
    print(ex.mean(), ex2.mean())
    print(ex_9.mean(), ex2_9.mean())
    print("\nSTDEV 150, 500, rho 0.1, rho 0.9")
    print(ex.std(), ex2.std())
    print(ex_9.std(), ex2_9.std())

# print(stats.chisquare(f_obs=ex, f_exp=ex2))

# print(ex)

# plt.hist(ex2, bins = 50)
# plt.show()