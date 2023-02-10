import quarto
import numpy as np
import math
from quarto import Quarto, Player, Piece
from copy import deepcopy
import random
from functools import reduce
from operator import and_

class my_Agent(quarto.Player):  
    MAX_DEPTH = 4
    DEFAULT_MOVE = (-1, (-1, -1))

    def __init__(self, quarto: Quarto) -> None:
        super().__init__(quarto)
        self.first_move = True
        self.BOARD_SIDE = 4

    def choose_piece(self) -> int:
        if self.first_move:
            self.first_move = False
            return random.randint(0, (self.BOARD_SIDE ** 2) - 1)
        
        # return self.__minmax('choose')
        return self.__minmax(False)

    def place_piece(self) -> tuple[int, int]:
        if self.first_move:
            self.first_move = False
            x = random.randint(0, self.BOARD_SIDE-1)
            y = random.randint(0, self.BOARD_SIDE-1)
            return (y,x)

        board = self.get_game().get_board_status()
        pieces = self.__get_usable_pieces(self.get_game())

        if(len(pieces) == 1):
            for i in range(self.BOARD_SIDE):
                for j in range(self.BOARD_SIDE):
                     if board[i, j] == -1:
                        return j, i
        # return self.__minmax('place')
        return self.__minmax(True)

    def __minmax(self, action: str):

        def get_scores(winner: int, minmax_turn: int) -> float:
            real_turn = self.get_game().get_current_player()

            if minmax_turn == real_turn:
                my_turn = True
            else:
                my_turn = False

            if winner == -1: 
                return 5 * (-1 if my_turn else 1)
            else: 
                return 10 * (-1 if winner == real_turn else 1)

        def heuristic(board):
            score = 0
            for row in board:
                useful_pieces = row != -1
                if sum(useful_pieces) == 3:
                    if reduce(and_, row[useful_pieces]) != 0 or reduce(and_, row[useful_pieces] ^ 15) != 0:
                        score += 1                

            for col in board.T:
                useful_pieces = col != -1
                if sum(useful_pieces) == 3:
                    if reduce(and_, col[useful_pieces]) != 0 or reduce(and_, col[useful_pieces] ^ 15) != 0:
                        score += 1

            for diag in [board.diagonal(), board[::-1].diagonal()]:
                useful_pieces = diag != -1
                if sum(useful_pieces) == 3:
                    if reduce(and_, diag[useful_pieces]) != 0 or reduce(and_, diag[useful_pieces] ^ 15) != 0:
                        score += 1       
            return score
        
        def alpha_beta_pruning(my_turn: bool, score, alpha, beta):
            if my_turn:
                if score <= alpha:
                    return True, alpha, beta
                return False, alpha, min(beta, score)
            else:
                if score >= beta:
                    return True, alpha, beta
                return False, max(alpha, score), beta

        def min_max(game: Quarto, action: bool, depth: int = 0, alpha = (-math.inf, self.DEFAULT_MOVE), beta = (math.inf, self.DEFAULT_MOVE)) -> tuple[float, tuple[tuple[int, int], int]]:
            minmax_turn = game.get_current_player()

            if minmax_turn == self.get_game().get_current_player():
                my_turn = True
            else:
                my_turn = False

            if depth >= self.MAX_DEPTH:
                return heuristic(game.get_board_status()) * (-1 if my_turn else 1), self.DEFAULT_MOVE

            moves = self.__get_possible_moves(game)
            remaining_pieces = self.__get_usable_pieces(game)

            score = math.inf * (1 if my_turn else -1), self.DEFAULT_MOVE
            winner = game.check_winner()

            # I have to choose a place where to move the piece
            if action == True:
                for move in moves:
                    if game.check_finished() or winner != -1: 
                        val = get_scores(winner, minmax_turn)
                    else:
                        copy_game = deepcopy(game)
                        copy_game.place(*move)
                        val, _ = min_max(copy_game, False, depth + 1, alpha, beta)

                    if my_turn == True:
                        score = min(score, (val, (-1, move)))
                    else:
                        score = max(score, (val, (-1, move)))

                    res, alpha, beta = alpha_beta_pruning(my_turn, score, alpha, beta)
                    if res:
                        break
                return score
            # I have to choose a piece
            elif action == False:
                for piece in remaining_pieces:
                    if game.check_finished() or winner != -1: 
                        val = get_scores(winner, minmax_turn)
                    else:
                        copy_game = deepcopy(game)
                        copy_game.select(piece)
                        copy_game._current_player = 1 - copy_game._current_player
                        val, _ = min_max(copy_game, True, depth + 1, alpha, beta)
                    
                    if my_turn == True:
                        score = min(score, (val, (piece, (-1, -1))))
                    else :
                        score = max(score, (val, (piece, (-1, -1))))

                    res, alpha, beta = alpha_beta_pruning(my_turn, score, alpha, beta)
                    if res:
                        break
                return score

        _, (piece, move) = min_max(self.get_game(), action)
        if action == True:
            return move
        else:
            return piece

    def __get_possible_moves(self, game: Quarto) -> list[tuple[int, int]]:
        return [(j, i) for i in range(0, game.BOARD_SIDE) for j in range(0, game.BOARD_SIDE) if game.get_board_status()[i, j] == -1]

    def __get_usable_pieces(self, game: Quarto) -> list[int]:
        board = game.get_board_status()
        usable_pieces = set([i for i in range(0,16)])

        for i in range(0, self.BOARD_SIDE):
            for j in range(0, self.BOARD_SIDE):
                if (board[i][j] in usable_pieces):
                    usable_pieces.remove(board[i][j])
            
        return usable_pieces
