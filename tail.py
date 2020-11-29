""" long tail distribution """

import random
import simpy
import numpy as np
import math
from queueing.probabilities import *
import pandas as pd

# Settings

RHO = 0.9
MU = 1
MU_long = 5# 1/mu is exponential service times
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
        if random.uniform(0, 1) <= 0.75:
            yield self.env.timeout(np.random.exponential(1/1, 1)[0])
        else:
            yield self.env.timeout(np.random.exponential(1/5, 1)[0])


def customer(env, name, qu):
    """Each customer has a ``name`` and requests a server
    Subsequently, it starts a process.
    need to do sthis differently though...
    """

    global arrivals

    a = env.now
    print(f'{name} arrives at the servicedesk at {a:.2f}')
    arrivals += 1

    with qu.server.request() as request:
        yield request

        global counter
        global waiting_time
        global leavers

        b = env.now
        print('%s enters the servicedesk at %.2f.' % (name, b))
        waitingtime = (b - a)
        print(f'{name} waiting time was {waitingtime:.2f}')
        waiting_time += waitingtime
        counter += 1

        yield env.process(qu.service(name))
        print('%s leaves the servicedesk at %.2f.' % (name, env.now))
        leavers += 1


def setup(env, servers, servicetime, Lambda):
    """Create a queue, a number of initial customers and keep creating customers
    approx. every 1/lambda*60 minutes."""
    # Generate queue
    queue = Queue(env, servers, servicetime)

    # Create 1 initial customer
    # for i in range(1):
    i = 0
    env.process(customer(env, f'Customer {i}', queue))

    # Create more customers while the simulation is running
    while True:
        yield env.timeout(np.random.exponential(1/Lambda, 1)[0])
        i += 1
        env.process(customer(env, f'Customer {i}', queue))




# Setup and start the simulation
print('QUEUE SIMULATION\n')

SIMULATIONS = 1
print(f'Simulations: {SIMULATIONS}')

for servers in [1,2,4]:

    # Create dataframe to store important values to calculate statistics
    cols = ['AVG_WAITING', 'AVG_ARRIVING', 'AVG_LEAVING']
    data = pd.DataFrame(columns=cols)

    print(f'\nServers (c): {servers}')
    SERVERS = servers
    LAMBDA = RHO * (MU * SERVERS)  # 1/lambda is exponential inter arrival times

    print("EXPECTED VALUES AND PROBABILITIES")

    print(f'Rho: {RHO}\nMu: {MU}\nLambda: {LAMBDA}\nExpected interarrival time: {1 / LAMBDA:.2f} time units')
    print(f'Expected processing time per server: {1 / MU:.2f} time units\n')
    print(f'Probability that a job has to wait: {pwait(SERVERS, RHO):.2f}')
    print(f'Expected waiting time E(W): {expw(MU, SERVERS, RHO):.2f} time units')
    print(f'Expected queue length E(Lq): {expquel(SERVERS, RHO):.2f} customers\n')

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

    # print dataframe with data
    # print(data)
    print(f'Expected waiting time E(W): {expw(MU, SERVERS, RHO):.3f} time units')
    print(f'AVG waiting: {data["AVG_WAITING"].mean():.3f} time units')
    print(conf_int(data["AVG_WAITING"].mean(), data["AVG_WAITING"].var(), SIMULATIONS, p=0.95))
    print()
    print(f'AVG arriving: {data["AVG_ARRIVING"].mean():.3f} per time unit')
    print(conf_int(data["AVG_ARRIVING"].mean(), data["AVG_ARRIVING"].var(), SIMULATIONS, p=0.95))
    print()
    print(f'AVG leaving: {data["AVG_LEAVING"].mean():.3f} per time unit')
    print(conf_int(data["AVG_LEAVING"].mean(), data["AVG_LEAVING"].var(), SIMULATIONS, p=0.95))

print("DONE")

# Make sure we need to variate rho?
# also write to a file needs to be done