import random
import simpy
import numpy as np
import math



# RANDOM_SEED = 33
SERVERS = 2 # Amount of servers (n or c)
LAMBDA = 6  # exponential inter arrival times

# e.g. Lambda = 3 gives 1/3 per unit in simulation time, so avg is around every 0.33 timestep a new customer occurs
# 0.33 timestep could be 0.33 hour = 0.33*60 = 19.8 minutes (on average)

MU = 4 # exponential service times
# 1/MU > 1/LAMBDA, otherwise no queue. If mu = 2, avg is every 0.5 time step is the time costs of a service.

SIM_TIME = 18-9 # simulation time in time units
waiting_time = 0
i = 0

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

    a = env.now
    print(f'{name} arrives at the servicedesk at {a:.2f}')

    with qu.server.request() as request:
        yield request
        b = env.now
        print('%s enters the servicedesk at %.2f.' % (name, b))
        waitingtime = (b - a) * 60
        print(f'{name} waiting time was {waitingtime:.2f} minutes')
        global waiting_time
        waiting_time += waitingtime

        yield env.process(qu.service(name))
        print('%s leaves the servicedesk at %.2f.' % (name, env.now))


def setup(env, servers, servicetime, t_inter):
    """Create a queue, a number of initial customers and keep creating customers
    approx. every 1/lambda*60 minutes."""
    global i

    # Generate queue
    queue = Queue(env, SERVERS, MU)

    # Create 1 initial customer
    for i in range(2):
        env.process(customer(env, f'Customer {i}', queue))

    # Create more customers while the simulation is running
    while True:
        yield env.timeout(np.random.exponential(1/LAMBDA, 1)[0])
        i += 1
        env.process(customer(env, f'Customer {i}', queue))


# Setup and start the simulation
print('Queue Simulation')

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, SERVERS, MU, LAMBDA))

# Execute the simulation
env.run(until=SIM_TIME)

rho = LAMBDA/(SERVERS*MU)
avg_waiting = waiting_time/i

print(f'Occupation rate per server: {rho:.3f}')
print(f'Average waiting time: {avg_waiting:.3f} minutes')