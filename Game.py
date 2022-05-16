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
        print("Player", player1, "with X".rjust(3))
        print("Player", player2, "with O".rjust(3))
        print()
        for x in range(board.n):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(board.n - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(board.n):
                move = i * board.n + j
                player = board.states.get(move, -1)
                if (player == -1):
                    print('_'.center(8), end='')
                elif (player == player1):
                    print('X'.center(8), end='')
                elif (player == player2):
                    print('O'.center(8), end='')
            print('\r\n\r\n')
    
    def start_play(self, player1, player2, start_player = 0, show_board = 1):
        '''
        starts game with two players
        '''
        self.board.init_board(start_player)
        p1, p2 = self.board.players
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2: player2}
        if show_board:
            self.display(self.board, player1.player, player2.player)
        while True:
            cur_player = self.board.get_cur_player()
            player_in_turn = players[cur_player]
            move = player_in_turn.get_action(self.board)
            self.board.do_move(move)
            if show_board:
                self.displaY(self.board, player1.player, player2.player)
            end, winner = self.board.game_done()
            if end:
                if show_board:
                    if winner != -1:
                        print("Game end. Winner is", players[winner])
                    else:
                        print("Game end. Tie")
                return winner

    def start_self_play(self, player, show_board=0, temp=1e-3):
        '''
        starts a self-play game using MCTS, and store the self-play data
        (state, mcts_probs, z) for training
        '''
        self.board.init_board()
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], []
        while True:
            move, move_probs = player.get_action(self.board, temp=temp,
                                                return_prob = 1)
            #store data
            states.append(self.board.cur_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.current_players)
            #perform a move
            self.board.do_move(move)
            if show_board:
                self.display(self.board, p1, p2)
            end, winner = self.board.game_end()
            if end:
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                #reset MCTS root node
                if show_board:
                    if winner != -1:
                        print("Game end. WInner is player:", winner)
                    else:
                        print("Game end. Draw")
                return winner, zip(states, mcts_probs, winners_z)






    








        

        