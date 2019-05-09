'''
Created on May 8, 2019

@author: Jordan
'''

import numpy as np
from _collections import defaultdict
from tkinter.constants import CURRENT

class MCNode(object):
    '''
    Node in the monte carlo search tree for a game of chexers 
    '''


    def __init__(self, board_state, parent = None):
        '''
        Constructor
        '''
        self.state = board_state
        self.parent = parent
        self.children = []
        self.number_of_visits = 0
        self.results = defaultdict(int)
        
    def fully_expanded(self):
        print(len(self.untried_actions), "Actions left")
        return len(self.untried_actions) == 0
    
    def best_child(self, c_param = 1.4):
        choices_weights = [
            (c.q / (c.n)) + c_param * np.sqrt((2 * np.log(self.n) / (c.n)))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]
    
    
    def rollout_policy(self, possible_moves):
        #Random policy
        return possible_moves[np.random.randint(len(possible_moves))]
    
    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.generate_successor(action)
        child_state = MCNode(next_state, parent=self)
        self.children.append(child_state)
        print("RETURNED CHILD STATE")
        return child_state
    
    def is_terminal_state(self):
        return self.state.is_terminal_state()
    
    def rollout(self):
        print("ENTERING ROLLOUT")
        current_state = self.state
        while not current_state.is_terminal_state():
            
            possible_moves = current_state.legal_moves.get_actions()
            action = self.rollout_policy(possible_moves)
            current_state = current_state.generate_successor(action)
        print("TERMINAL STATE FOUND")
        return current_state.player_colour
                                                  
    def backpropogate(self, result):
        self.number_of_visits += 1 
        self.results[result] +=1
        if self.parent:
            self.parent.backpropogate(result)
    
    @property
    def untried_actions(self):
        if not '_untried_actions' in self.__dict__:
            self._untried_actions = self.state.legal_moves.get_actions()
        return self._untried_actions
    
    @property
    def q(self):
        wins = self.results[self.parent.state.player_colour]
        loses = self.results[-1 * self.parent.state.player_colour]
        
        return wins-loses
    
    @property
    def n(self):
        return self.number_of_visits