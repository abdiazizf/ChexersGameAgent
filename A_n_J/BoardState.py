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
        
        
    '''
    Takes an action and player colour as input, returns a new piece vector that
    represents the move taken by that player 
    '''
    def update_piece_positions(self,colour,action,board):
        new_vector = [row[:] for row in self.piece_vectors]

        if(action.type == "PASS"):
            return new_vector
        elif(action.type == "EXIT"):
            new_vector[colour].remove(action.origin)
            board[action.origin] = 0
            return new_vector
        elif(action.type == "JUMP"):
            #Check if another player was captured
            neighbour = action.get_neighbour_space()
            other_player = self.board[neighbour]
    
            if board[neighbour] != 0 and board[neighbour] != colour:
                new_vector[other_player].remove(neighbour)
                new_vector[colour].append(neighbour)
                board[neighbour] = colour
        
        new_vector[colour].remove(action.origin)
        new_vector[colour].append(action.destination)
        
        board[action.origin] = 0
        board[action.destination] = colour
        
        return new_vector
        
    def update_game_state(self,action,colour,score,board):
        
        # Needs to 
        # Reconfigure piece positions 
        #Change board entries
        # add to score
        # change turn order
        # return the new state 
        
        new_piece_vector = self.update_piece_positions(colour, action, self.board)
        next_player = self.player_turn_order()
        new_score = score[:]
        new_board = np.array(board)

        return BoardState(next_player,new_piece_vector,new_score,new_board)
        
    
    def generate_successor(self,action):

        new_board = np.array(self.board)
        new_piece_vector = self.update_piece_positions(self.player_colour, action,new_board)
        next_player = self.player_turn_order()
        new_score = self.score[:]

        if(action.type == "EXIT"):
            new_score[self.player_colour] += 1
        new_score[0] += 1
        
        new_state = BoardState(next_player,new_piece_vector,new_score,new_board)

        
        return new_state
    
    def do_update(self,colour,action,board):
        new_vector = self.piece_vectors
        if(action.type == "PASS"):
            return new_vector
        elif(action.type == "EXIT"):
            board[action.origin] = 0
            new_vector[colour].remove(action.origin)
            return new_vector
        elif(action.type == "JUMP"):
            #Check if another player was captured
            neighbour = action.get_neighbour_space()
            other_player = self.board[neighbour]
            if board[neighbour] != 0 and board[neighbour] != colour:
                new_vector[other_player].remove(neighbour)
                new_vector[colour].append(neighbour)
                board[neighbour] = colour
        
        new_vector[colour].remove(action.origin)
        new_vector[colour].append(action.destination)
        
        board[action.origin] = 0
        board[action.destination] = colour
    
    
    def do_move(self,action):
        self.do_update(self.player_colour, action, self.board)
        if(action.type == "EXIT"):
            self.score[self.player_colour] += 1
        self.score[0] += 1
        self.player_colour = self.player_turn_order()
        self.legal_moves.actions = []
        self.legal_moves.generate_actions(self.player_colour, self.piece_vectors, self.board)
    
    
    
    def player_turn_order(self):
        if (self.player_colour == 1):
            return 2
        elif( self.player_colour == 2):
            return 3
        else:
            return 1
    
    def validate_board(self):
        p = 0
        for player in self.piece_vectors:
            for piece in player:
                if self.board[piece] == 0:
                    return False
                if self.board[piece] != p:
                    print("INVALID BOARD",piece,p)
                    return False
            p += 1 
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
    

    '''
    Defines comparison of two board states
    '''
    def __eq__(self, other):
        return all(self.piece_vectors == other.piece_vectors)
    def __hash__(self):
        return
    def __str__(self):
        return
    