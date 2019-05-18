'''
Created on Apr 28, 2019

@author: Jordan
'''
from copy import deepcopy
from itertools import chain

#possible axial directions
axial_directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
#possible jump directions
axial_jump = [(2, 0), (2, -2), (0, -2), (-2, 0), (-2, 2), (0, 2)]
# off board co-ordinates for generating valid exit moves
exit_spaces = {'red': [(3, -3), (3, -2), (3, -1), (3, 0)], 'blue': [(0, -3), (-1, -2), (-2, -1),  (-3, 0)], 'green': [(-3, 3), (-2, 3), (-1, 3), (0, 3)]}
coordinates = [(q, r) for q in range(-3, +3 + 1) for r in range(-3, +3 + 1) if -q - r in range(-3, +3 + 1)]

MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"
PASS = "PASS"

class State:
    '''
    Representation of the current board state in a game of Chexers
    
    player_colour: the colour of the pieces owned by the player
    piece_vectors: a vector of all piece positions on a board
    actions: Instance of PossibleActions class containing the valid moves for 
             a given board state.
    '''

    def __eq__(self, other):
        return all(self.piece_vectors == other.piece_vectors)

    def __init__(self, colour_turn, piece_vector, score, depth):
        self.legal_move = []
        self.depth = depth
        self.colour_turn = colour_turn
        self.piece_vectors = piece_vector
        self.successor_state = []
        self.score = score
        self.players_max_move = 0
        self.legal_moves()
        self.successor_states()

    def successor_states(self):
        if self.depth == 0:
            return
        for move in self.legal_moves :
            new_player_pieces, score = self.update_piece_positions(move)
            player_turn = self.next_player()
            new_state = State(player_turn, new_player_pieces, score, self.depth)
            self.successor_state.append(new_state)

    def update_piece_positions(self, move):
        new_piece_vector = deepcopy(self.piece_vectors)
        score = deepcopy(self.score)
        score[self.colour_turn]['turns'] += 1
        if move[0] == MOVE:
            index = new_piece_vector[self.colour_turn].index(move[1][0])
            new_piece_vector[self.colour_turn][index] = move[1][1]
            return new_piece_vector, score
        elif move[0] == EXIT:
            index = new_piece_vector[self.colour_turn].index(move[1])
            new_piece_vector[self.colour_turn].pop(index)
            score[self.colour_turn]['exits'] += 1
            return new_piece_vector, score

        elif move[0] == JUMP:
            jumped_colour = None
            index = new_piece_vector[self.colour_turn].index(move[1][0])
            neighbour = (move[1][1][0] - move[1][0][0], move[1][1][1] - move[1][0][1])
            new_piece_vector[self.colour_turn][index] = move[1][1]
            for player in new_piece_vector:
                for pieces in new_piece_vector[player]:
                    if neighbour in pieces:
                        jumped_colour = player
            if self.colour_turn != jumped_colour:
                j_index = new_piece_vector[jumped_colour].index(neighbour)
                new_piece_vector[jumped_colour].pop(j_index)
                new_piece_vector[self.colour_turn].append(neighbour)
            else:
                return new_piece_vector, score
        return new_piece_vector, score



    def legal_moves(self):
        player_pieces = self.piece_vectors[self.colour_turn]
        pieces = chain.from_iterable(self.piece_vectors.values())
        a = list(pieces)
        for piece in player_pieces:
            if piece in exit_spaces[self.colour_turn]:
                self.legal_move.append((EXIT, piece))
            for i in axial_directions:

                potential_move = (piece[0] + i[0], piece[1] + i[1])
                if potential_move not in coordinates or potential_move in a:
                    continue
                self.legal_move.append((MOVE, (piece, potential_move)))

            for i in axial_jump:
                potential_jump = (piece[0] + i[0], piece[1] + i[1])
                if potential_jump not in coordinates or potential_jump in pieces:
                    continue
                elif (potential_jump[0] - (i[0] / 2), potential_jump[1] - (i[1] / 2)) in pieces:
                    self.legal_move.append((JUMP, (piece, potential_jump)))
                else:
                    continue
        if not self.legal_move:
            self.legal_move.append([(PASS, None)])

        return self.legal_move

    '''
    Takes an action and player colour as input, returns a new piece vector that
    represents the move taken by that playerel
    '''

        
    def next_player(self):
        if (self.colour_turn == "red"):
            return 'green'
        elif( self.colour_turn == 'green'):
            return 'blue'
        else:
            return 'red'



    