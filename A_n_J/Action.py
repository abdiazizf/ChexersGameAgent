'''
Created on Apr 30, 2019

@author: Jordan
'''

class Action(object):
    '''
    Represents an action taken in a game of chexers 
    
    origin: The original location of a piece before the move
    destination: The hex where the piece will be after the move
    action_type: JUMP, MOVE or EXIT. The type of move made to reach the destination
    from the origin
    '''
    
    '''
    Checks to see if a move will end on a valid hex on the game_board
    '''
    def on_board(self):
        if(self.hex_distance(self.destination, (0,0) ) > 3):
            return False
        if (self.destination[0] < -3) or (self.destination[0] > 3):
            return False
        if (self.destination[1] < -3) or (self.destination[1] > 3):
            return False
        else: 
            return True
        
    '''
    Formats an actions attributes into the desired output for the simulation
    
    Eg.  (  MOVE, ( (1,0) , (1,1) )  )
         (  JUMP, ( (1,0) , (3,0) )  )
    '''
    def format_output(self):
        return (self.action_type, ((self.origin), (self.destination)))
    
    def format_exit(self):
        return (self.action_type, (self.origin))
       
    
    def __init__(self, origin, direction, action_type):
        '''
        Constructor
        '''
        self.origin = origin
        self.destination = (origin[0] + direction[0],origin[1] + direction[1])
        self.action_type = action_type
        
        
    def get_direction(self):
        return (self.destination[0] - self.origin[0],self.destination[1] - self.origin[1])
        
    def get_neighbour_space(self):
        direction = self.get_direction()
        return ( int((self.origin[0])) + int((direction[0]/2)) , int((self.origin[1])) + int((direction[1]/2)) )
    '''
    Returns true if both numbers share the same sign, ie + or - 
    '''
    def same_sign(self, q , r) :
        return (q < 0 and r < 0)or (q>=0 and r>= 0)
    
    '''
    Takes two tuples as input and returns the distance between them in 
    number of hexes
    '''
    def hex_distance(self, origin, goal):

        distance_x = goal[0] - origin[0]
        distance_y = goal[1] - origin[1]
        if self.same_sign(distance_x, distance_y):
            return abs(distance_x + distance_y)
        else:
            return max(abs(distance_x), abs(distance_y))
    
        return
        