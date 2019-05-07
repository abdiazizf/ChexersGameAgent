'''
Created on Apr 28, 2019

@author: Jordan
'''
import A_n_J.PossibleActions
import A_n_J.Evaluater
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
    
    def __init__(self, player_colour,piece_vector):

        self.player_colour = player_colour
        self.piece_vectors = piece_vector
        self.actions = A_n_J.PossibleActions(self)
        self.actions.generate_actions(player_colour,self)
        self.evaluater = A_n_J.Evaluater()
    
    '''
    Takes an action and player colour as input, returns a new piece vector that
    represents the move taken by that player
    '''
    def update_piece_positions(self,colour,action):
        
        new_vector = copy.deepcopy(self.piece_vectors)
        
        origin = action.origin
        new_position = action.destination
        new_vector[colour][origin] = new_position
        return new_vector
        
    def generate_successor(self,action):
        
        new_piece_vector = self.update_piece_positions(self.player_colour, action)
        new_state = A_n_J.BoardState(self.player_colour,new_piece_vector)
        
        return new_state
        
    '''
    Defines comparison of two board states
    '''
    def __eq__(self, other):
        
        return
    def __hash__(self):
        return
    def __str__(self):
        return
    