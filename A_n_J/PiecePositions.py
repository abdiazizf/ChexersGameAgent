'''
Created on Apr 28, 2019

@author: Jordan
'''

class GameState(object):
    '''
    Representation of the current board state in a game of Chexers
    '''
    
    def construct_piece_vectors(self):
        
        piece_vectors = {}
        
        piece_vectors["red"] = [(-3,0),(-3,1),(-3,2),(-3,3)]
        piece_vectors["green"] = [(0,-3),(1,-3),(2,-3),(3,-3)]
        piece_vectors["blue"] =  [(3,0),(2,1),(1,2),(0,3)]
        
        return piece_vectors
    
    def update_piece_positions(self,colour,action):
        origin = action[0]
        new_position = action[1]
        self.piece_vectors[colour][origin] = new_position

    def __init__(self, params):
        '''
        Constructor
        '''
        self.piece_vectors = self.construct_piece_vectors(self)
        
    def __eq__(self, other):
        return
    def __hash__(self):
        return
    def __str__(self):
        return
    