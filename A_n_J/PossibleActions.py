'''
Created on Apr 30, 2019

@author: Jordan
'''

from A_n_J.Action import Action

class PossibleActions(object):
    '''
    Holds a list of possible actions for the current board state
    Used in calculation of successor nodes 
    
    
    
    '''
    #possible axial directions
    axial_directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    #possible jump directions
    axial_jump = [(2, 0), (2, -2), (0, -2), (-2, 0), (-2, 2), (0, 2)]
    # off board co-ordinates for generating valid exit moves
    exit_hexes = {'red': [(4, -3),(4,-2),(4,-1)] , 'blue':[(-3,-1),(-2,-2),(-1,-3)] , 'green' :[(-3,4),(-2,4),(-1,4)]}
    
    '''
    Input: current board_state and player colour
    Output: List of valid actions for a given player
    '''
    def generate_actions(self,player_colour,board_state):

        for piece in board_state.piece_vectors[player_colour]:
            for direction in self.axial_directions:
                self.add_action(piece,direction,"MOVE",board_state)
                self.add_action(piece, direction, "EXIT", board_state)
            for jump in self.axial_jump:
                self.add_action(piece,jump,"JUMP",board_state)
                
    '''
    Takes a piece, a direction and a move type as input, creates an action
    and asserts its validity before adding it to the list of possible actions for 
    the current state
    '''
    def add_action(self,piece,direction,move,board_state):
        tempAction = Action(piece,direction,move)
        if(self.valid_action(tempAction,board_state,move) == True):
            self.actions.append(tempAction)
          
    '''
    Returns true if an action would end a piece on the board
    OR returns true if the conditions to jump are met and end would be 
    on the board
    OR returns true if a move would exit the board and is not a jump
    OR returns false if space is occupied
    '''    
    def valid_action(self,action,board_state,move):
        
        if(move == "EXIT"):
            if(action.destination not in self.exit_hexes[board_state.player_colour]):
                return False
        if(action.on_board() != True):
            return False
        for player in board_state.piece_vectors:
            if(action.destination in board_state.piece_vectors[player]):
                return False
        if(move == "JUMP"):
            if not self.has_neighbour_in_jump_direction(action, board_state):
                return False
        return True
    
    def print_moves(self):
        for move in self.actions:
            print(move.format_output())
    
    def has_neighbour_in_jump_direction(self,action,board_state):
        neighbouring_space = action.get_neighbour_space()
        for player in board_state.piece_vectors:
            if neighbouring_space in board_state.piece_vectors[player]:
                return True
        return False
    
    
    '''
    Returns vector of exit hexes for a colour
    '''
    def get_exit_hexes(self,colour):
        return self.exit_hexes[colour]

    def get_actions(self):
        return self.actions

    def __init__(self,board_state):
        '''
        Constructor
        '''
        self.actions = []

        