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

        self.epsilon = 0.7
        self.gamma = 0.4
        self.alpha = 0.2
        self.profit = [0]
        amounts = np.linspace(0,1,100)
        bids = np.array([round(x,2) for x in amounts])
        asks = np.array([round(x,2) for x in amounts])
        self.action_space = np.array([[i,j] for i in bids for j in asks])
        #demands = np.linspace(-100, 100, 2000)
        self.state_space = np.linspace(-200, 200, 401)
        #self.states = np.array([[i,j,k] for i in demands for j in demands for k in volume])

        self.Q = np.zeros((self.state_space.size,self.action_space.size))

    def quote(self, price, buyOrder, sellOrder):
        """
        If a randomly generated number between 0 and 1 is less than our set epsilon,
        the algorithm explores a random action, i.e. chooses a random bid-ask price.

        If not, the algorithm isolates the row of vectors in Q associated with the state,
        right now thats the lastVolume, and then chooses the maximum action.
        """
        if random.uniform(0,1) < self.epsilon:
            bidSpread, askSpread = self.action_space[int(random.uniform(0,1)*9999)]
        else:
            row = np.where(self.state_space==(buyOrder-sellOrder))[0][0]
            actionRow = self.Q[row]
            col = np.argmax(actionRow)
            bidSpread, askSpread = self.action_space[col]

        bid = price - bidSpread
        ask = price + askSpread
        return bid, ask

    def cumulative_profit(self, spread, volume):

        self.profit.append(self.profit[-1] + round(Decimal(volume*spread),2))
        return

    def updateQ(self, bid, ask, state, nextState, won):
        newRow, newCol = self._state_max_vol(nextState)
        row, col = self._state_max_vol(state)
        self.Q[row][col] = self.Q[row][col] + self.alpha*(self.reward(state,ask-bid,won) + self.gamma*self.Q[newRow][newCol])
        return

    def _state_max_vol(self, state):
        row = np.where(self.state_space == state)[0][0]
        actionRow = self.Q[row]
        col = np.argmax(row)
        return row, col

    def reward(self, volume ,spread,won):
        if won == True:
            return volume*spread
        else:
            return 0

    def printQ(self):
        rows, cols = np.nonzero(self.Q)
        for row in rows:
            for col in cols:
                print('Q')
                print(self.Q[row][col])
                print('state')
                print(self.state_space[row])
                print('action')
                print(self.action_space[col])
        return
