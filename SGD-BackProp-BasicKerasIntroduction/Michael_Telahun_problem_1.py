# **************************#
#* Michael Telahun * #
#* CECS 590-01 * #
#* Assignment 1 * #
#************************* #
import math

def sigmoid(x):
    return (1 / (1 + math.exp(-x)))

def dSigmoid(x):
    return (math.exp(-x) / math.pow(math.exp(-x) + 1, 2))

def relu(x):
    if x > 0:
        return x
    else:
        return 0

def MSE(y, yHat, n=1):
    return (math.pow((y - yHat), 2) / n)

def dMSE(y, yHat):
    return (-(y - yHat))
