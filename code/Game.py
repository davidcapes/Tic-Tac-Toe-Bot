import enum
import numpy as np


class Team(enum.Enum):
    TEAM1 = 1
    TEAM2 = 2

    def __hash__(self):
        return self.value

    def __str__(self):
        return "Team" + str(self.value)

    def __repr__(self):
        return str(self)

    def to_char(self):
        return str(self.value)

    def get_enemy(self):
        if self == Team.TEAM1:
            return Team.TEAM2
        elif self == Team.TEAM2:
            return Team.TEAM1
        return NotImplemented


class GameOutcome(enum.Enum):
    INCONCLUSIVE = "Inconclusive"
    DRAW = "Draw"
    TEAM1_WINS = "Team1 Wins"
    TEAM2_WINS = "Team2 Wins"

    @staticmethod
    def get_winning_outcome(team):
        if team == Team.TEAM1:
            return GameOutcome.TEAM1_WINS
        elif team == Team.TEAM2:
            return GameOutcome.TEAM2_WINS
        return NotImplemented

    def get_evaluation(self):
        if self == GameOutcome.TEAM1_WINS:
            return 1
        elif self == GameOutcome.TEAM2_WINS:
            return -1
        elif self == GameOutcome.DRAW or self == GameOutcome.INCONCLUSIVE:
            return 0
        return NotImplemented

    def __str__(self):
        return self.value


class Game:

    def __init__(self, rows, columns, max_run):

        # Board related attributes.
        self.rows = rows
        self.columns = columns
        self.max_run = max_run
        self.board = np.empty((rows, columns), Team)
        self.piece_count = 0

        # Game related attributes.
        self.game_outcome = GameOutcome.INCONCLUSIVE
        self.turn_team = Team.TEAM1
        self.previous_moves = []

    def __str__(self):
        board_chars = []
        for r in range(self.rows):
            for c in range(self.columns):
                if self.board[r][c] is None:
                    board_chars.append('-')
                else:
                    board_chars.append(self.board[r][c].to_char())
            board_chars.append('\n')
        return ''.join(board_chars)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __update_game_outcome__(self, max_run, prev_move):
        prev_move_row, prev_move_column = prev_move
        if self.board[prev_move_row][prev_move_column] is None:
            return GameOutcome.INCONCLUSIVE

        # Horizontal
        curr_run = 1
        r = prev_move_row
        c = prev_move_column
        while 0 <= c - 1 < self.columns and self.board[r][c] == self.board[r][c - 1]:
            curr_run += 1
            if curr_run >= max_run:
                if self.board[r][c] == Team.TEAM1:
                    return GameOutcome.TEAM1_WINS
                elif self.board[r][c] == Team.TEAM2:
                    return GameOutcome.TEAM2_WINS
            c -= 1
        c = prev_move_column
        while 0 <= c + 1 < self.columns and self.board[r][c] == self.board[r][c + 1]:
            curr_run += 1
            if curr_run >= max_run:
                if self.board[r][c] == Team.TEAM1:
                    return GameOutcome.TEAM1_WINS
                elif self.board[r][c] == Team.TEAM2:
                    return GameOutcome.TEAM2_WINS
            c += 1

        # Vertical
        curr_run = 1
        r = prev_move_row
        c = prev_move_column
        while 0 <= r - 1 < self.rows and self.board[r][c] == self.board[r - 1][c]:
            curr_run += 1
            if curr_run >= max_run:
                if self.board[r][c] == Team.TEAM1:
                    return GameOutcome.TEAM1_WINS
                elif self.board[r][c] == Team.TEAM2:
                    return GameOutcome.TEAM2_WINS
            r -= 1
        r = prev_move_row
        while 0 <= r + 1 < self.rows and self.board[r][c] == self.board[r + 1][c]:
            curr_run += 1
            if curr_run >= max_run:
                if self.board[r][c] == Team.TEAM1:
                    return GameOutcome.TEAM1_WINS
                elif self.board[r][c] == Team.TEAM2:
                    return GameOutcome.TEAM2_WINS
            r += 1

        # Downwards Diagonal
        curr_run = 1
        r = prev_move_row
        c = prev_move_column
        while 0 <= r - 1 < self.rows and 0 <= c - 1 < self.columns and self.board[r][c] == self.board[r - 1][c - 1]:
            curr_run += 1
            if curr_run >= max_run:
                if self.board[r][c] == Team.TEAM1:
                    return GameOutcome.TEAM1_WINS
                elif self.board[r][c] == Team.TEAM2:
                    return GameOutcome.TEAM2_WINS
            r -= 1
            c -= 1
        r = prev_move_row
        c = prev_move_column
        while 0 <= r + 1 < self.rows and 0 <= c + 1 < self.columns and self.board[r][c] == self.board[r + 1][c + 1]:
            curr_run += 1
            if curr_run >= max_run:
                if self.board[r][c] == Team.TEAM1:
                    return GameOutcome.TEAM1_WINS
                elif self.board[r][c] == Team.TEAM2:
                    return GameOutcome.TEAM2_WINS
            r += 1
            c += 1

        # Upwards Diagonal
        curr_run = 1
        r = prev_move_row
        c = prev_move_column
        while 0 <= r + 1 < self.rows and 0 <= c - 1 < self.columns and self.board[r][c] == self.board[r + 1][c - 1]:
            curr_run += 1
            if curr_run >= max_run:
                if self.board[r][c] == Team.TEAM1:
                    return GameOutcome.TEAM1_WINS
                elif self.board[r][c] == Team.TEAM2:
                    return GameOutcome.TEAM2_WINS
            r += 1
            c -= 1
        r = prev_move_row
        c = prev_move_column
        while 0 <= r - 1 < self.rows and 0 <= c + 1 < self.columns and self.board[r][c] == self.board[r - 1][c + 1]:
            curr_run += 1
            if curr_run >= max_run:
                if self.board[r][c] == Team.TEAM1:
                    return GameOutcome.TEAM1_WINS
                elif self.board[r][c] == Team.TEAM2:
                    return GameOutcome.TEAM2_WINS
            r -= 1
            c += 1

        if self.piece_count >= self.rows * self.columns:
            return GameOutcome.DRAW
        return GameOutcome.INCONCLUSIVE

    def make_move(self, move):
        row, column = move
        if (0 <= row < self.rows and 0 <= column < self.columns and self.board[row][column] is None and
                self.game_outcome == GameOutcome.INCONCLUSIVE):
            self.piece_count += 1
            self.board[row][column] = self.turn_team
            self.game_outcome = self.__update_game_outcome__(self.max_run, (row, column))
            self.previous_moves.append((row, column))
            self.turn_team = self.turn_team.get_enemy()

    def undo_move(self):
        if self.previous_moves:
            row, column = self.previous_moves.pop()
            team = self.board[row][column]
            if 0 <= row < self.rows and 0 <= column < self.columns and team in Team:
                self.piece_count -= 1
                self.board[row][column] = None
                self.turn_team = team
                self.game_outcome = GameOutcome.INCONCLUSIVE

    def get_possible_moves(self):
        return [(r, c) for r in range(self.rows) for c in range(self.columns) if self.board[r][c] is None]

    def find_winning_run(self):

        for r in range(self.rows):
            for c in range(self.columns):

                # Horizontal
                current_run = []
                if self.board[r][c] is not None:
                    for k in range(self.max_run):
                        r2 = r
                        c2 = c + k
                        if 0 <= r2 < self.rows and 0 <= c2 < self.columns and self.board[r2][c2] == self.board[r][c]:
                            current_run.append((r2, c2))
                        else:
                            break
                if len(current_run) == self.max_run:
                    return current_run

                # Vertical
                current_run = []
                if self.board[r][c] is not None:
                    for k in range(self.max_run):
                        r2 = r + k
                        c2 = c
                        if 0 <= r2 < self.rows and 0 <= c2 < self.columns and self.board[r2][c2] == self.board[r][c]:
                            current_run.append((r2, c2))
                        else:
                            break
                if len(current_run) == self.max_run:
                    return current_run

                # Diagonal Down
                current_run = []
                if self.board[r][c] is not None:
                    for k in range(self.max_run):
                        r2 = r + k
                        c2 = c + k
                        if 0 <= r2 < self.rows and 0 <= c2 < self.columns and self.board[r2][c2] == self.board[r][c]:
                            current_run.append((r2, c2))
                        else:
                            break
                if len(current_run) == self.max_run:
                    return current_run

                # Diagonal Down
                current_run = []
                if self.board[r][c] is not None:
                    for k in range(self.max_run):
                        r2 = r + k
                        c2 = c - k
                        if 0 <= r2 < self.rows and 0 <= c2 < self.columns and self.board[r2][c2] == self.board[r][c]:
                            current_run.append((r2, c2))
                        else:
                            break
                if len(current_run) == self.max_run:
                    return current_run