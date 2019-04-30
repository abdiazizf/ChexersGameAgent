'''
Created on Apr 30, 2019

@author: Jordan
'''

class Action(object):
    '''
    Represents an action
    '''
    
    
    def on_board(self):
        '''
        Checks to see if a move will end on the game_board
        '''
        if (self.destination[0] < -3) or (self.destination[0] > 3):
            return False
        if (self.destination[1] < -3) or (self.destination[1] > 3):
            return False
        else: 
            return True
        
    def format_output(self):
        return (self.action_type,(self.origin,self.destination))
       

    def __init__(self, origin, direction, action_type):
        '''
        Constructor
        '''
        self.origin = origin
        self.destination = origin+direction
        self.action_type = action_type
        