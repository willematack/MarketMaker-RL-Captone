import numpy as np
from decimal import Decimal
import random

class QLAgent():
    def __init__(self):
        """
        epsilon:    This is the value that determines exploration vs exploitation.
                    We will see this being used in self.quote()

        actions:    The set of actions contains 2-tuples in R+ of prices between 0 and 1.
                    These will be the bid-ask spreads.

        states:     This differs from our original paper right now. Just for simplicity
                    I am setting it equal to the last volume bought.

        Q:          This is the matrix that will determine the optimal action given
                    a given state.

        """

        self.epsilon = 0.2
        amounts = np.linspace(0,1,100)
        bids = np.array([round(x,2) for x in amounts])
        asks = np.array([round(x,2) for x in amounts])
        self.actions = np.array([[i,j] for i in bids for j in asks])
        #demands = np.linspace(-100, 100, 2000)
        print('here')
        self.states = np.linspace(0, 200, 200)
        #self.states = np.array([[i,j,k] for i in demands for j in demands for k in volume])

        self.Q = np.zeros((self.states.size,self.actions.size))
        self.lastVolume = 0

    def quote(self):
        """
        If a randomly generated number between 0 and 1 is less than our set epsilon,
        the algorithm explores a random action, i.e. chooses a random bid-ask price.

        If not, the algorithm isolates the row of vectors in Q associated with the state,
        right now thats the lastVolume, and then chooses the maximum action.
        """
        if random.uniform(0,1) < self.epsilon:
            bid, ask = self.actions[int(random.uniform(0,1)*9999)]
        else:
            actionRow = self.Q[np.where(self.states==self.lastVolume)[0][0]]
            ind = np.argmax(actionRow)
            bid, ask = self.actions[ind]

        return bid,ask
