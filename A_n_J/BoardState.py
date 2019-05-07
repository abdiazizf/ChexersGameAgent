'''
Created on Apr 28, 2019

@author: Jordan
'''
import A_n_J.PossibleActions
import A_n_J.Evaluater

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
    
    def __init__(self, player_colour):

        self.player_colour = player_colour
        self.piece_vectors = self.construct_piece_vectors(self)
        self.actions = A_n_J.PossibleActions(self)
        self.actions.generate_actions(player_colour,self)
        self.evaluater = A_n_J.Evaluater()
    
    
    '''
    Returns a dictionary of vectors containing the initial positions of the 
    pieces for each player on the board. Used during setup of a board_state
    '''
    def construct_piece_vectors(self):
        
        piece_vectors = {}
        piece_vectors["red"] = [(-3,0),(-3,1),(-3,2),(-3,3)]
        piece_vectors["green"] = [(0,-3),(1,-3),(2,-3),(3,-3)]
        piece_vectors["blue"] =  [(3,0),(2,1),(1,2),(0,3)]
        
        return piece_vectors
    
    '''
    Takes an action and player colour as input, updates the piece vector in 
    the board state to represent a move taken by that player
    '''
    def update_piece_positions(self,colour,action):
        origin = action.origin
        new_position = action.destination
        self.piece_vectors[colour][origin] = new_position
        
    '''
    Defines comparison of two board states
    '''
    def __eq__(self, other):
        
        return
    def __hash__(self):
        return
    def __str__(self):
        return
    