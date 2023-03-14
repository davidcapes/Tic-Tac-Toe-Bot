import pygame
import sys

from Bot import *
from Game import *

# Define Static Parameters
ROWS = 3
COLUMNS = 3
MAX_RUN = 3

IMAGE_SIZE = 101
VS_COMPUTER = True
COMPUTER_TEAM = random.choice(list(Team))
WINDOW_DIMENSIONS = (COLUMNS*IMAGE_SIZE, ROWS*IMAGE_SIZE)

# Initialize Game
pygame.init()
screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
pygame.display.set_caption("Tic Tac Toe")
pygame.display.set_icon(pygame.image.load('../skins/Icon.png'))

# Load Images
IMAGE_DICT = {team: pygame.image.load('../skins/' + str(team) + '.png') for team in Team}
IMAGE_DICT[None] = pygame.image.load('../skins/Blank.png')
HIGHLIGHTED_IMAGE = pygame.image.load('../skins/Highlighted.png')

# Game Initialization
game = Game(ROWS, COLUMNS, MAX_RUN)
winning_run = []

# main loop
while True:
    for event in pygame.event.get():

        # Exit Game
        if event.type == pygame.QUIT:
            sys.exit()

        # Computer make move
        if VS_COMPUTER and game.turn_team == COMPUTER_TEAM:
            best_move = get_best_move(game)
            if best_move is not None:
                game.make_move(best_move)

        # Make Moves
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected_row = event.pos[1] // IMAGE_SIZE
            selected_column = event.pos[0] // IMAGE_SIZE
            game.make_move((selected_row, selected_column))

        # Undo Moves
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            game.undo_move()
            while VS_COMPUTER and game.turn_team == COMPUTER_TEAM:
                game.undo_move()
            winning_run.clear()

        # Restart
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game = Game(ROWS, COLUMNS, MAX_RUN)
            COMPUTER_TEAM = random.choice(list(Team))
            winning_run.clear()

    # Display Everything
    for row in range(ROWS):
        for column in range(COLUMNS):
            image = IMAGE_DICT[game.board[row][column]]
            screen.blit(image, (column * IMAGE_SIZE, row * IMAGE_SIZE))
    if game.game_outcome != GameOutcome.INCONCLUSIVE and game.game_outcome != GameOutcome.DRAW:
        if not winning_run:
            winning_run = game.find_winning_run()
        for row, column in winning_run:
            screen.blit(HIGHLIGHTED_IMAGE, (column * IMAGE_SIZE, row * IMAGE_SIZE))
    pygame.display.update()