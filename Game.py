import numpy as np


"""
Defines Go Board and Game classes
"""

class Board(object):
    '''
    Game Board
    '''

    def __init__(self, n):
        '''
        initialize board with n x n board
        states: dictionary with key = move, value = player
        move is a natural number defined as follows if n = 3
        7 8 9
        4 5 6
        1 2 3
        '''
        self.n = n 
        self.n_in_row = 5
        self.states = {}
        self.players = [1, 2]
    

    def init_board(self, start_player = 0):
        '''
        initializes current_player, available moves, and states
        start_player: index 0 or 1 to denote players 1 and 2
        avals: list of possible moves (moves that have not been played)
        last_move: last move played on this board
        '''
        self.cur_player = self.players[start_player]
        self.avals = set(range(self.n * self.n))
        self.states = {}
        self.last_move = -1
    
    def move_to_coord(self, move):
        '''
        converts move into coordinate format [h, w]
        7 8 9       (2,0) (2,1) (2,2)
        4 5 6  -->  (1,0) (1,1) (1,2)
        1 2 3       (0,0) (0,1) (0,2) 
        '''
        return [move // self.n, move % self.n]

    
    def coord_to_move(self, coord):
        '''
        converts coordinate format to move
        '''
        return coord[0] * self.n + coord[1]


    def make_move(self, move):
        '''
        makes a move 
        '''
        self.states[move] = self.cur_player
        self.avals.remove(move)
        self.cur_player = (
            1 if self.cur_player == 2
            else 2
        )
        self.last_move = move

    def has_winner(self):
        '''
        returns [True, player] if game won
        returns [False, -1] if no one won 
        '''
        states = self.states
        moved = list(set(range(self.n*self.n)) - self.avals) #list of made moves
        if len(moved) < 9:
            return False, -1
        
        for m in moved:
            h, w = self.move_to_coord(m)
            player = states[m]

            if (w in range(self.n - 5 + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + 5))) == 1):
                return True, player

            if (h in range(self.n - 5 + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + 5 * self.n, self.n))) == 1):
                return True, player

            if (w in range(self.n - 5 + 1) and h in range(self.n - 5 + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + 5 * (self.n + 1), self.n + 1))) == 1):
                return True, player

            if (w in range(5 - 1, self.n) and h in range(self.n - 5 + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + 5 * (self.n - 1), self.n - 1))) == 1):
                return True, player
    
        return False, -1
    
    def game_done(self):
        '''
        check if the game is done
        '''
        if (len(self.avals) == 0): #draw
            return True, -1
        return self.has_winner()
    
    def get_cur_player(self):
        '''
        returns current player (1 or 2)
        '''
        return self.cur_player

    '''
    returns board state where its shape is (4,n,n) from the cur_player's pespective
    Each of the 4 elements contains a (nxn) board where
    state[0]: cur_players' moves marked by 1.0 on the board
    state[1]: opponenent's moves marked by 1.0 on the board
    state[2]: last move's location marked by 1.0 on the board
    state[3]: all 1 if both players went, all 0 otherwise
    '''
    def cur_state(self):
        state = np.zeros((4, self.n, self.n))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            curr_moves = moves[players == self.cur_player]
            oppo_moves = moves[players != self.cur_player]
            state[0][curr_moves // self.n, curr_moves % self.n] = 1.0
            state[1][oppo_moves // self.n, oppo_moves % self.n] = 1.0
            state[2][self.last_move // self.n, self.last_move % self.n] = 1.0
        
        if len(self.states) % 2 == 0:
            state[3][:, :] = 1.0
        
        return state[:, ::-1, :] #flip board vertically for visual


class Game(object):
    '''
    Game Server
    '''

    def __init__(self, board):
        self.board = board
    
    def display(self, board, player1, player2):
        '''
        Displays the board with game info
        '''
        






        

        