"""M/M/1 PRIORITY SCHEDULING (SHORTEST JOB FIRST)
This file is to collect data for a plot of the mean waiting times"""

import random
import simpy
import numpy as np
import math
from probabilities import *
import pandas as pd
import scipy.stats as st

def conf_int(mean, var, n, p=0.95):
    pnew = (p+1)/2
    zval = st.norm.ppf(pnew)
    sigma = math.sqrt(var)
    alambda = (zval*sigma)/math.sqrt(n)
    min_lambda = mean - alambda
    plus_lambda = mean + alambda
    return f"Confidence interval: [{min_lambda:.4f} < X < {plus_lambda:.4f}] with p = {p}"

### SETTINGS
# RANDOM_SEED = 33
# SERVERS = 2 # amount of servers (n or c)
# Set RHO to a little bit smaller then 1; makes the simulation interesting



class Queue(object):
    """
    Create the initial object queue
    """

    def __init__(self, env, servers, servicetime):
        self.env = env
        self.server = simpy.PriorityResource(env, servers)
        self.servicetime = servicetime

    def service(self, customer, job_length):
        """The process"""
        yield self.env.timeout(job_length)


def customer(env, name, qu, job_length):
    """Each customer has a ``name`` and requests a server
    Subsequently, it starts a process.
    need to do sthis differently though...
    """

    global arrivals

    a = env.now
    # print(f'{name} arrives at the servicedesk at {a:.2f}, job length is {job_length} time units')
    # arrivals += 1

    # priority queue job_length
    with qu.server.request(priority = job_length) as request:
        yield request

        global counter
        global waiting_time
        global leavers

        b = env.now
        # print('%s enters the servicedesk at %.2f.' % (name, b))
        waitingtime = (b - a)
        # print(f'{name} waiting time was {waitingtime:.2f}')
        waiting_time += waitingtime
        counter += 1

        yield env.process(qu.service(name, job_length))
        # print('%s leaves the servicedesk at %.2f.' % (name, env.now))
        # leavers += 1


def setup(env, servers, servicetime, t_inter):
    """Create a queue, a number of initial customers and keep creating customers
    approx. every 1/lambda*60 minutes."""

    # Generate queue
    queue = Queue(env, SERVERS, MU)

    # Create 1 initial customer
    # for i in range(1):
    i = 0
    env.process(customer(env, f'Customer {i}', queue, np.random.exponential(1/MU, 1)[0]))

    # Create more customers while the simulation is running
    while True:
        yield env.timeout(np.random.exponential(1/LAMBDA, 1)[0])
        i += 1
        env.process(customer(env, f'Customer {i}', queue, np.random.exponential(1/MU, 1)[0]))


# Setup and start the simulation
print('QUEUE SIMULATION\n')

SIMULATIONS = 500
RHO = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.975]
MU = 1 # 1/mu is exponential service times
SIM_TIME = 500 # simulation time in time units
data_sims = []

# Create dataframe to store important values to calculate statistics
column = ['RHO', 'SIM_TIME', 'AVG_WAIT']


SERVERS = 1

# print("EXPECTED VALUES AND PROBABILITIES")
# # for shortest job expected values etc differ

# print(f'Rho: {RHO}\nMu: {MU}\nLambda: {LAMBDA}\nExpected interarrival time: {1 / LAMBDA:.2f} time units')
# print(f'Expected processing time per server: {1 / MU:.2f} time units\n')
# print(f'Probability that a job has to wait: {pwait(SERVERS, RHO):.2f}')
# print(f'Expected waiting time E(W): {expw(MU, SERVERS, RHO):.2f} time units')
# print(f'Expected queue length E(Lq): {expquel(SERVERS, RHO):.2f} customers\n')


for rho in RHO:
    LAMBDA = rho * (MU * SERVERS)  # 1/lambda is exponential inter arrival times
    data = pd.DataFrame(columns=column)

    for s in range(SIMULATIONS):

        waiting_time = 0
        counter = 0
        arrivals = 0
        leavers = 0

        # Create an environment and start the setup process
        env = simpy.Environment()
        env.process(setup(env, SERVERS, MU, LAMBDA))

        # Execute the simulation
        env.run(until=SIM_TIME)

        avg_waiting = waiting_time/(counter)
        avg_arrivals = arrivals/SIM_TIME
        avg_leavers = leavers/SIM_TIME

        data.loc[s] = [rho, SIM_TIME, avg_waiting]

        # print(f'Simulation {s+1}')
        # print(f'Average waiting time: {avg_waiting:.3f} time units')
        # print(f'Avg customers arriving per time unit: {avg_arrivals:.3f} time units')
        # print(f'Avg customers leaving per time unit: {avg_leavers:.3f} time units\n')
    data_sims.append(data)

print(pd.concat(data_sims))

pd.concat(data_sims).to_csv('MMJ_SJ_1.txt', sep='\t', index=False)