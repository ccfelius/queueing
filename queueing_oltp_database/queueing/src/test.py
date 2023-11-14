from simpy import *
import random
import statistics
import numpy as np
import math
import time
from collections import defaultdict
import sys

"""
This code is based on https://medium.com/swlh/simulating-a-parallel-queueing-system-with-simpy-6b7fcb6b1ca1

Bank with multiple queues example
Covers:
- Resources: Resource
- Iterating processes
Scenario:
  A multi-counter bank with a random service time and customers arrival process. Based on the
  program bank10.py from TheBank tutorial of SimPy 2. (KGM)
By Aaron Janeiro Stone
"""

class SimulateSelect(object):

    def CalculateConnectionsPerWorker(self, connections, workers):

        result = math.floor(connections/workers)

        if result > 400:
            raise Exception("Amount of connections per worker exceeds 400")
        
        return result


    def __init__(self, workers = 2, connections = 10, workload = 1000, maxTime = 10000000, factor = 1):

        """ Initializes a Simulation """

        self.workers = workers
        self.connections = connections
        self.workload = workload
        self.avg_execution_time = []
        self.avg_wait_for_worker = []
        self.last_executed = 0
        self.counters = []
        self.connections_per_worker = self.CalculateConnectionsPerWorker(connections, workers)
        self.MinPCompute = 0.12 / connections
        self.MinCCompute = 0.108 / connections
        self.MinLatency = 0.1  
        self.Latency = 0.18 
        self.ParentComputeTime = 0.29   / max(1, (self.connections - self.connections_per_worker)) # mean of compute on parent node 0.29
        self.ChildComputeTime = 0.19  / max(1, (self.connections - self.connections_per_worker)) # mean of compute on child node 0.19
        self.Queues = []
        self.maxTime = maxTime
        self.factor = factor
        self.ycsb_overhead = (self.connections ** 2) * 0.00005

        # With overhead by connections
        self.ParentComputeTime = self.SetOverhead(self.ParentComputeTime)
        self.ChildComputeTime = self.SetOverhead(self.ChildComputeTime)


    def ScaleExponentialDistribution(self, avg, minimum, set = True):

        """ Scaling the exponential distribution """

        if set:
            execution_time = (1 / self.factor) * random.expovariate(1.0 / avg)
            return max(minimum, execution_time)

        return random.expovariate(1.0 / avg)


    def GetWorkerLatency(self, parent, child):

        """ Gets latency of worker """

        # if parent is child, no latency
        if parent == child:
            return 0

        return self.ScaleExponentialDistribution(0.21, 0.12, set = False)


    def GetDriverLatency(self):

            """ returns 2x driver latency """
            
            return self.ScaleExponentialDistribution(self.Latency, self.MinLatency, set = False)


    def QueueSelector(self, d, counters):

        """ selects a queue """

        return random.sample(range(len(counters)), d)


    def LoadBalance(self, env, connection_queue):

        """ choose connection with shortest queue """

        Qlength = {i: self.NoInSystem(connection_queue[i]) for i in self.QueueSelector(1, connection_queue)}

        self.Queues.append({i: len(self.counters[i].put_queue) for i in range(len(self.counters))})

        # return connection with shortes queue
        return [k for k, v in sorted(Qlength.items(), key=lambda a: a[1])][0]


    def SetOverhead(self, mu):

        """ sets overhead caused by incoming connections from the driver node"""

        # every connection costs around 0.125% of the CPU
        # so we divide 0.125 by hundred, add 1.1 and multiply this number with the current service times.

        overhead = self.connections_per_worker * 0.125

        return overhead * mu


    def WaitForTransaction(self, env, connection_queue, i):

        """ Function that waits until transaction is finished """

        choice = self.LoadBalance(env, connection_queue)
        ycsb_overhead = random.expovariate(1.0 / self.ycsb_overhead)

        with connection_queue[choice].request() as req:

            yield req

            # get driver latency before connection actually reaches worker
            latency = self.GetDriverLatency() / 2

            now = env.now

            yield env.timeout(latency)
            
            # Connection waits until transaction is finished
            yield env.process(self.Transaction(env, 'TXN_ID_%02d' % i, i))

            # send results back to driver
            yield env.timeout(latency)

            # calculate total YCSB driver overhead
            yield env.timeout(ycsb_overhead)

            # total execution time = 2 * latency + exec_time on child node
            total = env.now - now

            self.avg_execution_time.append(total)

        self.last_executed = env.now


    def ChildCompute(self, env, child, child_compute):

        """ computes on child node """

        with self.counters[child].request() as req:

            # wait until no queue
            yield req

            # wait until child_compute is finished
            yield env.timeout(child_compute)


    def ParentCompute(self, env, parent, parent_compute):

        """ computes on parent node """

        with self.counters[parent].request() as req:

            # print(self.NoInSystem(self.counters[parent]))
            
            # wait until its your turn
            yield req

            # parent compute
            yield env.timeout(parent_compute)



    def Transaction(self, env, name, i):

        """ simulates a transaction workflow """

        # select random parent and child node
        parent = random.sample([i for i in range(self.workers)], k = 1).pop()
        child = random.sample([i for i in range(self.workers)], k = 1).pop()

        # get latency from parent to child worker node
        worker_latency = 0

        if parent is not child:
            worker_latency = self.GetWorkerLatency(parent, child) / 2
            
        # print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        parent_compute = self.ScaleExponentialDistribution(self.ParentComputeTime, self.MinPCompute, set = False) / 2
        child_compute = self.ScaleExponentialDistribution(self.ChildComputeTime, self.MinCCompute, set = False) 

        # forward to parent node
        yield env.process(self.ParentCompute(env, parent, parent_compute))
        
        # latency from forwarding to child node
        yield env.timeout(worker_latency)

        # compute on child node
        yield env.process(self.ChildCompute(env, child, child_compute))

        # latency from child to parent node
        yield env.timeout(worker_latency)

        # finish query, send back to driver
        yield env.process(self.ParentCompute(env, parent, parent_compute))


    def NoInSystem(self, R: Resource):

        """Total number of transactions in the resource R"""

        return max([0, len(R.put_queue) + len(R.users)])


    def Driver(self, env):

        """ TXN_ID = Transaction ID """
        
        # Keep track of all connections
        connection_queue = []
        
        # Compose connection queue
        for i in range(self.connections):
            connection_queue.append(Resource(env))

        # for each query in workload, allocate to a connection
        for i in range(self.workload):
            env.process(self.WaitForTransaction(env, connection_queue, i))

        env.run(until = self.maxTime)


    def GetResources(self, env, workers):

        """ returns a list of workers """

        return [Resource(env) for w in range(workers)]


    def GetThroughput(self):

        """ Returns estimated throughput in transactions per second """

        throughput = self.workload / (self.last_executed / 1000)
        
        if throughput >= self.workload:
            print(f"WARNING: Estimated throughput {throughput} is larger then workload {self.workload}")

        return throughput


    def Simulate(self):

        # Setup and start the simulation
        print(f"WORKERS: {self.workers}, CONNECTIONS: {self.connections}, WORKLOAD: {self.workload} read transactions")
        print(f"---------------------------------------------------------------------------------")
        time.sleep(1)
        print("Starting Simulation ...")

        # random.seed(seed)
        env = Environment()
        self.counters = self.GetResources(env, self.workers)
        self.Driver(env)

        print(f"Average latency from YCSB driver: {statistics.median(self.avg_execution_time)} ms")
        # print(f"AVG waiting on worker node: {statistics.median(self.avg_wait_for_worker)} ms")
        tps = self.GetThroughput()
        print(f"Troughput in Transactions per Second: {tps} TPS")
        print()

        return tps


if __name__ == "__main__":

    runs = sys.argv[1]
    results = defaultdict(list)

    for simulation in range(int(runs)):

        print(f"Simulation: {simulation + 1}")
        print()

        for w in [2, 4, 8, 16, 32]:

            ob = SimulateSelect(workers = w, connections = 800, workload = 100000)
            results[w].append(ob.Simulate())
    
    # Resulting dictionary
    print(results)