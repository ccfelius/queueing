import random
import simpy
import numpy as np
import math
import pandas as pd
import scipy.stats as st

arrivals = 0


class Queue(object):
    
    """
    Create the initial object queue
    """

    def __init__(self, env, servers, servicetime):
        
        self.env = env
        self.server = simpy.Resource(env, servers)
        self.servicetime = servicetime
        self.wal_buffer = simpy.Container(env, capacity=3, init=0)  # Create the Buffer 


    def service(self, transaction, servicetime, worker, coordinator, network):
        
        """
        The process:
        each type of transaction has a different servicetime
        """
        
        if worker:
            yield self.env.timeout(np.random.exmponential(1/service_time_worker()))
        yield self.env.timeout(np.random.exponential(1/servicetime, 1)[0])


    def 


    def service_time_worker(self, cpu, connections, cpu_usage, max_txn):

        return max_txn * cpu * (1 - 1 / (connections * cpu_usage) )
        

def transaction(env, name, qu, servicetime):
    
    """
    Each transaction has a ``name`` and requests a server
    Subsequently, it starts a process.
    """

    global arrivals

    a = env.now
    print(f'{name} enters worker number at {a:.2f}')
    arrivals += 1

    with qu.server.request() as request:
        yield request

        global counter
        global waiting_time
        global leavers

        b = env.now
        print(f'%s enters the woker {qu.server} at %.2f.' % (name, b))
        waitingtime = (b - a)
        print(f'{name} waiting time was {waitingtime:.2f}')
        waiting_time += waitingtime
        counter += 1

        yield env.process(qu.service(name, servicetime))
        print('%s leaves the servicedesk at %.2f.' % (name, env.now))
        leavers += 1


def setup(env, servers, servicetime, Lambda):
    
    """Create a queue, a number of initial transactions and keep creating transactions
    approx. every 1/lambda*60 minutes."""
    
    # Generate queue
    queue = Queue(env, servers, servicetime)
    
    # for i in range(1):
    i = 0
    env.process(transaction(env, f'TXN {i}', queue, servicetime))

    # Create more transactions while the simulation is running
    while True:

        yield env.timeout(np.random.exponential(1/Lambda, 1)[0])
        i += 1
        env.process(transaction(env, f'TXN {i}', queue, servicetime))




# Setup and start the simulation
print('QUEUE SIMULATION\n')

# Set servers = 1
# set the amount of simulations
SIMULATIONS = 10
column = ['RHO', 'SIM_TIME', 'AVG_WAIT']
data_sims = []
servers =[2] # fixed
rho = 0.9

# nodes = 2
# vcores = 4
# memory = 1024
# connections = 

def calculate_worker_mu(nodes, connections):
    return int(connections/nodes)

def calculate_disk_io(mem_buffer, disk_size):

    return




MU = 0.1
SIM_TIME = 500 # 1/lambda is exponential inter arrival times

leavers = 0
for SERVERS in servers:
    LAMBDA = rho * (MU * SERVERS)
    # Create dataframe to store important values to calculate statistics
    data = pd.DataFrame(columns=column)
    for s in range(SIMULATIONS):

        waiting_time = 0
        counter = 0

        # Create an environment and start the setup process
        env = simpy.Environment()
        env.process(setup(env, SERVERS, MU, LAMBDA))

        # Execute the simulation
        env.run(until=SIM_TIME)

        avg_waiting = waiting_time/(counter)

        data.loc[s] = [rho, SIM_TIME, avg_waiting]

    data.to_csv(f'output.txt', sep='\t', index=False)
