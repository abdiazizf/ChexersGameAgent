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
    
    '''
    
    def __init__(self, player_colour,piece_vector,score):
        self.player_colour = player_colour
        self.piece_vectors = deepcopy(piece_vector)
        self.legal_moves = PossibleActions(self)
        self.legal_moves.generate_actions(player_colour,self)
        self.score = score
        self.players_max_move = 0
        
    '''
    Takes an action and player colour as input, returns a new piece vector that
    represents the move taken by that player
    '''
    def update_piece_positions(self,colour,action):
        new_vector = {}
        
        red = deepcopy(self.piece_vectors['red'])
        blue = deepcopy(self.piece_vectors['blue'])
        green = deepcopy(self.piece_vectors['green'])
        
        new_vector['red'] = red
        new_vector['green'] = green
        new_vector['blue'] = blue
        
        if(action.action_type == "PASS"):
            self.score[self.player_colour]["turns"] += 1
            return new_vector
        
        origin = action.origin
        destination = action.destination
        if(action.action_type == "EXIT"):
            self.score[colour]["exits"] +=1
            new_vector[colour].remove(origin)
        elif(action.action_type == "JUMP"):
            neighbour = action.get_neighbour_space()
            pc = None
            piece_taken = False
            for player in new_vector:
                for piece in new_vector[player]:
                    if piece == neighbour:
                        pc = player
                        piece_taken = True
            new_vector[colour].remove(origin)
            new_vector[colour].append(destination)
            if piece_taken == True:
                new_vector[pc].remove(neighbour)
                new_vector[colour].append(neighbour)
        else:
            new_vector[colour].remove(origin)
            new_vector[colour].append(destination)
        self.score[self.player_colour]["turns"] += 1
        return new_vector
        
    def update_board_state(self,action,colour,score):
        new_piece_vector = self.update_piece_positions(colour, action)
        next_player = self.player_turn_order()
        new_score = deepcopy(score)

        return BoardState(next_player,new_piece_vector,new_score)
        
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
    
    def is_terminal_state(self):
        max_moves = 0
        if not self.piece_vectors[self.player_colour]:
            return True
        for player in self.score:
            if self.score[player]["exits"] == 4:
                return True
            if self.score[player]["turns"] >= 256:
                max_moves +=1
        if max_moves == 3:
            return True
        else:
            return False
            
    def get_winner(self):
        for player in self.score:
            if self.score[player]['exits'] == 4:
                return player
    '''
    Defines comparison of two board states
    '''
    def __eq__(self, other):
        return all(self.piece_vectors == other.piece_vectors)
    def __hash__(self):
        return
    def __str__(self):
        return
    