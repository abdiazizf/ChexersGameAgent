
from A_n_J.BoardState import BoardState
from A_n_J.MonteCarlo import MonteCarlo
from A_n_J.MCNode import MCNode
from A_n_J.Action import Action
from copy import deepcopy
import random

import numpy as np


class Player:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (Red, Green or Blue). The value will be one of the 
        strings "red", "green", or "blue" correspondingly.
        """
        # TODO: Set up state representation.
        
        initial_pieces = self.construct_piece_vectors()
        self.initial_score = self.construct_score_dict()
        self.current_score = self.initial_score[:]


        self.pieces_exited = 0

        self.colour = colour
        
        # Setup board representation
        self.board = np.array([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        i = 0
        for player in initial_pieces:
            for piece in player:
                self.board[piece] = i
            i+= 1 

        self.initial_state = BoardState(1,initial_pieces,self.initial_score,self.board)
        self.current_board = np.array(self.board)
        self.current_state = BoardState(1,initial_pieces,self.initial_score,self.board)
        self.root_node = MCNode(self.initial_state)
        self.mcAI = MonteCarlo(self.root_node)

                
    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. If there are no allowed 
        actions, your player must return a pass instead. The action (or pass) 
        must be represented based on the above instructions for representing 
        actions.
        """

        
        # JUMP, MOVE, PASS, EXIT 
        #action = self.mcAI.best_action(1)
        self.current_state.legal_moves.generate_actions
        action = random.choice(self.current_state.legal_moves.actions)
        if action:
            if not 'type' in action.__dict__:
                return ("PASS", None)
            if action.type == "PASS":
                return ("PASS", None)
            elif(action.type == "EXIT"):
                return action.format_exit()
            else:    
                return action.format_output()
        else:
            return ("PASS", None)


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red", 
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or 
        pass) conforming to the above instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        (or pass) for the player colour (your method does not need to validate 
        the action/pass against the game rules).
        """
        
        new_score = self.current_score[:]
        new_score[0] += 1 
        new_action = self.convert_sim_action(action)
        
        self.current_state.validate_board()
        
        self.current_state = self.current_state.update_game_state(new_action,self.convert_colour(colour),new_score,self.current_state.board)
        
        #Update new root node in tree
        new_node = MCNode(self.current_state)
        for child in self.mcAI.initial_node.children:
            if child.generated_by.compare_to(new_action) == True:
                new_node = child
                
        self.mcAI.initial_node = new_node

    
    '''
    Returns a dictionary of vectors containing the initial positions of the 
    pieces for each player on the board. Used during setup of a board_state
    '''

    def convert_colour(self,colour):
        if colour == 'red':
            return 1 
        elif colour == 'green':
            return 2
        elif colour == 'blue':
            return 3
        
    def construct_piece_vectors(self):
        
        piece_vectors = []
        piece_vectors.append([])
        piece_vectors.append([(-3,0),(-3,1),(-3,2),(-3,3)])
        piece_vectors.append([(0,-3),(1,-3),(2,-3),(3,-3)])
        piece_vectors.append([(3,0),(2,1),(1,2),(0,3)])
        
        return piece_vectors
        
    def construct_score_dict(self):
        
        return [0,0,0,0]
        
    def convert_sim_action(self,action):
        type = action[0]
        if (type == "PASS"):
            return Action((0,0),(0,0),"PASS")
        if (type == "EXIT"):
            origin = action[1]
            direction = (0,0)
            return Action(origin,direction,type)
        else: 
            origin = action[1][0]
            destination = action[1][1]
    
            direction = (destination[0] - origin[0],destination[1] - origin[1])
            
            return Action(origin,direction,type)
        