import numpy.random as np
import matplotlib.pyplot as plt

def demand(Size):
    buy = np.standard_normal(size=int(Size))*50
    sell = np.standard_normal(size=int(Size))*50
    return buy, sell
