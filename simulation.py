import numpy as np

from environment import Environment
from agent import Agent
from agentQ import AgentQ
import matplotlib.pyplot as plt


#simulation configuration

step = 0.25
time = 100
steps = time/step
numCompetitors = 5 
refPriceConfig = {
    "step": step,
    "time": time,
    "drift": 0.025,
    "volatility": 0.1,
    "initValue": 20
}

#Qlearner configuration
qConfig = {
    "epsilon": 0.7,
    "gamma": 0.4,
    "alpha": 0.2,
    "nudge": 0.5 # nudge constant in $ for moving bid/ask spread
}
#initial spread will be [refprice-(refprice*delta), refprice+(refprice*delta)]

#create environment
env = Environment(refPriceConfig)
#The initial state is set up kinda sloppily, may need to fix in the future

env.updateState({
        "tightestSpread": {"bid": refPriceConfig["initValue"]-1, "ask": refPriceConfig["initValue"]+1},
        "refPrice": refPriceConfig["initValue"]
        })

#create and shape random Q tensor [inventory][bid][ask][actions]
qTable = np.random.rand(2000)
qTable = np.reshape(qTable, (4,10,10,5))

#create Q learning agent
Qagent = AgentQ(qConfig,qTable,numCompetitors)
#create competitor agents
agents = [Agent(0.05) for i in range(numCompetitors)]

#Run Simulation
done = False
while(not done):
    #get current state variables
    currentTimeStep = env.getCurrentTimeStep()
    price = env.getCurrentRefPrice()
    buyOrder = env.getDemand()["buy"][currentTimeStep]
    sellOrder = env.getDemand()["sell"][currentTimeStep]

    #spreads for competitors and Qlearner
    bid = np.zeros(numCompetitors+1)
    ask = np.zeros(numCompetitors+1)

    
    #get bids/asks from market maker competitors
    for i in range(numCompetitors):
        bid[i], ask[i] = agents[i].quote(price, buyOrder, sellOrder)
    
    #get bid/ask from qlearner (with bid/ask from last timestep)

    competitorSpread = {
        "bid":env.states[-1]["tightestSpread"]["bid"],
        "ask":env.states[-1]["tightestSpread"]["ask"],
    }
    bid[-1], ask[-1] = Qagent.quote(price,competitorSpread)
    
    #profit calc for learner
    sellWinner = ask.argmin()
    buyWinner = bid.argmax()
    #profit calculations for each agent
    for i in range(numCompetitors):
            agents[i].settle(sellOrder, bid[buyWinner], buyWinner, buyOrder, ask[sellWinner], sellWinner)
    Qagent.settle(sellOrder, bid[buyWinner], buyWinner, buyOrder, ask[sellWinner], sellWinner)
    env.updateState({
        "tightestSpread": {"bid": max(bid), "ask": min(ask)},
        "refPrice": price
        })
    
    env.updateCurrentTimeStep()
    #finish once simulation time is reached
    if(currentTimeStep > steps -1):
        done = True

#plot results
def plotResults():
    plt.figure(0, figsize=(18, 10))
    
    #plot ref price over time
    plt.subplot(121)
    plt.plot(env.refPrices)
    plt.grid(True)    
    plt.xlabel('Timestep')
    plt.ylabel('Reference Price ($)')
    plt.title('Reference Price')

    #plot competitor agent performance
    plt.subplot(122)
    for agent in agents:
        plt.plot(agent.profit)  #plot the agents
        plt.legend(["0","1","2","3","4","Q"])

    plt.plot(Qagent.profit)
    plt.ylabel('Profit ($)')
    plt.xlabel('Timestep')
    plt.title('Agent Profit over time')
    plt.grid(True)

    #plot agent trades over time    
    for i in range (len(agents)):
        plt.figure(i+1)
        plt.plot(agents[i].trades)
        plt.ylabel('Volume')
        plt.xlabel('Timestep')
        plt.title('Agent '+ str(agents[i]._id) + ' trade activity')
        plt.grid(True)
    #plot Qlearner
    plt.figure(7)
    plt.plot(Qagent.trades)
    plt.ylabel('Volume')
    plt.xlabel('Timestep')
    plt.title('QL Agent trade activity')
    plt.grid(True)
    plt.show()


plotResults()

