import pygame
import sys

from game import Sudoku


if __name__ == "__main__":
    SUDOKU = Sudoku()
    SUDOKU.play()
    pygame.quit()
    quit()
    sys.exit()
