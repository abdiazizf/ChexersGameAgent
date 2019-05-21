'''
Created on Apr 28, 2019

@author: Jordan
'''
from A_n_J.PossibleActions import PossibleActions
import numpy as np
from itertools import chain


class BoardState(object):
    '''
    Representation of the current board state in a game of Chexers
    
    player_colour: the colour of the pieces owned by the player
    piece_vectors: a vector of all piece positions on a board
    board: an array representing the position of all pieces on the board
    legal_moves: Instance of PossibleActions class containing the valid moves for 
             a given board state.
    score: A list representing the number of turns taken to reach the state, 
           as well as the number of pieces that have exited the board for each player
    '''
    
    def __init__(self, player_colour,piece_vector,score,board):
        self.player_colour = player_colour
        new_vector = piece_vector[:]
        self.piece_vectors = new_vector
        self.board = np.array(board)
        self.legal_moves = PossibleActions(self)
        self.legal_moves.generate_actions(player_colour,self.piece_vectors,self.board)
        self.score = np.array(score)
        
        
    '''
    Takes an action, colour and board as input. Returns a new piece vector that
    represents the move taken by that player and updates the board to reflect it
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
            # If player was captured, convert their piece to the appropriate colour
            if board[neighbour] != 0 and board[neighbour] != colour:
                new_vector[other_player].remove(neighbour)
                new_vector[colour].append(neighbour)
                board[neighbour] = colour
        
        # Update new piece position in the vector
        new_vector[colour].remove(action.origin)
        new_vector[colour].append(action.destination)
        
        # Update the board 
        board[action.origin] = 0
        board[action.destination] = colour
        
        return new_vector
        
    '''
    Called during the update function of the Player class. Creates a new state 
    based on the new information and returns it. 
    '''
    def update_game_state(self,action,colour,score,board):
        
        new_piece_vector = self.update_piece_positions(colour, action, self.board)
        next_player = self.player_turn_order()
        new_score = score[:]
        new_board = np.array(board)

        return BoardState(next_player,new_piece_vector,new_score,new_board)
        
    '''
    Create a new state based on an action 
    '''
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

    '''
    Update the piece vectors and board in the current state without returning a
    new vector. 
    '''
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
    
    '''
    Perform a move on the current state by modifying its attributes. Does not 
    return a new BoardState object or copy any of its attributes.
    '''
    def do_move(self,action):
        self.do_update(self.player_colour, action, self.board)
        if(action.type == "EXIT"):
            self.score[self.player_colour] += 1
        self.score[0] += 1
        self.player_colour = self.player_turn_order()
        self.legal_moves.actions = []
        self.legal_moves.generate_actions(self.player_colour, self.piece_vectors, self.board)
    
    
    '''
    Determines the next player's turn based on the current state
    '''
    def player_turn_order(self):
        if (self.player_colour == 1):
            return 2
        elif( self.player_colour == 2):
            return 3
        else:
            return 1
    '''
    Debug function used to discover discrepancies between the board 
    and the location of the pieces stores in the piece vector.
    '''
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
            
    '''
    Copy the current score
    '''
    def copy_score(self):
        return self.score[:]
    
    '''
    Determines if the current state is a terminal state for the game Chexers.
    Returns true if the maximum number of turns has been reached for each player, 
    or if any player exits four pieces from the board. 
    '''
    def is_terminal_state(self):
        if self.score[0] == 768:
            return True
        if self.score[1] == 4:
            return True
        if self.score[2] == 4:
            return True
        if self.score[3] == 4:
            return True 
        return False
            
    '''
    Based on the current state estimates the current winner given a non terminal
    state, or returns the true winner given a terminal state
    '''
    def get_winner(self):
        winner = None
        max = -999999
        for i in range(1,4):
            temp_score = self.evaluation_function(i)
            if temp_score == 1234567890: 
                return None
            #print(i,temp_score)
            if temp_score > max:
                winner = i
                max = temp_score
        #print("----------")
        return winner
    
    '''
    Evaluation heuristic used to estimate the predicted winner given a state. 
    In practice is used to determine player advantage given a non terminal state.
    '''
    def evaluation_function(self,colour):

        material_weight = len(self.piece_vectors[colour])
        if material_weight == 0:
            material_weight = -10000
        
        opposing_material = np.count_nonzero(self.board)-material_weight
        if opposing_material == 0:
            return 1234567890
        self_exits = self.score[colour]
        opposing_exits = np.sum(self.score[1:]) - self_exits
        if opposing_exits == 0:
            opposing_exits = 0.01
            
        safe = self.safe_pieces(colour)
        
        return self.wins(colour) + 6*(self_exits/opposing_exits) + 2*(material_weight/opposing_material) + 0.5*safe 

    '''
    Checks if the current player has won the game, or if another player has won.
    '''
    def wins(self,colour):
        if self.score[colour] == 4:
            return 10000
        else:   
            for i in range(1,4):
                if i != colour:
                    if self.score[i] == 4:
                        return -10000
            if len(self.piece_vectors[colour]) == 0:
                return -10000
            return 0
    '''
    Evaluates the number of pieces not threatened by a jump from another piece 
    '''
    def safe_pieces(self, colour):
        safe_count = 0
        safe = True
        
        for my_piece in self.piece_vectors[colour]:
            safe = True
            for dir in self.legal_moves.axial_directions: 
                threat_space = (my_piece[0] + dir[0],my_piece[1] + dir[1])
                open_space = (my_piece[0] - dir[0],my_piece[1] - dir[1])
                if open_space in self.legal_moves.valid_board:
                    if threat_space in self.legal_moves.valid_board:
                        if self.board[threat_space] != 0 and self.board[threat_space] != colour: 
                            safe = False
            if safe:
                safe_count += 1
        return safe_count
    
    
    def diff(self, first, second):
        second = set(second)
        return [piece for piece in first if piece not in second]