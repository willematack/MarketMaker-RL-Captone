import numpy as np

from environment import Environment
from agent import Agent


#simulation configuration

step = 0.25
time = 1000
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
    for i in range(numCompetitors):
            agents[i].settle(sellOrder, bid[buyWinner], buyWinner, buyOrder, ask[sellWinner], sellWinner)

    

    env.updateCurrentTimeStep()
    #finish once simulation time is reached
    if(currentTimeStep > steps -1):
        done = True

#plot results

print(env.getCurrentState())

