# imports
import math


def calc_rho(mu, lbda, c):
    return lbda/(c*mu)


def pwait(c, rho):
    """
    Probability that a job has to wait

    :param c: amount of servers
    :param rho: occupation rate per server
    :return: probability
    """
    fixed = ((c*rho)**c)/math.factorial(c)

    sum = 0
    for n in range(c):
        sum += ((c*rho)**n)/math.factorial(n)

    return fixed/((1-rho)*sum + fixed)


def expw(mu, c, rho):
    """
    Expected waiting time

    :param mu: server processing time
    :param c: amount of servers
    :param rho: occupation rate per server
    :return: Exp. waiting time
    """

    piw = pwait(c, rho)
    return piw * (1/(1-rho)) * 1/(c*mu)

def expquel(c, rho):
    """
    Expected queue length

    :param c: amount of servers
    :param rho: occupation rate per server
    :return: Exp. queue length
    """
    piw = pwait(c, rho)
    return piw * (rho/(1-rho))

# print(f'Probability that a job has to wait: {pwait(c, rho):.2f}')
# print(f'Expected waiting time E(W): {expw(mu, c, rho):.2f} time units')
# print(f'Expected queue length E(Lq): {expquel(c, rho):.2f} customers')