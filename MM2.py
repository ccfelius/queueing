import random
import simpy
import numpy as np



# RANDOM_SEED = 33
SERVERS = 2  # Amount of servers (n)
LAMBDA = 3  # interarrival times
SERVICETIME = 3
SIM_TIME = 60     # Simulation time in minutes


class Queue(object):
    """
    """
    def __init__(self, env, servers, servicetime):
        self.env = env
        self.server = simpy.Resource(env, servers)
        self.servicetime = servicetime

    def service(self, customer):
        """The process"""
        yield self.env.timeout(np.random.poisson(SERVICETIME, 1)[0])


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
    queue = Queue(env, SERVERS, SERVICETIME)

    # Create 1 initial customer
    for i in range(3):
        env.process(customer(env, 'Customer %d' % i, queue))

    # Create more customers while the simulation is running
    while True:
        yield env.timeout(np.random.poisson(LAMBDA, 1)[0])
        i += 1
        env.process(customer(env, 'Customer %d' % i, queue))


# Setup and start the simulation
print('Queue Simulation')
# random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, SERVERS, SERVICETIME, LAMBDA))

# Execute!
env.run(until=SIM_TIME)