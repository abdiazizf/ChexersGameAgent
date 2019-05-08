'''
Created on Apr 28, 2019

@author: Jordan
'''
from A_n_J.PossibleActions import PossibleActions
import copy

class BoardState(object):
    '''
    Representation of the current board state in a game of Chexers
    
    player_colour: the colour of the pieces owned by the player
    piece_vectors: a vector of all piece positions on a board
    actions: Instance of PossibleActions class containing the valid moves for 
             a given board state.
    evaluater: An instance of the Evaluater class used to evaluate the utility
               of a board state for the current player
    
    '''
    
    def __init__(self, player_colour,piece_vector,score):

        self.player_colour = player_colour
        self.piece_vectors = piece_vector
        self.legal_moves = PossibleActions()
        self.legal_moves.generate_actions(player_colour,self)
        self.score = score
    '''
    Takes an action and player colour as input, returns a new piece vector that
    represents the move taken by that player
    '''
    def update_piece_positions(self,colour,action):
        new_vector = copy.deepcopy(self.piece_vectors)
        if(action.action_type == "EXIT"):
            self.score[colour] +=1
            origin = action.origin
            new_vector[colour].remove(origin)
        else:
            origin = action.origin
            new_position = action.destination
            new_vector[colour][origin] = new_position
        return new_vector
        
    def generate_successor(self,action):
        
        new_piece_vector = self.update_piece_positions(self.player_colour, action)
        new_state = BoardState(self.player_colour,new_piece_vector,self.score)
        
        return new_state
    
    def is_terminal_state(self):
        for player in self.score:
            if self.score[player] == 4:
                return True
        
    '''
    Defines comparison of two board states
    '''
    def __eq__(self, other):
        return all(self.piece_vectors == other.piece_vectors)
    def __hash__(self):
        return
    def __str__(self):
        return
    