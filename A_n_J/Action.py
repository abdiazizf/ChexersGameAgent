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
        return (self.action_type,(self.origin,self.destination))
       

    def __init__(self, origin, direction, action_type):
        '''
        Constructor
        '''
        self.origin = origin
        self.destination = origin+direction
        self.action_type = action_type
        