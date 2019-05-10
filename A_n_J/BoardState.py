'''
Created on Apr 28, 2019

@author: Jordan
'''
from A_n_J.PossibleActions import PossibleActions
import copy
from copy import deepcopy

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
        self.legal_moves = PossibleActions(self)
        self.legal_moves.generate_actions(player_colour,self)
        self.score = score
        self.players_max_move = 0
        
    '''
    Takes an action and player colour as input, returns a new piece vector that
    represents the move taken by that player
    '''
    def update_piece_positions(self,colour,action):
        
        new_vector = copy.deepcopy(self.piece_vectors)
        if(action.action_type == "EXIT"):
            print("EXIT MOVE TAKEN")
            self.score[colour]["exits"] +=1
            origin = action.origin
            new_vector[colour].remove(origin)
        else:
            new_vector[colour].remove(action.origin)
            new_position = action.destination
            new_vector[colour].append(new_position) 
        self.score[self.player_colour]["turns"] += 1
        return new_vector
        
    def player_turn_order(self):
        if (self.player_colour == "red"):
            return 'green'
        elif( self.player_colour == 'green'):
            return 'blue'
        else:
            return 'red'
        
    def generate_successor(self,action):
        
        #self.generated_by = action
        new_piece_vector = self.update_piece_positions(self.player_colour, action)
        next_player = self.player_turn_order()
        new_state = BoardState(next_player,new_piece_vector,self.score)
        
        return new_state
    
    def update_board_state(self,action,colour,score):
        new_piece_vector = self.update_piece_positions(colour, action)
        next_player = self.player_turn_order()
        new_score = deepcopy(score)

        return BoardState(next_player,new_piece_vector,new_score)
    
    def is_terminal_state(self):
        max_moves = 0
        for player in self.score:
            if self.score[player]["exits"] == 4:
                return True
            elif self.score[player]["turns"] >= 256:
                max_moves +=1
        if max_moves == 3:
            return True
        else:
            return False
            
    def get_winner(self):\
        pass
    '''
    Defines comparison of two board states
    '''
    def __eq__(self, other):
        return all(self.piece_vectors == other.piece_vectors)
    def __hash__(self):
        return
    def __str__(self):
        return
    