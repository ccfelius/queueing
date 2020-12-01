# queueing
queueing theory in practice


Assignment 2:  DES simulation assignment
By: Amber den Hollander (10910441) and Lotte Felius (12368032)

### Required Packages:
numpy<br>
matplotlib<br>
random<br>
time<br>
math<br>
scipy<br>
simpy<br>
pandas<br>
scipy.stats<br>


### Explanations per file

- MM2.py<br>
We this file for various experiments, including the following:
a) We can collect the data of MMC with 1, 2 and 4 servers by:
Setting RHO = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.975], SIMULATIONS = 500, SIM_TIME= 500, MU = 1 and changing SERVERS each time we run for the values 1, 2 and lastly 4.<br>
b) ...

- MM1_SJ_data.py<br> 
When executing this file we collect data of the M/M/1 queue with shortest job first scheduling with a varying rho. Using servers=2 we can compare this to M/M/2 using:  compare_124_processing.py 

- MDN_data.py<br> 
By changing servers to 1,2,4 we can analyse this data using compare_124_processing.py. Or we can have 2 servers and compare this with tail.py (also setting servers=2) using compare_2_processing.py.

- compare_124_processing.py<br>
The data of for example the MMC with 1, 2, 4 servers runs can be processed using this file. Executing this file, a plot is created of the average waiting times with 1, 2and 4 servers. 

- compare_2_processing.py<br> 
When comparing 2 types queueing this file is used. 
