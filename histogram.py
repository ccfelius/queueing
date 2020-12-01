import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from scipy import stats

data = pd.read_csv("data/500-4.txt", sep="\t")

# example1 = data[data["SIM_TIME"] == 500]

simulations = 500
simtimes = [5, 50, 150, 500, 1000]

# for i in [1, 2, 4]:
#     data = pd.read_csv(f"data/500-{i}.txt", sep="\t")
#     example = data[data["SIM_TIME"] == simtime]


rhos = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.975]


print("DONE")

print("\n START MEAN, STDEV, CONF INT")

data = pd.read_csv(f"data/500-2.txt", sep="\t")
example = data[data["SIM_TIME"] == 25]
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

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='whitesmoke', axisbelow=True)
ax.hist(ex_9, bins = 100, alpha=0.5, color = 'cornflowerblue')
ax.hist(ex2_9, bins = 100, alpha = 0.6, color='springgreen')
ax.set_xlabel(r'$Mean waiting time / time unit$', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Distribution mean waiting time', fontsize = 14)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)

plt.savefig("plots/histogram-25-500.png", dpi=300)
plt.show()
