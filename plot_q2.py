import random
import simpy
import numpy as np
import math
# from queueing.probabilities import *
from probabilities import *
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt


def conf_int(mean, var, n, p=0.95):
    pnew = (p+1)/2
    zval = st.norm.ppf(pnew)
    sigma = math.sqrt(var)
    alambda = (zval*sigma)/math.sqrt(n)
    min_lambda = mean - alambda
    plus_lambda = mean + alambda
    return min_lambda, plus_lambda

### SETTINGS
# RANDOM_SEED = 33
# SERVERS = 2 # amount of servers (n or c)
# Set RHO to a little bit smaller then 1; makes the simulation interesting
RHO = 0.9
MU = 20 # 1/mu is exponential service times
# MU > LAMBDA, if  mu = 1 and c is 1 otherwise no queue.
# 1/MU > 1/LAMBDA if c=2 or higher?
# If mu = 2, avg is every 0.5 time step is the time costs of a service.
# suppose lambda < 1
SIM_TIME = 100 # simulation time in time units

class Queue(object):
    """
    Create the initial object queue
    """

    def __init__(self, env, servers, servicetime):
        self.env = env
        self.server = simpy.Resource(env, servers)
        self.servicetime = servicetime

    def service(self, customer):
        """The process"""
        yield self.env.timeout(np.random.exponential(1/MU, 1)[0])


def customer(env, name, qu):
    """Each customer has a ``name`` and requests a server
    Subsequently, it starts a process.
    need to do sthis differently though...
    """

    global arrivals

    a = env.now
    # print(f'{name} arrives at the servicedesk at {a:.2f}')
    arrivals += 1

    with qu.server.request() as request:
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

        yield env.process(qu.service(name))
        # print('%s leaves the servicedesk at %.2f.' % (name, env.now))
        leavers += 1


def setup(env, servers, servicetime, t_inter):
    """Create a queue, a number of initial customers and keep creating customers
    approx. every 1/lambda*60 minutes."""
    # Generate queue
    queue = Queue(env, SERVERS, MU)

    # Create 1 initial customer
    # for i in range(1):
    i = 0
    env.process(customer(env, f'Customer {i}', queue))

    # Create more customers while the simulation is running
    while True:
        yield env.timeout(np.random.exponential(1/LAMBDA, 1)[0])
        i += 1
        env.process(customer(env, f'Customer {i}', queue))




# Setup and start the simulation
print('QUEUE SIMULATION\n')

# set the amount of simulations per server instellingen
SIMULATIONS = 2
print(f'Simulations: {SIMULATIONS}')


RHO_values = np.array([0.8, 0.85, 0.9, 0.95])
outcomes = []


for servers in [1, 2, 4]:
    print(f'\nServers (c): {servers}')

    mean_waiting_times = []
    lower = []
    higher = []
    for RHO in RHO_values:

        # Create dataframe to store important values to calculate statistics
        cols = ['AVG_WAITING', 'AVG_ARRIVING', 'AVG_LEAVING']
        data = pd.DataFrame(columns=cols)

        SERVERS = servers
        LAMBDA = RHO * (MU * SERVERS)  # 1/lambda is exponential inter arrival times

        # print("EXPECTED VALUES AND PROBABILITIES")

        # print(f'Rho: {RHO}\nMu: {MU}\nLambda: {LAMBDA}\nExpected interarrival time: {1 / LAMBDA:.2f} time units')
        # print(f'Expected processing time per server: {1 / MU:.2f} time units\n')
        # print(f'Probability that a job has to wait: {pwait(SERVERS, RHO):.2f}')
        # print(f'Expected waiting time E(W): {expw(MU, SERVERS, RHO):.2f} time units')
        # print(f'Expected queue length E(Lq): {expquel(SERVERS, RHO):.2f} customers\n')

        # e.g. Lambda = 3 gives 1/3 per unit in simulation time, so avg is around every 0.33 timestep a new customer occurs
        # 0.33 timestep could be 0.33 hour = 0.33*60 = 19.8 minutes (on average)

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

            rho = LAMBDA/(SERVERS*MU)
            avg_waiting = waiting_time/(counter)
            avg_arrivals = arrivals/SIM_TIME
            avg_leavers = leavers/SIM_TIME

            data.loc[s] = [avg_waiting, avg_arrivals, avg_leavers]

            # print(f'Simulation {s+1}')
            # print(f'Average waiting time: {avg_waiting:.3f} time units')
            # print(f'Avg customers arriving per time unit: {avg_arrivals:.3f} time units')
            # print(f'Avg customers leaving per time unit: {avg_leavers:.3f} time units\n')

        mean_waiting_times.append(data["AVG_WAITING"].mean())
        conf = conf_int(data["AVG_WAITING"].mean(), data["AVG_WAITING"].var(), SIMULATIONS, p=0.95)
        lower.append(conf[0])
        higher.append(conf[1])


# plot figure with confidence interval
    plt.plot(RHO_values, mean_waiting_times)
    plt.fill_between(RHO_values, lower, higher, alpha=.1, label= servers)

    plt.ylabel('Mean waiting time')

    plt.xlabel('Rho')
    plt.legend()
plt.show()


# also write to a file needs to be done
