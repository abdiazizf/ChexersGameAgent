'''
Created on May 8, 2019

@author: Jordan
'''


from _collections import defaultdict
from A_n_J.Action import Action
import random
import math 
from copy import deepcopy

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
        self.generated_by = None
        self.depth = 0
        self.sdepth = str(self.depth)
        
    def fully_expanded(self):
        cur_num_action = len(self.untried_actions)
        if cur_num_action == 0:
            return True
        else:
            return False 
    
    def best_child(self, c_param = 1):
        choice_weights = []
        for child in self.children:
            weight = ((child.wins/(child.visits)) + c_param * math.sqrt((2 * math.log(self.visits) / (child.visits))))
            choice_weights.append(weight)
        max_val = max(choice_weights)
        index_max = choice_weights.index(max_val)
        if(choice_weights):
            return self.children[index_max]
        else:
            return self
    
    def rand_child(self):
        return random.choice(self.children)
    
    def expand(self):
        # Choose an unexpanded action
        action_index = random.randint(0,len(self.untried_actions)-1)
        action = self.untried_actions.pop(action_index)  
        # Create a new state from action and form a new node for it
        next_state = self.state.generate_successor(action)
        child_state = MCNode(next_state, parent=self)
        child_state.generated_by = self.get_generated_by(action)
        self.children.append(child_state)
        return child_state
    
    def is_terminal_state(self):
        return self.state.is_terminal_state()
    
    def rollout_policy(self, possible_moves):
        #Random policy
        return random.choice(possible_moves)
    
    def rollout(self):
        current_state = deepcopy(self.state)
        depth = 0
        while depth < 60:
            possible_moves = current_state.legal_moves.get_actions()
            action = self.rollout_policy(possible_moves)
            current_state.do_move(action)
            depth += 1
        winner = current_state.get_winner()
        return winner
                                                  
    def backpropogate(self, result):
        self.number_of_visits += 1 
        self.results[result] +=1
        if self.parent:
            self.parent.backpropogate(result)
    
    def get_generated_by(self,action):
        if(action == None):
            genby = Action((0,0),(0,0),"PASS")
        else:
            genby = action
        
        return genby
    
    def has_children(self):
        if self.children != []:
            return True
    
    @property
    def untried_actions(self):
        if not '_untried_actions' in self.__dict__:
            self._untried_actions = self.state.legal_moves.get_actions()
        return self._untried_actions
    
    @property
    def wins(self):
        wins = 0
        loses = 0
        for outcome in self.results:
            if outcome == self.parent.state.player_colour:
                wins = self.results[outcome]
            else:
                loses = self.results[outcome]
        return wins-loses
    
    @property
    def visits(self):
        return self.number_of_visits