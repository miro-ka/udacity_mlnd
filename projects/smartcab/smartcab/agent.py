import random
import itertools
import sys
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

        
    def __init__(self, env_):
        super(LearningAgent, self).__init__(env_)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.state = {}
        self.actions = [None, 'forward', 'left', 'right']
        self.state_roots = ['light', 'next_waypoint'] #'right', 'left'
        self.Qtable = {}
        #tuning variables
        self.gamma = 0.1 #todo update self.gamma
        self.alpha = 0.1


    def add_new_state_to_Qtable(self, new_state_):
        print "ADDING NEW STATE: ", new_state_
        init_actions = [(None, 0), ('forward', 0), ('left', 0), ('right', 0)]
        state_tuple = {new_state_: init_actions}
        self.Qtable.update(state_tuple)
        return init_actions


    def print_Qtable(self):
        print "-----------------------"
        print "self.Qtable:"
        for row in self.Qtable:
            print "\t", row, self.Qtable[row]
        print "-----------------------"        


    def get_action_from_Qtable(self, state_):
        state_tuple = self.Qtable.get(str(state_))
        new_action_tuple = None
        
        if state_tuple is None:
            # if the state is not in Q-table create it and choose random action
            state_actions = self.add_new_state_to_Qtable(state_)
            new_action_tuple = random.choice(state_actions)
            print "new_random_action: ", new_action_tuple
        else:
            #state is in Q_table so get the maximum
            print "found_existing_Q-table_state: ", state_tuple
            i = random.choice([0,1,2,3]);
            max_value = -sys.maxint - 1
            for state in state_tuple:
                if state[1] > max_value:
                    max_state = i
                    max_value = state[1]
            
            new_action_tuple = state_tuple[i]
            print "max_state: ", state_tuple[i]
        return new_action_tuple    



    def reset(self, destination=None):
        self.planner.route_to(destination)
        print "\n-----resetting-----"
        # TODO: Prepare for a new trip; reset any variables here, if required



    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        inputs.update({'next_waypoint': self.next_waypoint})

        
        # Update state
        print "\n\ninputs:", inputs
        # get only the monitoring states and save them to self.state     
        map(lambda state: self.state.update({state: inputs[str(state)]}), self.state_roots)
        
        
        self.print_Qtable()
                
        
        # 1) ----- get new state from Q-table (according to your policy)
        state_string = str(self.state)
        print "state_string:", state_string
        new_action_tuple = self.get_action_from_Qtable(state_string)
         

        # 2) ----- Execute action and get reward
        action = new_action_tuple[0]
        #action = random.choice(self.actions)
        #action = self.next_waypoint
        print "new_action_tuple:", new_action_tuple               
        reward = self.env.act(self, action)
        print "action REWARD: ", reward
        
                        
        # 3) ----- Learn policy based on state, action, reward
        new_state = {}
        new_inputs = self.env.sense(self)
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator        
        new_inputs.update({'next_waypoint': self.next_waypoint})

        
        map(lambda state: new_state.update({state: new_inputs[str(state)]}), self.state_roots)
        print "new_state:", new_state
        max_action_tuple = self.get_action_from_Qtable(str(new_state))

        
        Q_hat = (1-self.alpha) * new_action_tuple[1] + self.alpha * (reward + self.gamma * max_action_tuple[1])
        
        print "Q_hat:", Q_hat
        state_tuples = self.Qtable[state_string]
        
        updated_state_tuples = state_tuples
        i = 0
        for s in state_tuples:
            if s[0] == action: state_tuples[i] = (action, Q_hat)
            i += 1
                
        print "updated_state_tuples:", updated_state_tuples
        print "state_string:", state_string
        self.Qtable[state_string] = updated_state_tuples
        
        #print "self.next_waypoint:", self.next_waypoint
        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]




def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=1, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
