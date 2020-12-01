import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from scipy import stats
from queueing.probabilities import *

data = pd.read_csv("data/500-4.txt", sep="\t")

# example1 = data[data["SIM_TIME"] == 500]

simulations = 500
simtimes = [5, 50, 150, 500, 1000]

# for i in [1, 2, 4]:
#     data = pd.read_csv(f"data/500-{i}.txt", sep="\t")
#     example = data[data["SIM_TIME"] == simtime]


st_5 = []
st_50 = []
st_150 = []
st_500 = []
st_1000 = []

sim_5 = []
sim_50 = []
sim_150 = []
sim_500 = []
sim_1000 = []

expected = []
for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.975]:
    expected.append(expw(1, 2, i))

for simtime in simtimes:
    data = pd.read_csv(f"data/1000-2.txt", sep="\t")
    example = data[data["SIM_TIME"] == simtime]

    for r in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.975]:
        if simtime == 5:
            sim_5.append(example[example['RHO'] == r]['AVG_WAIT'].mean())
            st_5.append(1.96 * example[example['RHO'] == r]['AVG_WAIT'].std() /
                          math.sqrt(simulations))
        elif simtime == 50:
            sim_50.append(example[example['RHO'] == r]['AVG_WAIT'].mean())
            st_50.append(1.96 * example[example['RHO'] == r]['AVG_WAIT'].std() /
                          math.sqrt(simulations))
        elif simtime == 150:
            sim_150.append(example[example['RHO'] == r]['AVG_WAIT'].mean())
            st_150.append(1.96 * example[example['RHO'] == r]['AVG_WAIT'].std() /
                          math.sqrt(simulations))
        elif simtime == 500:
            sim_500.append(example[example['RHO'] == r]['AVG_WAIT'].mean())
            st_500.append(1.96 * example[example['RHO'] == r]['AVG_WAIT'].std() /
                          math.sqrt(simulations))
        else:
            sim_1000.append(example[example['RHO'] == r]['AVG_WAIT'].mean())
            st_1000.append(1.96 * example[example['RHO'] == r]['AVG_WAIT'].std() /
                          math.sqrt(simulations))


rhos = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.975]


fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='whitesmoke', axisbelow=True)
ax.plot(rhos, sim_5, 'cornflowerblue', alpha=1, lw=2, label='Simtime=5')
ax.plot(rhos, sim_50, 'deeppink', alpha=0.8, lw=2, label='Simtime=50')
ax.plot(rhos, sim_150, 'springgreen', alpha=0.6, lw=2, label='Simtime=150')
ax.plot(rhos, sim_500, 'black', alpha=0.6, lw=2, label='Simtime=500')
ax.plot(rhos, sim_1000, 'grey', alpha=0.6, lw=2, label='Simtime=1000')
ax.plot(rhos, expected, 'black', alpha=1, lw=2, label='Expected Waiting Time')

ax.fill_between(rhos, [a - b for a, b in zip(sim_5, st_5)], [a + b for a, b in zip(sim_5, st_5)], color='cornflowerblue', alpha=.1)
ax.fill_between(rhos, [a - b for a, b in zip(sim_50, st_50)], [a + b for a, b in zip(sim_50, st_50)], color='deeppink', alpha=.1)
ax.fill_between(rhos, [a - b for a, b in zip(sim_150, st_150)], [a + b for a, b in zip(sim_150, st_150)], color='springgreen', alpha=.1)
ax.fill_between(rhos, [a - b for a, b in zip(sim_500, st_500)], [a + b for a, b in zip(sim_500, st_500)], color='black', alpha=.1)
ax.fill_between(rhos, [a - b for a, b in zip(sim_1000, st_1000)], [a + b for a, b in zip(sim_1000, st_1000)], color='grey', alpha=.1)

ax.set_xlabel(r'$\rho$', fontsize=12)
ax.set_ylabel('Waiting time / time unit', fontsize=12)
ax.set_title('Mean waiting time', fontsize = 14)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)

plt.savefig("plots/simtimes-exp.png", dpi=300)
plt.show()

# plt.title(f"Mean waiting time (Simtime={simtime})", fontsize=16)
# plt.legend()
# plt.grid(True)
# plt.xlabel(r"$\rho$")
# plt.ylabel("Waiting time / time unit")
# plt.savefig("plots/simtimes.png")
# plt.show()

print("DONE")

print("\n START MEAN, STDEV, CONF INT")
for i in [1,2,4]:
    print(f'Server(s): {i}')
    data = pd.read_csv(f"data/500-{i}.txt", sep="\t")
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
