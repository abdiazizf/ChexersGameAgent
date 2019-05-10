'''
Created on May 8, 2019

@author: Jordan
'''

import numpy as np
from _collections import defaultdict
from A_n_J.Action import Action
import random
from numpy.random.mtrand import choice

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
        return len(self.untried_actions) == 0
    
    def best_child(self, c_param = 1.4):
        choices_weights = [
            (c.wins / (c.visits)) + c_param * np.sqrt((2 * np.log(self.visits) / (c.visits)))
            for c in self.children
        ]
        if(choices_weights):
            return self.children[np.argmax(choices_weights)]
        else:
            return self
    
    def expand(self):
        action = random.choice(self.untried_actions)
        next_state = self.state.generate_successor(action)
        child_state = MCNode(next_state, parent=self)
        child_state.generated_by = self.generated_by(action)
        self.children.append(child_state)
        return child_state
    
    def is_terminal_state(self):
        return self.state.is_terminal_state()
    
    def rollout_policy(self, possible_moves):
        #Random policy
        if(possible_moves):
            for move in possible_moves:
                if(move.action_type == "EXIT"):
                    return move
            move_to_use = random.choice(possible_moves)

        else:
            move_to_use = Action((0,0),(0,0),"PASS")
        return move_to_use 
    
    def rollout(self):
        current_state = self.state
        while not current_state.is_terminal_state():
            possible_moves = current_state.legal_moves.get_actions()
            action = self.rollout_policy(possible_moves)
            current_state = current_state.generate_successor(action)
        return current_state.player_colour
                                                  
    def backpropogate(self, result):
        self.number_of_visits += 1 
        self.results[result] +=1
        if self.parent:
            self.parent.backpropogate(result)
    
    def generated_by(self,action):
        if(action == None):
            action = Action((0,0),(0,0),"PASS")
        if not '_generated_by' in self.__dict__:
            self._generated_by = action
        return self._generated_by
    
    @property
    def untried_actions(self):
        if not '_untried_actions' in self.__dict__:
            self._untried_actions = self.state.legal_moves.get_actions()
        return self._untried_actions
    
    @property
    def wins(self):
        wins = self.results[self.parent.state.player_colour]
        loses = self.results[-1 * self.parent.state.player_colour]
        
        return wins-loses
    
    @property
    def visits(self):
        return self.number_of_visits