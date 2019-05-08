'''
Created on May 7, 2019

@author: Jordan
'''
from A_n_J.BoardState import BoardState
from A_n_J.MCNode import MCNode

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
        
        return self.initial_state.best_child()
    
    def tree_policy(self):
        current_state = self.initial_state
        while not current_state.is_terminal_state():
            if not current_state.fully_expanded():
                return current_state.expand()
            else: 
                current_state = current_state.best_child()
                
        return current_state