
import A_n_J.BoardState


class ExamplePlayer:
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
        self.board_state = A_n_J.BoardState(colour,initial_pieces)
        self.pieces_exited = 0


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
        # TODO: Decide what action to take.
        
        # JUMP, MOVE, PASS, EXIT 

        #actionTaken = action.format_output()
        
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
        # TODO: Update state representation in response to action.
        self.board_state = self.board_state.update_piece_positions(colour,action)

    
    '''
    Returns a dictionary of vectors containing the initial positions of the 
    pieces for each player on the board. Used during setup of a board_state
    '''
    def construct_piece_vectors(self):
        
        piece_vectors = {}
        piece_vectors["red"] = [(-3,0),(-3,1),(-3,2),(-3,3)]
        piece_vectors["green"] = [(0,-3),(1,-3),(2,-3),(3,-3)]
        piece_vectors["blue"] =  [(3,0),(2,1),(1,2),(0,3)]
        
        return piece_vectors
        
        