import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("data/1000sims_1000time.txt", sep="\t")


# df_mut[df_mut['nameDest'] == 'C1848904242']
example = data[data["SIM_TIME"] == 150]
ex = example[example['RHO'] == 0.9]['AVG_WAIT']
ex2 = example[example['RHO'] == 0.5]['AVG_WAIT']
ex3 = example[example['RHO'] == 0.1]['AVG_WAIT']

print(ex.std(), ex2.std(), ex3.std())

# print(ex)

plt.hist(ex, bins = 50)
plt.show()