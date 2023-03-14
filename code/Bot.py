import random

from Game import *

TRANSPOSITION_TABLE = {}


def min_max(game, alpha=-np.inf, beta=np.inf):

    # Base Case
    if game.game_outcome != GameOutcome.INCONCLUSIVE:
        return game.game_outcome.get_evaluation()

    if game.turn_team == Team.TEAM1:
        best_eval = -np.inf
    elif game.turn_team == Team.TEAM2:
        best_eval = np.inf
    else:
        return NotImplemented

    # Recursive Case
    for move in game.get_possible_moves():

        game.make_move(move)
        board_tuple = tuple(map(tuple, game.board))
        if board_tuple in TRANSPOSITION_TABLE:
            curr_eval = TRANSPOSITION_TABLE[board_tuple]
        else:
            curr_eval = min_max(game)
            TRANSPOSITION_TABLE[board_tuple] = curr_eval
        game.undo_move()

        if game.turn_team == Team.TEAM1:
            best_eval = max(best_eval, curr_eval)
            alpha = max(alpha, best_eval)
        elif game.turn_team == Team.TEAM2:
            best_eval = min(best_eval, curr_eval)
            beta = min(beta, best_eval)

        if beta <= alpha:
            break

    return best_eval


def get_best_move(game):

    # Opening Book
    if game.piece_count == 0:
        num = random.randint(0, 10)
        if random.randint(0, 10) <= 4:
            return 1, 1
        elif num <= 9:
            return random.choice([0, 2]), random.choice([0, 2])
        else:
            return random.choice(((0, 1), (1, 0), (1, 2), (2, 1)))

    move_evaluations = {}
    for move in game.get_possible_moves():
        game.make_move(move)
        move_evaluations[move] = min_max(game)
        game.undo_move()

    if move_evaluations:
        best_eval = 0
        if game.turn_team == Team.TEAM1:
            best_eval = max(move_evaluations.values())
        elif game.turn_team == Team.TEAM2:
            best_eval = min(move_evaluations.values())
        move_candidates = [move for move in move_evaluations.keys() if move_evaluations[move] == best_eval]
        best_move = random.choice(move_candidates)
        return best_move

    return None
