from brownian import gmbrownian
from demand import demand
from agent import Agent
from QLAgent import QLAgent
import numpy as np
import matplotlib.pyplot as plt

def makeAgents(agent_num):
    """
    agents: an array of Agent()'s of length agent_num
    """
    agents = [Agent(0.05) for i in range(agent_num)]
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
    print(buyOrders.shape)
    print(sellOrders.shape)
    return price, buyOrders, sellOrders


def profitCalculation(agents, bid, ask, spread, price, buyOrders, sellOrders,agent_num):
    for i in range(len(price)):    #loop over every value in the array price
        for j in range(agent_num):  #For each price get the bid and ask of each agent
            bid[j], ask[j] = agents[j].quote(price[i], buyOrders[i], sellOrders[i])
        sellWinner = ask.argmin()
        buyWinner = bid.argmax()
        for j in range(agent_num):
            agents[j].settle(sellOrders[i], bid[buyWinner], buyWinner, buyOrders[i], ask[sellWinner], sellWinner)
        print('\n')


def simulation():
    step = 0.25
    time= 1000
    drift = 0.025
    volatility = 0.1
    initValue = 20
    agent_num = 5

    #get arrays
    price, buyOrders, sellOrders = initialize(step, time, drift, volatility, initValue)
    #get agents
    agents = makeAgents(agent_num)
    # qag = QLAgent()
    # agents.append(qag)
    # agent_num += 1
    #initialize the bid, ask and spread arrays
    bid = np.zeros(agent_num)
    ask = np.zeros(agent_num)
    spread = np.zeros(agent_num)

    profitCalculation(agents, bid, ask, spread, price, buyOrders, sellOrders, agent_num)


    for agent in agents:
        print(agent._id)
        print(agent.profit[-1])
        print(agent.inventory[-1])
        plt.plot(agent.profit)  #plot the agents
        plt.legend([0,1,2,3,4])
    plt.show()
    for agent in agents:
        plt.plot(agent.inventory)  #plot the agents
        plt.legend([0,1,2,3,4])
    plt.show()
    return agents

simulation()
