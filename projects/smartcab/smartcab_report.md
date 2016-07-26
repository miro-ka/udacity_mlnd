# Smartcab project report

```
author: miroslav.karpis@gmail.com
project: Udacity Reinforcement Learning project (Machine Learning Engineer Nanodegree)
```

## Simulation details
### Valid actions###
[None, 'forward', 'left', 'right']

### Rules
Agent is at a green light, it should be allowed to:
* Go forward
* Turn right
* Turn left, yielding to any oncoming traffic that is going straight or turning right

At a red light:
* Turn right, yielding to any traffic from the left that is going straight

### Rewards and Goal
* The smartcab receives a reward for each successfully completed trip.
* Smaller reward for each action it executes successfully that obeys traffic rules. 
* Smartcab receives a small penalty for any incorrect action.
* Larger penalty for any action that violates traffic rules or causes an accident with another vehicle.


## Task 1: Implement a Basic Driving Agent

**Question 1: Does the smartcab eventually make it to the destination?**
During my observations (approximately 10 cycles of new target placement), I have observed only 1 case, when the car reached the target.

**Question 2: Are there any other interesting observations to note?**
So far I didn't observe very much of interesting behavior.


## Task 2: Inform the Driving Agent

**Question 1: What states have you identified that are appropriate for modeling the smartcab and environment?**

 Initially we have following state inputs available from the environment:
 * **light**: ['red', 'green']
 
 * **oncoming**: Information whether a car is approaching from oncoming(forward) direction, and the direction where the vehicle is heading. [None, 'right', 'left', 'forward']
 
 * **right**: Information whether a car is approaching from right direction, and the direction where the vehicle is heading. [None, 'right', 'left', 'forward']
 
 * **left**: Information whether a car is approaching from left direction, and the direction where the vehicle is heading. [None, 'right', 'left', 'forward']
 
 * **deadline**: The current time left from the allotted deadline.
 
 * **t**: Total of my current time steps (in this game)
 
 * **reward**: Sum of my current reward
 
 * **waypoint**: The next waypoint location relative to its current location and heading.  ['right', 'left', 'forward']
 
 I think that following states are important and should be identified as appropriate for modeling the smartcab (reasons described in question 2):
  * light, oncoming, right, left

**Question 2: Why do you believe each of these states to be appropriate for this problem?**
 Most of the selected states because of the specified rules in overall [rules](#rules). 
 
 List of selected states and the reason of selecting it:
 
 * **light**: State indicating whether we can go to all directions (on green light, with extra check when we need to turn to left), or only to right (on red light).
 
 * **oncoming**: Important state in relation to traffic light. Logic described in [rules](#rules).
 
 * **right**: Important state in relation to traffic light. Logic described in [rules](#rules).
 
 * **left**: Important state in relation to traffic light. Logic described in [rules](#rules).
 
 
**OPTIONAL**
1. *How many states in total exist for the smartcab in this environment?* If we consider that our states have following parameters/combinations we have total **129 states**. 129 is calculated from following values (2 x lights) x (4 x oncoming) x (4 x right) x (4 x left)
2. Does this number seem reasonable given that the goal of Q-Learning is to learn and make informed decisions about each state? 
3. Why or why not?


## Task 3: Implement a Q-Learning Driving Agent

### QUESTION: What changes do you notice in the agent's behavior when compared to the basic driving agent when random actions were always taken? Why is this behavior occurring?


