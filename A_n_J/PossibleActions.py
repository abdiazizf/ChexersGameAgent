'''
Created on Apr 30, 2019

@author: Jordan
'''

import A_n_J.Action

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

    possible_actions = []
    
    def generate_actions(self,player_colour,board_state):
        '''
        Input: current board_state and player colour
        Output: List of valid actions for a given player
        '''
        for piece in board_state[player_colour]:
            for direction in self.axial_directions:
                self.add_action(piece,direction,"MOVE",board_state)
                self.add_action(piece, direction, "EXIT", board_state)
            for jump in self.axial_jump:
                self.add_action(piece,jump,"JUMP",board_state)
                
    
    def add_action(self,piece,direction,move,board_state):
        tempAction = A_n_J.Action(piece,direction,move)
        if(self.valid_action(tempAction,board_state,move,direction) == True):
            self.possible_actions.append(tempAction)
          
              
    def valid_action(self,action,board_state,move,direction):
        '''
        Returns true if an action would end a piece on the board
        OR returns true if the conditions to jump are met and end would be 
        on the board
        OR returns true if a move would exit the board and is not a jump
        '''
        if(move == "EXIT"):
            if(action.destination not in self.exit_hexes[self.player_colour]):
                return False
        if(move == "JUMP"):
            if(action.destination-direction/2) not in board_state:
                return False    
        if(action.on_board() != True):
            return False
        if(action.destination in board_state):
            return False
        return True

    def __init__(self, colour):
        '''
        Constructor
        '''
        self.player_colour = colour
        