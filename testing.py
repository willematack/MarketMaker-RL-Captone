from agentQ import AgentQ
import numpy as np


qConfig = {
    "epsilon": 0.7,
    "gamma": 0.4,
    "alpha": 0.2,
    "nudge": 0.5 # nudge constant for moving bid/ask spread
}
compSpread = {
            "bid": 9.5,
            "ask":12.3}

price = 10
#q value indicates the quality of an action at a particular state
#4d table [inventory][bid ratio][ask ratio][action]
'''
inventory(4): {0-50,50-100,100-150,>150}
bid ratio(10): {<-0.2, 
            -0.2:-0.15, 
            -0.15:-0.1,
            -0.1:-0.05,
            -0.05:0,
            0:0.05,
            0.05:0.1,
            0.1:0.15,
            0.15:0.2,
            >0.2,
            }
ask ratio(10): {<-0.2, 
            -0.2:-0.15, 
            -0.15:-0.1,
            -0.1:-0.05,
            -0.05:0,
            0:0.05,
            0.05:0.1,
            0.1:0.15,
            0.15:0.2,
            >0.2,
            }
actions(5):{
    "increaseBid",
    "decreaseBid", 
    "increaseAsk", 
    "decreaseAsk",
    "do nothing"}
'''

#create and shape Q tensor [inventory][bid][ask][actions]
qTable = np.random.rand(2000)
qTable = np.reshape(qTable, (4,10,10,5))

print("Testing: ")

Qagent = AgentQ(qConfig,qTable)
x = (Qagent.quote(10,compSpread))
