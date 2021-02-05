# Capstone

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

## Environment.py
Don't worry about this file. I was trying to implement Q-learning using a method
I found in a textbook but it doesn't seem to provide the level of detail we want.
Might come back to it at some point later in the project.

## QLAgent.py
This file contains our learning agent. This is my attempt at designing a Q-table and
the state and action space are not as specified yet. We need to do a little more research
to see if there are any libraries that help with Q-tables. I feel like their is probably
a more efficient way to do this than using numpy matrices.

A lot of the functions are similar to the agent.py file. 

## main.py
This is where the simulation is executed. Running this file executes *simulation()*.
At the top of this function are the important values to manipulate:
* step
* time
* Drift
* volatility
* initValue
* agent_num

We call the previous functions to get our prices and demand and then call *makeAgents*
to initialize the competitors. I have commented out three lines after that which
are involved with the Q-learning agent because I am currently focused on the environment.
The competition happens in *profitCalculation()*. 

In this function, we iterate over all the time steps and find who has the most competitive bid and ask
prices. It then uses settle to reward the agents who outbid their opponents. Once this is finished, we
plot the profit of each agent. This profit does not include their assets (i.e. inventory). We can add this
next.

## Issues
* get Q-Learning agent working and look for possible 3rd party libraries to help


## Tasks (not started)
* create GUI
* Generalize our agent so that it can use any RL algorithm (Q-learning, etc.)
* make trader demand function more realistic 

## Tasks (started)
* Track inventory

## tasks (done)
* plot ref price
* track trades
* Visualize trades over time, plot 
* Create more detailed simulation diagram
