import pygame

from board import Board


class Sudoku():

    def __init__(self):

        self.board = Board(10, 10, 9)
        self.run = True

    def play(self):

        pygame.init()
        win = pygame.display.set_mode(
            (self.board.width + 20, self.board.width + 20))
        clock = pygame.time.Clock()
        pygame.display.set_caption("SUDOKU SOLVER")

        while self.run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

                    if self.board.sel_pos and not self.board.solving:
                        if event.key == pygame.K_KP0 or event.key == pygame.K_0:
                            self.board.set_value_sel_block(0)
                        if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                            self.board.set_value_sel_block(1)
                        if event.key == pygame.K_KP2 or event.key == pygame.K_2:
                            self.board.set_value_sel_block(2)
                        if event.key == pygame.K_KP3 or event.key == pygame.K_3:
                            self.board.set_value_sel_block(3)
                        if event.key == pygame.K_KP4 or event.key == pygame.K_4:
                            self.board.set_value_sel_block(4)
                        if event.key == pygame.K_KP5 or event.key == pygame.K_5:
                            self.board.set_value_sel_block(5)
                        if event.key == pygame.K_KP6 or event.key == pygame.K_6:
                            self.board.set_value_sel_block(6)
                        if event.key == pygame.K_KP7 or event.key == pygame.K_7:
                            self.board.set_value_sel_block(7)
                        if event.key == pygame.K_KP8 or event.key == pygame.K_8:
                            self.board.set_value_sel_block(8)
                        if event.key == pygame.K_KP9 or event.key == pygame.K_9:
                            self.board.set_value_sel_block(9)

                    if event.key == pygame.K_s:
                        self.board.solving = not self.board.solving
                        if self.board.solving:
                            self.board.setup_solve()

                    if event.key == pygame.K_a:
                        self.board.clear_solved()

                    if event.key == pygame.K_c:
                        self.board.clear_all()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not self.board.solving:
                        self.board.set_selected_position(pos)

            if self.board.solving:
                self.board.solve()

            win.fill((255, 255, 255))
            self.board.draw(win)
            pygame.display.update()
