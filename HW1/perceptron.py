import random
import time
import os
import math
import numpy as np
import re
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
# from sklearn import svm, datasets
# from sklearn.metrics import plot_confusion_matrix

def sigmoid(x):
    return (1 / (1 + math.exp(-x)))

def dSigmoid(x):
    return (math.exp(-x) / math.pow(math.exp(-x) + 1, 2))

def relu(x):
    if x > 0:
        return x
    else:
        return 0
    # return math.log2(1 + math.exp(x))

def MSE(y, yHat, n=1):
    return (math.pow((y - yHat), 2) / n)

# dataset = np.random.choice([0, 1], size=(100,100), p=[0.8, 1-0.8])

# # sns.load_dataset(dataset)
# # sns.barplot(dataset)
# # plt.show()

# heatmap = sns.heatmap(dataset)
# plt.show()