# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

"""
from __future__ import print_function
import pickle
from Game import Board, Game
from mcts import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
from policy_value_network import PolicyValueNet 
import tensorflow as tf
import argparse

class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run(model_name, start_player):
    n = 5
    width, height = 15, 15
    
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)
        best_policy = PolicyValueNet(width, height, model_file = model_name)
        mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=1000)

        # human player, input your move in the format: 2,3
        human = Human()

        # set start_player=0 for human first
        game.start_play(human, mcts_player, start_player=start_player, is_shown=1)
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    # parse the commandline
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help = "initial model if needed e.g. (number).model")
    parser.add_argument('--start', help = "0: Human goes first, 1: AI goes first")
    args = parser.parse_args()
    tf.compat.v1.disable_eager_execution()
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    run(args.model, int(args.start))
