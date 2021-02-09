# Capstone

## Running simulation
Ensure that you have git and Python3 installed. Clone the git repo, enter the directory and switch to 'joshDev' branch.
    
    git clone https://github.com/spencerkelly143/capstone.git
    cd captone 
    git checkout joshDev
    git pull

To run the simulation, run the simulation.py file.

    python simulation.py

If executed correctly, the program should create the simulation environment and produce graphs with the ref price and agent profits over time. The simulation can be configured in the simulation.py file.

## demand.py
Generates the market buy and sell orders. These are randomly generated and are normalized to be around
100. Returns an array of size *Size*.

## agent.py
This is the file that defines the competitor 1. We initialize the competitor with emax. That's the
max spread value percentage. We call *quote()* when we want to get bi/ask prices from the agent.
Currently I am using five agents.

As far as future construction, I'm thinking that once we go to define other
competitors, we will take the *spread()* function out of this file and make separate competitor_1,
competitor_2, and competitor_3 files. We will then just inherit the other properties from *agent.py*
in those and then define the spread function in the respective files.

## brownian.py
This file returns a list of reference prices. Considers the initial value, volatility,
and drift. You can also specify the time and step values. The total number of iterations
is calculated time divided by step. For example, if you wanted prices every hour for 5 days,
you could do *time = 5 x 24* and *step = 1*.

## environment.py
Currently set up as main market environment for the simulation. Made a few changes from the master branchand will continue to work with this file for Q-learning


## simulation.py
This is the new main file where the simulation is executed. Running this file executes initializes the environment.py, generates GBM ref prices based on confguration, creates agents, and runs the market simulation. At this time, it is almost identical in functionality to the old main.py file.


## agentQ.py
todo: write documentation for q learner


## Q-Matrix format
The q matrix is shaped as a 4 dimentional tensor (4,10,10,5). The first 3 indices are the state of the QLearner/market. They are binned based on the ranges shown below to increase computational efficiency. The 4th index represents the action space. 

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

## Issues
* get Q-Learning agent working in simple terms
* simulation assumes all market makers can buy/sell as much as the market demands
* test settle() method for agents and Qagent. I think it might be allowing multiplt buy/sell winners at the same time. I also think it was preventing the same agent from being a buyer and seller before
* A mix of python dicts and small arrays are used throughout the project to pass multiple values, this should be standardized to just one or the other
* might need to do more actions at once
* type 1 agents have keep losing profit for some reason

## Tasks (not started)
* create GUI
* Generalize our agent so that it can use any RL algorithm (Q-learning, etc.)
* make trader demand function more realistic 

## Tasks (started)
* get Qlearning agent working more consistently
    * setup simulation to have many training episodes
    * setup testing for all methods
    * formalize all math and make sure its good
## tasks (done)
* plot ref price
* track trades
* Visualize trades over time, plot 
* Create more detailed simulation diagram
* update Q table with bellman
