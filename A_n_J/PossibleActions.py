'''
Created on Apr 30, 2019

@author: Jordan
'''

from A_n_J.Action import Action
from mpmath import acsc



class PossibleActions(object):
    '''
    Holds a list of possible actions for the current board state
    Used in calculation of successor nodes 
    
    
    
    '''
    #possible axial directions
    axial_directions = set([(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)])
    # off board co-ordinates for generating valid exit moves
    exit_spaces = {1: set([(3, -3), (3,-2) , (3,-1) , (3, 0)]) , 3:set([(0, -3), (-1,-2) , (-2,-1) , (-3, 0)]) , 2:set([(-3, 3), (-2, 3) , (-1, 3) , (0, 3)])}
    
    #board_coords = {(0,-3): 0, (1,-3):1, (2,-3):2, (3,-3):3, (-1,-2):4, (0,-2):5, (2,-3):2,}
    
    valid_board = set((q, r) for q in range(-3, 4) for r in range(-3, 4) if -q - r in range(-3, 4))
    
    '''
    Input: current board_state and player colour
    Output: List of valid actions for a given player
    '''
    def generate_actions(self,player_colour,pieces,board):

        self.actions = [self._actions(piece,direction,board) for direction in self.axial_directions for piece in pieces[player_colour] if self._actions(piece,direction,board) is not None]
        exits = [self.exits(piece, player_colour) for piece in pieces[player_colour] if self.exits(piece, player_colour) is not None]

        self.actions.extend(exits)
        
        if len(self.actions) == 0:
            self.actions.append(Action((0,0),(0,0),"PASS"))

            
    def exits(self,piece,colour):
        if piece in self.exit_spaces[colour]:
                return Action(piece,(0,0),"EXIT")

    def _actions(self,piece,direction,board):
            dest = (piece[0] + direction[0],piece[1] + direction[1])
            if dest not in self.valid_board:
                return None
            if board[dest] == 0:
                return Action(piece,direction,"MOVE")
            else: 
                neighbour = dest
                if board[neighbour] != 0:
                    dir = (direction[0]+direction[0],direction[1]+direction[1])
                    dest = (piece[0] + dir[0],piece[1] + dir[1])
                    if dest in self.valid_board:
                        if board[neighbour] != 0 and board[dest] == 0:
                            return Action(piece,dir,"JUMP")
            
    
    '''
    Takes a piece, a direction and a move type as input, creates an action
    and asserts its validity before adding it to the list of possible actions for 
    the current state
    '''
    def add_action(self,piece,direction,board, move,colour):
        tempAction = Action(piece,direction,move)
        if(self.valid_action(tempAction,board,move,colour) == True):
            return tempAction
    '''
    Returns true if an action would end a piece on the board
    OR returns true if the conditions to jump are met and end would be 
    on the board
    OR returns true if a move would exit the board and is not a jump
    OR returns false if space is occupied
    '''    
    def valid_action(self,action,board,move,colour):

        dest = action.destination
        if move == "EXIT":
            if action.origin in self.exit_spaces[colour]:
                return True
        # Check hex is on board
        if dest not in self.valid_board:
            return False
        #Check hex isn't occupied
        if board[dest] != 0: 
            return False
        if move == "JUMP": 
            if not self.has_neighbour_in_jump_direction(action, board):
                return False

        return True
            
    
    def print_moves(self):
        for move in self.actions:
            print(move.format_output())
    
    def has_neighbour_in_jump_direction(self,action,board):
        neighbouring_space = action.get_neighbour_space()

        if board[neighbouring_space] == 0:
            return False
        else:
            return True
    
    def jump(self,direction):
        return (direction[0]*2,direction[1]*2)
    
    
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

        