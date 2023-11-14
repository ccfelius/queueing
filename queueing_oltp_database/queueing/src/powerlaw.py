import math
import random

x_min = 0.05
alpha = 1.1

for i in range(100):
    x = 1 - random.random()
    res = ((alpha - 1) / x_min) * (x / x_min) ** -alpha
    print(res)
