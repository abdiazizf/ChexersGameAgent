'''
Created on Apr 30, 2019

@author: Jordan
'''

class Action(object):
    '''
    Represents an action taken in a game of Chexers 
    
    origin: The original location of a piece before the move
    destination: The hex where the piece will be after the move
    action_type: JUMP, MOVE or EXIT. The type of move made to reach the destination
    from the origin
    '''
        
    '''
    Formats an actions attributes into the desired output for the simulation
    
    Eg.  (  MOVE, ( (1,0) , (1,1) )  )
         (  JUMP, ( (1,0) , (3,0) )  )
    '''
    def format_output(self):
        return (self.type, ((self.origin), (self.destination)))
    
    '''
    Formats an exit action to the desired output used by the referee
    Eg. ( EXIT, (0,0) )
    '''
    def format_exit(self):
        return (self.type, (self.origin))
       
    
    def __init__(self, origin, direction, action_type):
        self.origin = origin
        self.destination = (origin[0] + direction[0],origin[1] + direction[1])
        self.type = action_type
  
    '''
    Calculate the direction of an action given its origin and destination 
    '''
    def get_direction(self):
        return (self.destination[0] - self.origin[0],self.destination[1] - self.origin[1])
        
    ''' 
    Calculates the location of the neighbouring space given the actions destination 
    '''
    def get_neighbour_space(self):
        direction = self.get_direction()
        return ( (self.origin[0]) + int((direction[0]/2)) , (self.origin[1]) + int((direction[1]/2)) )

    '''
    Compares the equality of two actions 
    '''
    def compare_to(self, other):
        
        if self.origin != other.origin:
            return False
        if self.destination != other.destination:
            return False
        if self.type != other.type:
            return False
        else: 
            return True
        
    
        
        