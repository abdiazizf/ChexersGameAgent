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
        
        for sim in range(0, num_simulations):
            v = self.tree_policy()
            simulation_result = v.rollout()
            v.backpropogate(simulation_result)
        
        best_choice_node = self.initial_state.best_child(c_param = 1.)
        return best_choice_node.generated_by
        
    
    def tree_policy(self):
        current_state = self.initial_state
        while current_state.is_terminal_state() == False:
            if current_state.fully_expanded() == False:
                return current_state.expand()
            else:
                current_state = current_state.best_child()
        return current_state