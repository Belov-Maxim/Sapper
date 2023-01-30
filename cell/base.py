import pygame
from typing import Tuple, List
import config


class Cell:
    def __init__(self, surface: pygame.Surface, board, x: int, y: int, width: int, height: int,
                 color: Tuple[int, int, int]):
        # Position
        self.x = x
        self.y = y
        self.board_x = self.x // config.CELL_SIZE
        self.board_y = self.y // config.CELL_SIZE

        # Properties
        self.width = width
        self.height = height
        self.color = color

        # Graphics
        self.surface = surface
        self.rect = None

        # Other
        self.is_clicked = False
        self.is_marked = False
        self.board = board

    def render(self, *render_args, **render_kwargs) -> pygame.Rect:
        self.rect = pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height), *render_args,
                                     **render_kwargs)

        if self.is_marked and not self.is_clicked:
            mark = pygame.image.load('textures/mark.png')
            mark.set_colorkey((255, 255, 255))
            dog_rect = mark.get_rect(topleft=(self.rect.center[0] - 11, self.rect.center[1] - 11))
            self.surface.blit(mark, dog_rect)

        return self.rect

    def look_around(self) -> List['Cell']:
        cells_to_check = []

        if self.board_x != self.board.width - 1:
            cells_to_check.append(self.board.board[self.board_y][self.board_x + 1])

            if self.board_y != self.board.height - 1:
                cells_to_check.append(self.board.board[self.board_y + 1][self.board_x + 1])

        if self.board_y != self.board.height - 1:
            cells_to_check.append(self.board.board[self.board_y + 1][self.board_x])

            if self.board_x != 0:
                cells_to_check.append(self.board.board[self.board_y + 1][self.board_x - 1])

        if self.board_x != 0:
            cells_to_check.append(self.board.board[self.board_y][self.board_x - 1])

            if self.board_y != 0:
                cells_to_check.append(self.board.board[self.board_y - 1][self.board_x - 1])

        if self.board_y != 0:
            cells_to_check.append(self.board.board[self.board_y - 1][self.board_x])

            if self.board_x != self.board.width - 1:
                cells_to_check.append(self.board.board[self.board_y - 1][self.board_x + 1])

        return cells_to_check

    def on_clicked(self) -> None:
        print(f'Cell: Cell ({self.__class__.__name__}) [{self.x};{self.y}] was clicked')

    def on_marked(self) -> None:
        if self.is_clicked:
            return

        if self.is_marked:
            self.board.available_marks += 1
            self.is_marked = False
        else:
            if self.board.available_marks == 0:
                return

            self.board.available_marks -= 1
            self.is_marked = True
