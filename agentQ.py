import numpy as np
from decimal import Decimal
import random

class AgentQ():
    # actions [increase ask, reduce ask, increase bid, reduce bid, do nothing] by some constant
    # may want to explore nudging by some ratio instead of constant 

    #states q = QLearner, c = competitor 
    # [(qbid-cbid)/refprice][(qask-cask)/refprice][inventory]

    def __init__(self, configuration, initialQTable,numCompetitors):
       #config Q-learning params
        self._id = numCompetitors
        self.qLearningConfig = configuration
        self.spread = [] # 2d array -> bid,ask at timestep
        self.profit=[0]
        self.inventory = [0]
        self.trades = [] #record of trade with volume at each timestep 
        self.states = [] # OBSERVED States indexes (inventory,bidratio,askratio)
        self.actions = [] #keep track of each action taken and the q value for that action
        self.rewards = [] #rewards array
        self.qTable = initialQTable #the agent will be re-created each episode, but the final qtable at the end of each episode should persist
        return
    def selectStateIndex(self,inventory,bidRatio,askRatio):
        '''
        The right way to do this is probably to make a range dictionary csv 
        and then import it to this file. I looked up some other ways and got lazy.
        Python also doesnt even have built in switch statements, crazy 
        '''
        #inventory
        if(inventory <= 50):
            inventoryIndex =0
        elif(inventory >50 and inventory <=100):
            inventoryIndex=1
        elif(inventory >100 and inventory <=150):
            inventoryIndex=2
        else:
            inventoryIndex=3
        #bid ratio
        if(bidRatio <= -0.2):
            bidIndex =0
        elif(bidRatio >-0.2 and bidRatio <=-0.15):
            bidIndex=1
        elif(bidRatio >-0.15 and bidRatio <=-0.1):
            bidIndex=2
        elif(bidRatio >-0.1 and bidRatio <=-0.05):
            bidIndex=3
        elif(bidRatio >-0.05 and bidRatio <=0):
            bidIndex=4
        elif(bidRatio >0 and bidRatio <=0.05):
            bidIndex=5
        elif(bidRatio >0.05 and bidRatio <=0.1):
            bidIndex=6
        elif(bidRatio >0.1 and bidRatio <=0.15):
            bidIndex=7
        elif(bidRatio >0.15 and bidRatio <=0.2):
            bidIndex=8    
        else:
            bidIndex=9
        #ask ratio
        if(askRatio <= -0.2):
            askIndex =0
        elif(askRatio >-0.2 and askRatio <=-0.15):
            askIndex=1
        elif(askRatio >-0.15 and askRatio <=-0.1):
            askIndex=2
        elif(askRatio >-0.1 and askRatio <=-0.05):
            askIndex=3
        elif(askRatio >-0.05 and askRatio <=0):
            askIndex=4
        elif(askRatio >0 and askRatio <=0.05):
            askIndex=5
        elif(askRatio >0.05 and askRatio <=0.1):
            askIndex=6
        elif(askRatio >0.1 and askRatio <=0.15):
            askIndex=7
        elif(askRatio >0.15 and askRatio <=0.2):
            askIndex=8    
        else:
            askIndex=9
        stateIndex = [inventoryIndex, bidIndex, askIndex]    

        # print("-state:")
        # print("inventory: " + str(inventory) +", bid: " + str(bidRatio) + ", askRatio: " + str(askRatio) )
        # print("-state index:")
        # print(stateIndex)
        return stateIndex
    def pickAction(self,stateIndex):
        '''
    returns index of best action according to Q tensor or a random action based 
    on epsilon.

                        action        actionIndex

                    "increaseBid" ->       0
                    "decreaseBid" ->       1
                    "increaseAsk" ->       2
                    "decreaseAsk" ->       3
                    "do nothing"  ->       4
        '''
        actionIndex = 4 #default to doing nothing

        #pick optimal action based on index and q values
        qOptions = self.qTable[stateIndex[0]][stateIndex[1]][stateIndex[2]]
        
        #print("-Action options for current state")
        #print(qOptions)
        
        actionIndex = qOptions.argmax()
        #explore or exploit
        if(self.qLearningConfig["epsilon"] < random.random()):
            print("-Exploring random action.")
            actionIndex = random.randrange(4)
        actionValue = qOptions[actionIndex]
        self.actions.append([actionIndex,actionValue])
        return actionIndex, actionValue


    def quote(self, price, competitorSpread):
        delta = 0.1 #initial delta for first bid ask
        if(not self.spread):
            self.spread.append([(price-price*delta), (price+price*delta)])
        #bid/ask = last times bid ask
        oldBid = self.spread[-1][0]
        oldAsk = self.spread[-1][1] 
        
        bidRatio = (competitorSpread["bid"]-oldBid)/price
        askRatio = (competitorSpread["ask"]-oldAsk)/price
        inventory = self.inventory[-1]

        stateIndex = self.selectStateIndex(inventory,bidRatio,askRatio)
        #update with current (pretrade) state
        self.states.append(stateIndex)
        actionIndex, actionValue = self.pickAction(stateIndex)
        print("State: " + str(stateIndex) )
        print("Action chosen: " + str(actionIndex) + " : " + str(actionValue))
            
        #move bid/ask based on state and Q
        nudgeConstant = self.qLearningConfig["nudge"]
        if(actionIndex ==0):
            oldBid = oldBid + nudgeConstant
        elif(actionIndex==1):
            oldBid = oldBid - nudgeConstant
        elif(actionIndex==2):
            oldAsk = oldAsk + nudgeConstant
        elif(actionIndex==3):
            oldAsk = oldAsk - nudgeConstant
        #if action is 4 ("do nothing") then spread is unchanged
        self.spread.append([oldBid,oldAsk])
        #update new state in settle()

        return self.spread[-1][0], self.spread[-1][1]

    def settle(self,sellOrder, bid, buyWinner, buyOrder, ask, sellWinner):
        if self._id == buyWinner and self._id == sellWinner:
            self.inventory.append(self.inventory[-1] + buyOrder - sellOrder)
            self.profit.append(self.profit[-1] - buyOrder*buyWinner + sellOrder*sellWinner)
            self.trades.append(buyOrder - sellOrder)#record trade
        elif self._id == buyWinner:
            self.inventory.append(self.inventory[-1] + buyOrder)
            self.profit.append(self.profit[-1] - buyOrder*buyWinner)
            self.trades.append(buyOrder)#record trade
        elif self._id == sellWinner:
            self.inventory.append(self.inventory[-1] - sellOrder)
            self.profit.append(self.profit[-1] + sellOrder*sellWinner)
            self.trades.append(-1*sellOrder ) #record trade (negative means a sell)
        if(self._id != sellWinner and self._id != buyWinner):
            self.profit.append(self.profit[-1])
            self.trades.append(0) #record trade

        #Find new (post trade) state
        stateIndex = self.selectStateIndex(self.inventory[-1],self.spread[-1][0],self.spread[-1][1])
        actionIndex, actionValue = self.pickAction(stateIndex)

        gamma = self.qLearningConfig["gamma"] #discount factor
        alpha = self.qLearningConfig["alpha"] #learning rate
        
        reward = self.profit[-1]-self.profit[-2]#reward from last step
        #should this be normalized?

        #calc temporal difference   
        TD = reward + gamma*actionValue + self.actions[-1][1] #reward + discount factor times greatest new q value + q value chosen
        
        #normalize TD to [0,1] assume min,max of [-200,200]
        #todo make this more sound
        TD = (TD+200)/400
        
        Qnew = self.actions[-1][1] + alpha*TD

        updateIndex = self.states[-1]
        updateIndex.append(self.actions[-1][0])
        #print(updateIndex)
        self.updateQTensor(updateIndex,Qnew)

  
    def updateQTensor(self,index,newValue):
        self.qTable[index[0]][index[1]][index[2]][index[3]] = newValue
        #print("new q value")
        #print(self.qTable[index[0]][index[1]][index[2]][index[3]])
      