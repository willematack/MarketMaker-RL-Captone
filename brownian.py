import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

def gmbrownian(step, time, drift, volatility, initValue):
    iter = int(time/step)
    price = np.zeros(iter)
    dist=np.random.standard_normal(size=iter)
    t = np.linspace(0, time, iter)
    br = np.cumsum(dist)*sqrt(step)
    price = initValue + (drift-0.5*(volatility**2))*t + volatility*br
    return price
