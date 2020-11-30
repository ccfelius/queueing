import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("data/test2.txt", sep="\t")


# df_mut[df_mut['nameDest'] == 'C1848904242']
example = data[data["SIM_TIME"] == 5]
ex = example[example['RHO'] == 0.9]['AVG_WAIT']

print(ex)

plt.hist(ex, bins = 50)
plt.show()