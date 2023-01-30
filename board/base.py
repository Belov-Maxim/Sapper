import pygame
import config
from cell import Cell
from typing import Union, Tuple, List


class Board:
    def __init__(self,
                 screen: pygame.Surface,
                 width: int,
                 height: int,
                 left_shift: int = 0,
                 top_shift: int = 0,
                 board_size:int = 2) -> None:
        self.screen = screen
        self.width = width
        self.height = height
        self.left_shift = left_shift
        self.top_shift = top_shift
        self.board: List[List[Cell]] = []
        self.board_size = board_size
        self.init_board()

    @property
    def full_width(self) -> int:
        return self.width * config.CELL_SIZE

    @property
    def full_height(self) -> int:
        return self.height * config.CELL_SIZE

    def init_board(self) -> None:
        raise NotImplementedError

    def set_zero_position(self, left: int, top: int) -> None:
        self.left_shift = left
        self.top_shift = top

    def click_cell_position(self, x: int, y: int) -> Union[Tuple[int, int], None]:
        x -= self.left_shift
        y -= self.top_shift

        if (x < 0 or y < 0) or (x > self.full_width or y > self.full_height):
            return

        return x // config.CELL_SIZE, y // config.CELL_SIZE

    def render(self) -> None:
        for line in self.board:
            for cell in line:
                cell.render(self.board_size)

    def on_clicked(self, x: int, y: int) -> None:
        cell = self.board[y][x]
        cell.on_clicked()
