from brownian import gmbrownian
from demand import demand
from agent import Agent
import numpy as np
import matplotlib.pyplot as plt

def makeAgents(agent_num):
    """
    agents: an array of Agent()'s of length agent_num
    """
    agents = [Agent() for i in range(agent_num)]
    return agents

def initialize(step, time, drift, volatility, initValue):
    """
    Price:  an array from time 0 to 'time' with increments of value 'step'. thus,
            it is of length time/step. Drift and volatility are the two parameters
            that geometric brownian motion needs.

    buy/sellOrders: This will generate an array of integers in between 0 and 100
                    of length time/step.
    """
    price = gmbrownian(step, time, drift, volatility, initValue)
    buyOrders, sellOrders = demand(time/step)
    return price, buyOrders, sellOrders

# def profitCalculation(agents, bid, ask, spread, price, buyOrders, sellOrders, askValue, bidValue):
#     for i in range(bidValue):
#         topBid = bidValue.argmax()
#         lowAsk = askValue.argmin()
#
#         agent[topBid].cumulative_profit = topBid*(bid[topBid].num if bid[topBid].num > buyOrders else buyOrders)
#
#         bidValue = np.delete(bidValue,topBid)
#         bid = np.delete(bid,topBid)
#         askValue = np.delete(askValue,lowAsk)
#         ask = np.delete(ask,lowAsk)
#

def simulation():
    step = 0.25
    time= 100
    drift = 0.025
    volatility = 0.1
    initValue = 20
    agent_num = 5

    #get arrays
    price, buyOrders, sellOrders = initialize(step, time, drift, volatility, initValue)
    #get agents
    agents = makeAgents(agent_num)

    #initialize the bid, ask and spread arrays
    bid = np.zeros(agent_num)
    ask = np.zeros(agent_num)
    spread = np.zeros(agent_num)

    for i in range(len(price)):    #loop over every value in the array price
        for j in range(agent_num):  #For each price get the bid and ask of each agent
            if i == 0:
                bid[j], ask[j] = agents[j].quote(price[i], 50, 50)  #if i==0, have a demand of 50,50
            else:
                bid[j], ask[j] = agents[j].quote(price[i], buyOrders[i-1], sellOrders[i-1])
            spread[j] = ask[j] - bid[j] #define the spread for each bid-ask

        winner = spread.argmin()    #this returns the index of the tightest spread

        agents[winner].cumulative_profit(spread[winner], abs(buyOrders[i]-sellOrders[i]))   #winner cashes in

    for agent in agents:
        plt.plot(agent.profit)  #plot the agents
        plt.legend([0,1,2,3,4])
    plt.show()
    return agents

simulation()
