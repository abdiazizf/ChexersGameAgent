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
    axial_directions = set([(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)])
    # off board co-ordinates for generating valid exit moves
    exit_spaces = {1: set([(3, -3), (3,-2) , (3,-1) , (3, 0)]) , 3:set([(0, -3), (-1,-2) , (-2,-1) , (-3, 0)]) , 2:set([(-3, 3), (-2, 3) , (-1, 3) , (0, 3)])}
    
    #board_coords = {(0,-3): 0, (1,-3):1, (2,-3):2, (3,-3):3, (-1,-2):4, (0,-2):5, (2,-3):2,}
    
    '''
    Input: current board_state and player colour
    Output: List of valid actions for a given player
    '''
    def generate_actions(self,player_colour,pieces,board):

        for piece in pieces[player_colour]:
            for direction in self.axial_directions:
                self.add_action(piece, direction, board, "MOVE", player_colour)
                self.add_action(piece, self.jump(direction), board, "JUMP", player_colour)
            if piece in self.exit_spaces[player_colour]:
                self.add_action(piece, (0,0), board, "EXIT", player_colour)
        if len(self.actions) == 0:
            self.actions.append(Action((0,0),(0,0),"PASS"))

                
    '''
    Takes a piece, a direction and a move type as input, creates an action
    and asserts its validity before adding it to the list of possible actions for 
    the current state
    '''
    def add_action(self,piece,direction,board, move,colour):
        tempAction = Action(piece,direction,move)
        if(self.valid_action(tempAction,board,move,colour) == True):
            self.actions.append(tempAction)
    '''
    Returns true if an action would end a piece on the board
    OR returns true if the conditions to jump are met and end would be 
    on the board
    OR returns true if a move would exit the board and is not a jump
    OR returns false if space is occupied
    '''    
    def valid_action(self,action,board,move,colour):

        if move == "EXIT":
            if action.origin in self.exit_spaces[colour]:
                return True
        # Check hex is on board
        if action.on_board() != True:
            return False
        #Check hex isn't occupied
        if board[action.destination] != 0: 
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

        