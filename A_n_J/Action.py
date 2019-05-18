'''
Created on Apr 30, 2019

@author: Abdiaziz Farah and Jordan
'''
ran = range(-3, +3 + 1)
coordinates = [(q, r) for q in ran for r in ran if -q - r in ran]


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
        return self.destination in coordinates
    '''
    Formats an actions attributes into the desired output for the simulation
    
    Eg.  (  MOVE, ( (1,0) , (1,1) )  )
         (  JUMP, ( (1,0) , (3,0) )  )
    '''
    def format_output(self):
        return (self.action_type, ((self.origin), (self.destination)))
    
    def format_exit(self):
        return (self.action_type, (self.origin))

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

    def compare_to(self, other):

        if self.origin != other.origin:
            return False
        if self.destination != other.destination:
            return False
        if self.action_type != other.action_type:
            return False
        else:
            return True


