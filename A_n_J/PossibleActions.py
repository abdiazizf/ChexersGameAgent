'''
Created on Apr 30, 2019

@author: Jordan
'''

from A_n_J.Action import Action

# Set of Axial directions used for action generation.



class PossibleActions(object):
    '''
    Holds a list of possible actions for the current board state
    Used in calculation of successor nodes
    '''
    axial_directions = set([(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)])
    # off board co-ordinates for generating valid exit moves
    exit_spaces = {1: set([(3, -3), (3, -2), (3, -1), (3, 0)]), 3: set([(0, -3), (-1, -2), (-2, -1), (-3, 0)]),
                   2: set([(-3, 3), (-2, 3), (-1, 3), (0, 3)])}
    # Valid positions on the board for a game of Chexers.
    valid_board = set((q, r) for q in range(-3, 4) for r in range(-3, 4) if -q - r in range(-3, 4))
    '''
    Generates a list of legal actions. Takes a colour, piece vector
    and board array as input.  
    '''
    def generate_actions(self,player_colour,pieces,board):

        # For every axial direction consider the legality of the proposed move 
        # and add it to the list of legal actions.  
        # List comprehension is used for efficiency. 
        self.actions = [self._actions(piece,direction,board) for direction in self.axial_directions for piece in pieces[player_colour] if self._actions(piece,direction,board) is not None]
        # For every piece currently in a position to exit the board, add and exit 
        # action to the list 
        exits = [self.exits(piece, player_colour) for piece in pieces[player_colour] if self.exits(piece, player_colour) is not None]
        self.actions.extend(exits)
        # If there are no possible actions the player must pass
        if len(self.actions) == 0:
            self.actions.append(Action((2,2),(2,2),"PASS"))
            
    '''
    Generates exit functions for a piece in a valid position
    '''
    def exits(self,piece,colour):
        if piece in self.exit_spaces[colour]:
                return Action(piece,(0,0),"EXIT")

    '''
    Takes a piece vector, axial direction and a board as input. Checks if 
    the destination of the proposed move is valid given the current board. 
    If the space is unoccupied returns a new action representing the legal move. 
    If the space is occupied checks the conditions for a jump action, and if 
    legal, returns an Action object representing the move. 
    '''
    def _actions(self,piece,direction,board):
        # Calculate the destination of the proposed move
            dest = (piece[0] + direction[0],piece[1] + direction[1])
            if dest not in self.valid_board:
                return None
            if board[dest] == 0:
                return Action(piece,direction,"MOVE")
            else: 
                # Get the neighbour and check the jump destination 
                # is empty. 
                neighbour = dest
                if board[neighbour] != 0:
                    dir = (direction[0]+direction[0],direction[1]+direction[1])
                    dest = (piece[0] + dir[0],piece[1] + dir[1])
                    if dest in self.valid_board:
                        if board[neighbour] != 0 and board[dest] == 0:
                            return Action(piece,dir,"JUMP")
            
    '''
    Debug function that prints the moves stored in self.actions 
    in the format used by the referee. 
    '''
    def print_moves(self):
        for move in self.actions:
            print(move.format_output())
    
    '''
    Returns vector of exit hexes for a colour
    '''
    def get_exit_hexes(self,colour):
        return self.exit_hexes[colour]
    '''
    Returns the list of actions generated. 
    '''
    def get_actions(self):
        return self.actions

    def __init__(self,board_state):
        '''
        Constructor
        '''
        self.actions = []

        