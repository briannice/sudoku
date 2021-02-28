import pygame

pygame.init()

class Block:
    def __init__(self, row, col, x, y, width, dx, dy):
        self.row = row
        self.col = col
        self.x = x + dx
        self.y = y + dy
        self.width = width
        self.value = 0
        if width == 40:
            self.fontsize = 30
        elif width == 25:
            self.fontsize = 18
        else:
            self.fontsize = 12
        self.rect = (self.x, self.y, width, width)
        self.sel_color = (255, 102, 102)
        self.color = (163, 163, 194)
        self.txtcolor = (0,0,0)
        self.selected = False

    def set_color(self, newcolor):
        self.color = newcolor

    def set_value(self, newvalue):
        self.value = newvalue

    def is_over(self, pos):
        if self.x <= pos[0] and pos[0] <= self.x + self.width:
            if self.y <= pos[1] and pos[1] <= self.y + self.width:
                return True
        return False

    def get_pos(self):
        return self.row, self.col

    def draw(self, win):
        if self.selected:
            pygame.draw.rect(win, self.sel_color, self.rect)
        else:
            pygame.draw.rect(win, self.color, self.rect)
        
        if self.value != 0:
            fnt = pygame.font.SysFont("arial", self.fontsize)
            txt = fnt.render(str(self.value), True, self.txtcolor)
            rect = txt.get_rect(center=(self.x + self.width // 2, self.y + self.width // 2))
            win.blit(txt, rect)