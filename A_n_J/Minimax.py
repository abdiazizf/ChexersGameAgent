from A_n_J.State import exit_spaces, axial_directions, axial_jump, coordinates
from itertools import chain
class Minimax:
    def __init__(self, initial_state, depth, colour) :
        self.colour = colour
        self.initial_state = initial_state
        self.depth = depth
        self.distance = 0
        self.safe_pieces = []
        self.aggressive_pieces = []
        self.aggressive_safe_pieces = []
        self.aggressive()
        self.hex_distance(exit_spaces)

    def utility_function(self):
        total_score = 0

        return total_score
    '''
       Returns true if both numbers share the same sign, ie + or - 
       '''

    def same_sign(self, q, r):
        return (q < 0 and r < 0) or (q >= 0 and r >= 0)

    '''
    Takes two tuples as input and returns the distance between them in 
    number of hexes
    '''

    def hex_distance(self, exit_spaces):
        list_distances= []
        for piece in self.initial_state.piece_vectors[self.colour]:
            for exit_position in exit_spaces[self.colour]:
                distance_x = exit_position[0] - piece[0]
                distance_y = exit_position[1] - piece[1]
            if self.same_sign(distance_x, distance_y):
                list_distances.append(abs(distance_x + distance_y))
            else:
                list_distances.append(max(abs(distance_x), abs(distance_y)))
            self.distance += min(list_distances)
        return

    def safe_pieces(self):
        safe_pieces = []
        all_pieces = chain.from_iterable(self.initial_state.piece_vectors.values())
        opponent_pieces = diff(all_pieces,self.initial_state.piece_vectors[self.colour])
        for my_piece in self.initial_state.piece_vectors[self.colour]:
            safe = True
            for opponent_piece in opponent_pieces:
                direction = (opponent_piece[0] - my_piece[0], opponent_piece[1] - my_piece[1])
                jump_move = (opponent_piece[0]+ direction[0] * 2, opponent_piece[1]+ direction[1] * 2)
                if direction not in axial_directions or jump_move not in coordinates or jump_move in all_pieces:
                    continue
                safe = False
            if safe :
                self.safe_pieces.append(my_piece)
        return
    #ALSO CONSIDER THE PIECE THAT IS BEING CAPTURED AS WELL OPPONENT MAY CAPTURE IT RIGHT BACK


    #OPPONENT PIECES NOT CONVERTED WHEN CONSIDERING IF A PIECE IS SAFE TO JUMP
    def aggressive(self):
        aggressive_pieces = []
        aggressive_safe_pieces = []
        all_pieces = chain.from_iterable(self.initial_state.piece_vectors.values())
        opponent_pieces = diff(all_pieces, self.initial_state.piece_vectors[self.colour])
        for my_piece in self.initial_state.piece_vectors[self.colour]:
            aggressive = False
            safe = True
            for jump in axial_jump :
                jump_to = (my_piece[0]+jump[0],my_piece[1]+jump[1])
                jump_over = (my_piece[0]+jump[0]/2, my_piece[1]+ jump[1]/2)
                if jump_to not in coordinates or jump_over not in opponent_pieces:
                    continue
                aggressive = True
                for opponent_piece in opponent_pieces:
                    direction = (opponent_piece[0] - jump_to[0], opponent_piece[1] - jump_to[1])
                    jump_move = (opponent_piece[0] + direction[0] * 2, opponent_piece[1] + direction[1] * 2)
                    if direction not in axial_directions or jump_move not in coordinates or jump_move in all_pieces:
                        continue
                    safe = False
            if aggressive:
                self.aggressive_pieces.append(my_piece)
            if aggressive and safe :
                self.aggressive_safe_pieces.append(my_piece)
        return






        return
def diff(first, second) :
    second = set(second)
    return [piece for piece in first if piece not in second]
