'''
Created on May 7, 2019

@author: Jordan
'''
from A_n_J.BoardState import BoardState
import datetime 
from random import choice

class MonteCarlo(object):
    
    def __init__(self, board_state, **kwargs):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.board_state = board_state
        self.states = []
        self.max_moves = kwargs.get('max_moves',100)
        
        self.wins = {}
        self.plays = {}
        
        
        seconds = kwargs.get('time',30)
        self.calculation_time = datetime.timedelta(seconds=seconds)
    
    def update(self, state):
        # Takes a game state, and appends it to the history.
        self.states.append(state)

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        
        self.max_depth = 0
        #state = self.states[-1]
        player = self.board_state.player_colour
        
        #generate legal moves
        self.board_state.actions.generate_actions()
        
        if not self.board_state.actions.actions:
            return
        if len(self.board_state.actions.actions) == 1:
            return self.board_state.actions.actions[0]
        
        games = 0
        begin = datetime.datetime.utcnow()
        
        #run simulation 
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games +=1
            
            
        move_states = [(p, self.board_state.generate_successor(p)) for p in self.board_state.actions.actions]
        
        print(games, datetime.datetime.utcnow() - begin)
        
        percent_wins, move = max(
            (self.wins.get((player, S), 0) / 
            self.wins.get((player, S), 0), 
            p)
        for p, S in move_states
            )
        
        for x in sorted(
            ((100 * self.wins.get((player, S), 0) /
              self.plays.get((player, S), 1),
              self.wins.get((player, S), 0),
              self.plays.get((player, S), 0), p)
             for p, S in move_states),
            reverse=True
        ):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))

        print("Maximum depth searched:", self.max_depth)
        
        
        # return highest probability move 
        return move 

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        
        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        cur_player = self.board_state.player_colour
        
        expand = True
        for x in range(self.max_moves):
            #generate legal actions for the state 
            self.board_state.actions.generate_actions()
            
            # Choose an action from the list of possible actions
            action = choice(self.board_state.actions.actions)
            
            #generate new state from the chosen action
            state = self.board_state.generate_successor(action)
            
            states_copy.append(state)
            
            ##########################
            
            if expand and (cur_player,state) not in self.plays:
                expand = False
                self.plays[(cur_player,state)] = 0
                self.wins[(cur_player, state)] = 0
            
            visited_states.add((cur_player,state))
            
            player = self.board_state.player_colour
            ##########################
            
            # if the game is over
            winner = self.board_state.evaluater.is_gameover()
            if winner: 
                break
            
        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[(player,state)] += 1
            if player == winner:
                self.wins[(player,state)] += 1