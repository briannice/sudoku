import pygame
import math
from .block import Block
from .line import Line

pygame.init()


class Board:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        # Number of blocks in a row
        self.size = size
        self.root = int(math.sqrt(size))
        # Tuple of the currently selected position
        self.sel_pos = None

        # Constants for lines and blocks
        if self.size > 25:
            BW = 15
        elif size > 16:
            BW = 25
        else:
            BW = 40
        LWB = 3
        LWS = 1
        self.width = size * BW + (self.root + 1) * \
            LWB + self.root * (self.root - 1) * LWS

        self.lines = set()

        # Thick lines
        for i in range(self.root + 1):
            p = i * (self.root * BW + (self.root - 1) * LWS + LWB)
            # Horizontal
            self.lines.add(Line(0, p, self.width, LWB, x, y))
            # Vertical
            self.lines.add(Line(p, 0, LWB, self.width, x, y))

        # Thin lines
        for i in range(self.root * (self.root - 1)):
            p1 = (i // (self.root - 1)) * \
                (self.root * BW + (self.root - 1) * LWS + LWB)
            p2 = LWB + BW + (i % (self.root - 1)) * (BW + LWS)
            # Horizontal
            self.lines.add(Line(0, p1 + p2, self.width, LWS, x, y))
            # Vertical
            self.lines.add(Line(p1 + p2, 0, LWS, self.width, x, y))

        # Blocks
        self.blocks = []
        for row in range(size):
            t1 = (row // self.root) * (self.root *
                                       BW + (self.root - 1) * LWS + LWB)
            t2 = LWB + (row % self.root) * (BW + LWS)
            lst = []
            for col in range(size):
                p1 = (col // self.root) * (self.root *
                                           BW + (self.root - 1) * LWS + LWB)
                p2 = LWB + (col % self.root) * (BW + LWS)
                lst.append(Block(row, col, p1 + p2, t1 + t2, BW, x, y))
            self.blocks.append(lst)

        # Values for solving the board
        self.cur_val = 1
        self.solving = False
        self.cur_block = None
        self.solved_positions = []

    def draw(self, win):
        for line in self.lines:
            line.draw(win)
        for row in self.blocks:
            for block in row:
                block.draw(win)

    def get_width(self):
        return self.width

    def is_over(self, pos):
        if self.x <= pos[0] and pos[0] <= self.x + self.width:
            if self.y <= pos[1] and pos[1] <= self.y + self.width:
                return True
        return False

    def set_selected_position(self, pos):
        if self.is_over(pos):
            if self.sel_pos:
                self.blocks[self.sel_pos[0]][self.sel_pos[1]].selected = False
            for row in range(self.size):
                for col in range(self.size):
                    if self.blocks[row][col].is_over(pos):
                        self.sel_pos = (row, col)
                        self.blocks[row][col].selected = True
                        break
        else:
            self.sel_pos = None

    def set_value_sel_block(self, val):
        if self.check_valid_position(self.sel_pos, val):
            self.blocks[self.sel_pos[0]][self.sel_pos[1]].set_value(val)
        else:
            print(f"Unvalid value: {val}")

    def get_empty_block(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.blocks[row][col].value == 0:
                    return self.blocks[row][col]
        return None

    def get_previous_block(self):
        block = self.solved_positions[-1]
        self.solved_positions.pop(-1)
        return block

    def check_valid_position(self, pos, val):
        if val == 0:
            return True
        row, col = pos
        # row
        for i in range(self.size):
            if self.blocks[row][i].value == val and i != col:
                return False

        # col
        for j in range(self.size):
            if self.blocks[j][col].value == val and j != row:
                return False
        # block
        brow = row // self.root
        bcol = col // self.root
        for k in range(self.root):
            for l in range(self.root):
                if self.blocks[self.root * brow + k][self.root * bcol + l].value == val:
                    if brow * self.root + k != row and bcol * self.root + l != col:
                        return False

        return True

    def solve(self):
        if self.cur_block is None:
            if self.get_empty_block() is not None:
                self.cur_block = self.get_empty_block()
            else:
                self.solving = False
        else:
            if self.cur_val <= self.size:
                self.cur_block.value = self.cur_val
                if self.check_valid_position(self.cur_block.get_pos(), self.cur_val):
                    self.cur_val = 1
                    self.solved_positions.append(self.cur_block)
                    self.cur_block = self.get_empty_block()
                else:
                    self.cur_val += 1
            else:
                self.cur_block.value = 0
                self.cur_block = self.get_previous_block()
                self.cur_val = self.cur_block.value + 1

    def setup_solve(self):
        if self.sel_pos:
            self.blocks[self.sel_pos[0]][self.sel_pos[1]].selected = False
            self.sel_pos = None

    def clear_solved(self):
        for block in self.solved_positions:
            block.value = 0
        if self.cur_block:
            self.cur_block.value = 0
        self.solved_positions = []
        self.cur_block = None
        self.cur_val = 1

    def clear_all(self):
        self.clear_solved()
        for row in range(self.size):
            for col in range(self.size):
                self.blocks[row][col].value = 0
