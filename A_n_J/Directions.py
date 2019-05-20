'''
Created on May 17, 2019

@author: Jordan
'''


    #possible axial directions
axial_directions = set([(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)])
    # off board co-ordinates for generating valid exit moves
exit_spaces = {1: set([(3, -3), (3,-2) , (3,-1) , (3, 0)]) , 3:set([(0, -3), (-1,-2) , (-2,-1) , (-3, 0)]) , 2:([(-3, 3), (-2, 3) , (-1, 3) , (0, 3)])}