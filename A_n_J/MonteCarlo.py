'''
Created on May 7, 2019

@author: Jordan
'''

class MonteCarlo(object):
    
    def __init__(self, root, **kwargs):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.initial_state = root
    
    def best_action(self, num_simulations):

        for _ in range(0, num_simulations):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropogate(reward)

        
        return self.initial_state.best_child(c_param = 0.).generated_by
    
    def tree_policy(self):
        current_state = self.initial_state
        while current_state.is_terminal_state() == False:
            if current_state.fully_expanded() == False:
                return current_state.expand()
            else: 
                return current_state.best_child()
                
        return current_state