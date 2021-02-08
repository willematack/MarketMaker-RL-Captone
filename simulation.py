import numpy as np

from environment import Environment
from agent import Agent
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
#create environment

env = Environment(refPriceConfig)
env.updateState("new")

#create agents
agents = [Agent(0.05) for i in range(numCompetitors)]

#Run Simulation
done = False
while(not done):
    #get current state variables
    currentTimeStep = env.getCurrentTimeStep()
    price = env.getCurrentRefPrice()
    buyOrder = env.getDemand()["buy"][currentTimeStep]
    sellOrder = env.getDemand()["sell"][currentTimeStep]
    
    #get bids/asks from market maker competitors
    bid = np.zeros(numCompetitors)
    ask = np.zeros(numCompetitors)
    for i in range(numCompetitors):
        bid[i], ask[i] = agents[i].quote(price, buyOrder, sellOrder)
    sellWinner = ask.argmin()
    buyWinner = ask.argmax()
    #profit calculations
    for i in range(numCompetitors):
            agents[i].settle(sellOrder, bid[buyWinner], buyWinner, buyOrder, ask[sellWinner], sellWinner)

    

    env.updateCurrentTimeStep()
    #finish once simulation time is reached
    if(currentTimeStep > steps -1):
        done = True

#plot results


#print(env.getCurrentState())

plt.figure(0, figsize=(18, 10))


    #plot ref price
plt.subplot(121)
plt.plot(env.refPrices)
plt.grid(True)    
plt.xlabel('Timestep')
plt.ylabel('Reference Price ($)')
plt.title('Reference Price')

    #plot competitor agent performance
plt.subplot(122)
for agent in agents:
    #print(agent._id, agent.trades)
    plt.plot(agent.profit)  #plot the agents
    plt.legend([0,1,2,3,4])
plt.ylabel('Profit ($)')
plt.xlabel('Timestep')
plt.title('Agent Profit')
plt.grid(True)

#plot agent trades over time    
for i in range (len(agents)):
    plt.figure(i+1)
    plt.plot(agents[i].trades)
    plt.ylabel('Volume')
    plt.xlabel('Timestep')
    plt.title('Agent '+ str(agents[i]._id) + ' trade activity')
    plt.grid(True)
    
plt.show()
