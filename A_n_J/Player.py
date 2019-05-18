from A_n_J.State import State
import random
import cProfile
from copy import deepcopy


# # JUMP, MOVE, PASS, EXIT
# profile = cProfile.Profile()
# profile.enable()#
# profile.disable()
# profile.print_stats()
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

        initial_pieces = self.position_initialisation()
        self.score = self.score_initialisation()
        self.state = State("red", initial_pieces, self.score, 0)
        self.pieces_exited = 0
        self.colour = colour

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

        return random.choice(self.state.legal_move)

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

        new_score_vector, score = self.state.update_piece_positions(action)
        self.state = State(self.state.next_player(), new_score_vector, score, 0)
        return

    '''
    Returns a dictionary of vectors containing the initial positions of the 
    pieces for each player on the board. Used during setup of a board_state
    '''

    def position_initialisation(self):
        piece_vectors = {}
        piece_vectors["red"] = [(-3, 0), (-3, 1), (-3, 2), (-3, 3)]
        piece_vectors["green"] = [(0, -3), (1, -3), (2, -3), (3, -3)]
        piece_vectors["blue"] = [(3, 0), (2, 1), (1, 2), (0, 3)]

        return piece_vectors

    def score_initialisation(self):
        score = {}
        score["red"] = {"exits": 0, "turns": 0}
        score["green"] = {"exits": 0, "turns": 0}
        score["blue"] = {"exits": 0, "turns": 0}

        return score

