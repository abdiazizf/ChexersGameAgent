'''
Created on May 7, 2019

@author: Jordan
'''

class Evaluater(object):
    '''
    This class handles the evaluation of a board state with regards to the 
    utility for a given player colour
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
    
    '''
    Assesses a board state and returns the evaluated utility of a given state 
    in regards to player colour 
    '''
    def get_utility(self,state,colour):
        
        goal = state.actions.get_exit_hexes()
        
        num_player_pieces = len(self.piece_vectors[self.player_colour])
        num_opponent_pieces = 0
        for player in self.board_state:
            num_opponent_pieces += len(self.board_state[player])
            
        num_opponent_pieces = num_opponent_pieces - num_player_pieces
        
        sum_distance = self.sum_distance_to_goal(state.piece_vectors[colour], goal)
        
        utility = num_opponent_pieces + num_player_pieces + sum_distance
        
        return utility 
    
    
    '''
    Returns true if both numbers share the same sign, ie + or - 
    '''
    def same_sign(self,q , r) :
        return (q < 0 and r < 0)or (q>=0 and r>= 0)
    
    '''
    Takes two tuples as input and returns the distance between them in 
    number of hexes
    '''
    def hex_distance(self,origin, goal):

        distance_x = goal[0] - origin[0]
        distance_y = goal[1] - origin[1]
        if self.same_sign(distance_x, distance_y):
            return abs(distance_x + distance_y)
        else:
            return max(abs(distance_x), abs(distance_y))
    
        return
    
    '''
    Returns the summed distance of each piece to the nearest exit 
    '''
    def sum_distance_to_goal(self,piece_vector,goal):
        total = 0
        for piece in piece_vector:
            min_dist = self.hex_distance(piece, self.nearest_goal(piece, goal))
            total += min_dist
        return total
            
    '''
    Takes a board state and piece tuple as input and returns the nearest exit 
    hex for the piece
    '''
    def nearest_goal(self,state,piece):
        exits = state.actions.get_exit_hexes()
        min_dist = self.hex_distance(piece, exits[0])
        min_hex = exits[0]
        for hexes in exits:
            temp_dist = self.hex_distance(piece,hexes)
            if(temp_dist < min_dist):
                min_hex = hexes
                min_dist = temp_dist
                 
        return min_hex
    
    '''
    Returns true if the current game state is a terminal state. ie, the game 
    is over. 
    '''
    def is_gameover(self):
        for colour in self.piece_vectors:
            if len(self.piece_vectors[colour]) == 0:
                return True
            else: return False