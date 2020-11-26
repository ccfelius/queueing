import random
import simpy
import numpy as np



# RANDOM_SEED = 33
SERVERS = 2 # Amount of servers (n)
LAMBDA = 1.8  # exponential interarrival times
# e.g. Lambda = 3 gives 1/3 per unit in simulation time, so avg is around every 0.33 timestep a new customer occurs
# 0.33 timestep could be 0.33 hour = 0.33*60 = 19.8 minutes (on average)

MU = 1 # exponential service times
# MU > LAMBDA, otherwise no or barely a queue. If mu = 2, avg is every 0.5 timestep is the timecosts of a service.

SIM_TIME = 24 # simulation time in time units


class Queue(object):
    """
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
    """

    print('%s arrives at the servicedesk at %.2f.' % (name, env.now))
    with qu.server.request() as request:
        yield request

        print('%s enters the servicedesk at %.2f.' % (name, env.now))
        yield env.process(qu.service(name))

        print('%s leaves the servicedesk at %.2f.' % (name, env.now))


def setup(env, servers, servicetime, t_inter):
    """Create a queue, a number of initial customers and keep creating customers
    approx. every ``t_inter`` minutes."""

    # Create the queue system
    queue = Queue(env, SERVERS, MU)

    # Create 1 initial customer
    for i in range(3):
        env.process(customer(env, 'Customer %d' % i, queue))

    # Create more customers while the simulation is running
    while True:
        yield env.timeout(np.random.exponential(1/LAMBDA, 1)[0])
        i += 1
        env.process(customer(env, 'Customer %d' % i, queue))


# Setup and start the simulation
print('Queue Simulation')
# random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, SERVERS, MU, LAMBDA))

# Execute!
env.run(until=SIM_TIME)

rho = LAMBDA/(SERVERS*MU)

print(f'Occupation rate per server: {rho:.3f}')