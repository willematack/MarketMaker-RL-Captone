from brownian import gmbrownian
from demand import demand
from agent import Agent
import numpy as np
import matplotlib.pyplot as plt
def makeAgents(agent_num):
    agents = [Agent() for i in range(agent_num)]
    return agents

def initialize(step, time, drift, volatility, initValue):
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

    price, buyOrders, sellOrders = initialize(step, time, drift, volatility, initValue)
    agents = makeAgents(agent_num)
    bid = np.zeros(agent_num)
    ask = np.zeros(agent_num)
    spread = np.zeros(agent_num)

    for i in range(len(price)):
        for j in range(agent_num):
            if i == 0:
                bid[j], ask[j] = agents[j].quote(price[i], 50, 50)
            else:
                bid[j], ask[j] = agents[j].quote(price[i], buyOrders[i-1], sellOrders[i-1])
            spread[j] = ask[j] - bid[j]
        winner = spread.argmin()

        agents[winner].cumulative_profit(spread[winner], abs(buyOrders[i]-sellOrders[i]))

    for agent in agents:
        plt.plot(agent.profit)
    plt.show()
    return agents

simulation()
