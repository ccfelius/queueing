import random
import simpy
import numpy as np
import math
import pandas as pd
import scipy.stats as st
from numpy import random

SIM_DURATION = 100

class Network(object):

    """This class represents the propagation through a network"""

    def __init__(self, env, delay):
        self.env = env
        self.delay = random.zipf()
        self.store = simpy.Store(env)

    def latency(self, value):
        yield self.env.timeout(self.delay)
        self.store.put(value)

    def put(self, value):
        self.env.process(self.latency(value))

    def get(self):
        return self.store.get()


def sender(env, cable):

    """A process which randomly generates messages."""
    while True:
        # wait for next transmission
        yield env.timeout(1)
        cable.put('Sender sent this at %d' % env.now)


def receiver(env, cable):

    """A process which consumes messages."""
    while True:
        # Get event for message pipe
        msg = yield cable.get()
        print('Received this at %d while %s' % (env.now, msg))


# Setup and start the simulation
print('Event Latency')
env = simpy.Environment()

cable = Network(env, 1)
env.process(sender(env, cable))
env.process(receiver(env, cable))

env.run(until=SIM_DURATION)


# # Setup and start the simulation
# print('QUEUE SIMULATION\n')

# # Set servers = 1
# # set the amount of simulations
# SIMULATIONS = 10
# column = ['RHO', 'SIM_TIME', 'AVG_WAIT']
# data_sims = []
# servers =[1,2,4] # fixed
# rho = 0.9
# MU = 1
# SIM_TIME = 500 # 1/lambda is exponential inter arrival times
# leavers = 0
# for SERVERS in servers:
#     LAMBDA = rho * (MU * SERVERS)
#     # Create dataframe to store important values to calculate statistics
#     data = pd.DataFrame(columns=column)
#     for s in range(SIMULATIONS):

#         waiting_time = 0
#         counter = 0

#         # Create an environment and start the setup process
#         env = simpy.Environment()
#         env.process(setup(env, SERVERS, MU, LAMBDA))

#         # Execute the simulation
#         env.run(until=SIM_TIME)

#         avg_waiting = waiting_time/(counter)

#         data.loc[s] = [rho, SIM_TIME, avg_waiting]

#     data.to_csv(f'output.txt', sep='\t', index=False)
