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
        self.state_roots = ['light', 'next_waypoint', 'right', 'left', 'oncoming'] 
        #self.state_roots = ['light', 'next_waypoint'] 
        self.Qtable = {}
        #tuning variables
        self.gamma = 0.1 # discount factor
        self.alpha = 0.5 # learning rate
        self.epsilon = 10 # exploration rate (select random action every x iteration)
        self.overall_simulations = 0
        self.overall_iterations = 0
        self.total_sucess = 0



    def reset(self, destination=None):
        self.overall_simulations += 1
        self.planner.route_to(destination)
        print "\n-----starting new simulation-----"
        self.print_Qtable()
        print "overall_iterations: ", self.overall_iterations
        print "overall_simulations: ", self.overall_simulations
        print "total_sucess: ", self.total_sucess
        print "self.gamma: ", self.gamma
        if self.total_sucess == 0:
            print "sucess_rate: 0%"
        else:
            sucess_rate = float(self.total_sucess)/float(self.overall_simulations)
            print "sucess_rate: ", sucess_rate*100, "%"
        
        

    def add_new_state_to_Qtable(self, new_state_):
        #print "ADDING NEW STATE: ", new_state_
        action_state_init = 2
        init_actions = [(None, action_state_init), 
                        ('forward', action_state_init), 
                        ('left', action_state_init), 
                        ('right', action_state_init)]
        state_tuple = {new_state_: init_actions}
        self.Qtable.update(state_tuple)
        return init_actions



    def print_Qtable(self):
        print "self.Qtable:"
        for row in self.Qtable:
            print "\t", row, self.Qtable[row]    



    def get_action_from_Qtable(self, state_):
        state_tuple = self.Qtable.get(str(state_))
        new_action_tuple = None
        
        if state_tuple is None:
            # if the state is not in Q-table create it and choose random action
            state_actions = self.add_new_state_to_Qtable(state_)
            new_action_tuple = random.choice(state_actions)
            #print "new_random_action: ", new_action_tuple
        else:
            # state is in Q_table so get the maximum
            #print "found_existing_Qtable_state: ", state_tuple
            
            # if all items have the same Q_value, just return a random one
            Q_values = map(lambda state: state[1], state_tuple)
            #print "Q_values:", Q_values
            are_the_same = all(x == Q_values[0] for x in Q_values)
            #print "are_the_same:", are_the_same
            if are_the_same:
                return state_tuple[random.choice([0,1,2,3])]

            #check epsilon greedy
            if((self.env.t != 0) and ((self.env.t % self.epsilon) == 0)):
                return state_tuple[random.choice([0,1,2,3])]
                
            max_value = -sys.maxint - 1
            #print "state_tuple:", state_tuple

            for index in range(len(state_tuple)):
                if state_tuple[index][1] > max_value:
                    max_state_index = index
                    max_value = state_tuple[index][1]

            new_action_tuple = state_tuple[max_state_index]
        return new_action_tuple
        

    def update(self, t):
        self.overall_iterations += 1
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        inputs.update({'next_waypoint': self.next_waypoint})
        inputs.update({'deadline': deadline})
        
        # Update state
        #print "\n\ninputs:", inputs
        # get only the monitoring states and save them to self.state     
        map(lambda state: self.state.update({state: inputs[str(state)]}), self.state_roots)
        
        #self.print_Qtable()        
        
        # 1) ----- get new state from Q-table (according to your policy)
        state_string = str(self.state)
        #print "state_string:", state_string
        new_action_tuple = self.get_action_from_Qtable(state_string)
         
        # 2) ----- Execute action and get reward
        action = new_action_tuple[0]
        #action = random.choice(self.actions)
        #action = self.next_waypoint
        #print "new_action_tuple:", new_action_tuple               
        reward = self.env.act(self, action)
        #print "action REWARD: ", reward
        
        # 3) ----- Learn policy based on state, action, reward
        new_state = {}
        new_inputs = self.env.sense(self)
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator        
        new_inputs.update({'next_waypoint': self.next_waypoint})
        new_inputs.update({'deadline': self.env.get_deadline(self)})
        
        map(lambda state: new_state.update({state: new_inputs[str(state)]}), self.state_roots)
        #print "new_state:", new_state
        max_action_tuple = self.get_action_from_Qtable(str(new_state))

        Q_hat = (1-self.alpha) * new_action_tuple[1] + self.alpha * (reward + self.gamma * max_action_tuple[1])
        
        #print "Q_hat:", Q_hat
        state_tuples = self.Qtable[state_string]
        # store new/updated value to Qtable
        updated_state_tuples = state_tuples
        i = 0
        for s in state_tuples:
            if s[0] == action: state_tuples[i] = (action, Q_hat)
            i += 1
                
        #print "updated_state_tuples:", updated_state_tuples
        self.Qtable[state_string] = updated_state_tuples
        
        if self.env.trial_data['success'] == 1:
            self.total_sucess += 1
            #for every 10 correct predictions we decay the exploration rate
            if(self.total_sucess > 1 and ((self.total_sucess % 10) == 0) and (self.gamma < 1)):
                self.gamma += 0.1 

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
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
