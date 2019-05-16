'''
Created on Apr 28, 2019

@author: Jordan
'''
from A_n_J.PossibleActions import PossibleActions
import numpy as np

class BoardState(object):
    '''
    Representation of the current board state in a game of Chexers
    
    player_colour: the colour of the pieces owned by the player
    piece_vectors: a vector of all piece positions on a board
    actions: Instance of PossibleActions class containing the valid moves for 
             a given board state.
    
    '''
    
    def __init__(self, player_colour,piece_vector,score,board):
        self.player_colour = player_colour
        new_vector = piece_vector[:]
        self.piece_vectors = new_vector
        self.board = np.array(board)

        self.legal_moves = PossibleActions(self)
        self.legal_moves.generate_actions(player_colour,self.piece_vectors,self.board)
        
        self.score = score
        self.players_max_move = 0
        
        
    '''
    Takes an action and player colour as input, returns a new piece vector that
    represents the move taken by that player
    '''
    def update_piece_positions(self,colour,action,board):

        new_vector = [x[:] for x in self.piece_vectors]
        

        if(action.type == "PASS"):
            return new_vector
        if(action.type == "EXIT"):
            new_vector[colour].remove(action.origin)
            board[action.origin] = 0
        elif(action.type == "JUMP"):
            neighbour = action.get_neighbour_space()
            other_player = self.board[neighbour]

            if other_player != 0:
                if other_player != colour:
                    new_vector[other_player].remove(neighbour)
                    new_vector[colour].append(neighbour)
                    board[neighbour] = colour
            new_vector[colour].remove(action.origin)
            new_vector[colour].append(action.destination)
            board[action.origin] = 0
            board[action.destination] = colour
            
        else:
            new_vector[colour].remove(action.origin)
            new_vector[colour].append(action.destination)
            board[action.origin] = 0
            board[action.destination] = colour
        return new_vector
        
        
    def update_board_state(self,action,colour,score,board):
        
        new_piece_vector = self.update_piece_positions(colour, action,board)
        next_player = self.player_turn_order()
        new_score = self.copy_score()
        new_board = np.array(board)
        
        new_board[self.hex_to_array(action.origin)] = 0
        new_board[self.hex_to_array(action.destination)] = colour

        return BoardState(next_player,new_piece_vector,new_score,new_board)
        
    def player_turn_order(self):
        if (self.player_colour == 1):
            return 2
        elif( self.player_colour == 2):
            return 3
        else:
            return 1
    
    def generate_successor(self,action):

        new_piece_vector = self.update_piece_positions(self.player_colour, action,self.board)
        next_player = self.player_turn_order()
        new_score = self.copy_score()
        if(action.type == "EXIT"):
            new_score[self.player_colour] += 1
        new_score[0] += 1
        new_state = BoardState(next_player,new_piece_vector,new_score,self.board)

        
        return new_state
    
    def copy_score(self):

        return self.score[:]
    
    def is_terminal_state(self):
        if self.score[0] == 756:
            return True
        if self.score[1] == 4:
            return True
        if self.score[2] == 4:
            return True
        if self.score[3] == 4:
            return True 
        return False
            
    def get_winner(self):
        winner = None
        if self.score[1] == 4:
            winner = 1
        if self.score[1] == 4:
            winner = 2
        if self.score[1] == 4:
            winner = 3
        return winner
    
    def array_to_hex(self,hex):
        return (hex[0]-3,hex[1]-3)
    
    def hex_to_array(self,hex):
        return (hex[0]-3,hex[1]-3)
    
    
    '''
    Defines comparison of two board states
    '''
    def __eq__(self, other):
        return all(self.piece_vectors == other.piece_vectors)
    def __hash__(self):
        return
    def __str__(self):
        return
    