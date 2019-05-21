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
        state: BoardState object representing current game state
        parent: Parent MCnode in the tree. 
        children: List of child MCNodes
        number_of_visits: number of times the node has been visited 
        results: a dict holding the results recorded by passing through this node
                 represented a the number of wins for each colour and the number 
                 of draws
        generated_by = action used to generate this node 
         
        '''
        self.state = board_state
        self.parent = parent
        self.children = []
        self.number_of_visits = 0
        self.results = defaultdict(int)
        self.generated_by = None
        
    '''
    Returns true if there are no more untried actions in the current node. 
    ie. all possible children have been created at this node in the tree. 
    '''
    def fully_expanded(self):
        if len(self.untried_actions) == 0:
            return True
        else:
            return False 
    
    '''
    Determines the 'best' child node based on the UCT formula. The c_param
    input is used to tune the level of exploration vs exploitation used 
    when selecting the best child. 
    '''
    def best_child(self, c_param = 1):
        choice_weights = []
        
        # Calculate the score for each child using UCT
        for child in self.children:
            weight = ((child.wins/(child.visits)) + c_param * math.sqrt((2 * math.log(self.visits) / (child.visits))))
            choice_weights.append(weight)
            
        # Determine the best choice by the maximum value 
        max_val = max(choice_weights)
        index_max = choice_weights.index(max_val)
        if(choice_weights):
            return self.children[index_max]
        else:
            return self
    
    '''
    Expands a the current node by choosing an untried action, creating a new 
    state for that action and then using that state to create a new MCNode.
    '''
    def expand(self):
        # Choose an unexpanded action at random and remove it from 
        # the list of untried actions
        action_index = random.randint(0,len(self.untried_actions)-1)
        action = self.untried_actions.pop(action_index)  
        
        # Create a new MCnode based on the chosen action and 
        # add it to the tree. 
        next_state = self.state.generate_successor(action)
        child_state = MCNode(next_state, parent=self)
        child_state.generated_by = self.get_generated_by(action)
        self.children.append(child_state)
        return child_state
    
    '''
    Check whether the current node is a terminal state in the game 
    of Chexers 
    '''
    def is_terminal_state(self):
        return self.state.is_terminal_state()
    
    '''
    The rollout policy for playing out a game from a node. Selects an action 
    at random from the available list of legal actions. 
    '''
    def rollout_policy(self, possible_moves):
        return random.choice(possible_moves)
    
    '''
    From a node in the tree choose moves according to the rollout policy until
    either a terminal state is reached or the rollout reaches the maximum depth
    allowed to it. 
    
    Once either condition has been satisfied will return the predicted, or 
    actual winner at this state.  
    '''
    def rollout(self):
        current_state = deepcopy(self.state)
        depth = 0
        endgame = False
        # imposed depth limit 
        while depth < 30 and current_state.is_terminal_state() == False:
            # Choose a move and modify the current state
            possible_moves = current_state.legal_moves.get_actions()
            action = self.rollout_policy(possible_moves)
            current_state.do_move(action)
            depth += 1
            if(endgame == True):
                depth = 768
        winner = current_state.get_winner()
        return winner
    
    '''
    Move back up through the tree updating the results dict with the result of 
    a rollout
    '''                                              
    def backpropogate(self, result):
        self.number_of_visits += 1 
        self.results[result] +=1
        if self.parent:
            self.parent.backpropogate(result)
    
    '''
    Return the action which generated the current node. 
    '''
    def get_generated_by(self,action):
        if(action == None):
            genby = Action((0,0),(0,0),"PASS")
        else:
            genby = action
        
        return genby
    
    '''
    Check if the current node has children 
    '''
    def has_children(self):
        if self.children != []:
            return True
    '''
    If a node does not already have a list of untried actions when called,
    will create that list. Otherwise will return untried action list. 
    '''
    @property
    def untried_actions(self):
        if not '_untried_actions' in self.__dict__:
            self._untried_actions = self.state.legal_moves.get_actions()
        return self._untried_actions
    
    '''
    Determines the wins for the current player whose turn it is based on 
    the number of times they have won versus the times their opponent has won. 
    '''
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
    
    '''
    Returns the number of times a node has been visited. 
    '''
    @property
    def visits(self):
        return self.number_of_visits