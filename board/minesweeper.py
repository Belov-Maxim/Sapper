from .base import Board
import random
from cell import MineCell, VoidCell
import colors
import config
import pygame


class Minesweeper(Board):
    def __init__(self,
                 screen: pygame.Surface,
                 width: int,
                 height: int,
                 left_shift: int = 0,
                 top_shift: int = 0,
                 mines_count: int = 5) -> None:
        self.mines_count = mines_count
        self.mines = []
        self.available_marks = mines_count

        super(Minesweeper, self).__init__(screen, width, height, left_shift, top_shift)

    def init_board(self) -> None:
        mine_positions = []
        while len(mine_positions) < self.mines_count:
            x, y = random.randint(0, self.width), random.randint(0, self.height)
            if (x, y) not in mine_positions:
                mine_positions.append((x, y))
            else:
                continue

        for y in range(self.height):
            line = []
            for x in range(self.width):
                if (x, y) in mine_positions:
                    cell = MineCell(
                        self.screen,
                        self,
                        self.left_shift + x * config.CELL_SIZE,
                        self.top_shift + y * config.CELL_SIZE,
                        config.CELL_SIZE,
                        config.CELL_SIZE,
                        colors.WHITE  # DEBUG ONLY; color.WHITE by default
                    )
                    self.mines.append(cell)
                else:
                    cell = VoidCell(
                        self.screen,
                        self,
                        self.left_shift + x * config.CELL_SIZE,
                        self.top_shift + y * config.CELL_SIZE,
                        config.CELL_SIZE,
                        config.CELL_SIZE,
                        colors.WHITE
                    )
                line.append(cell)
            self.board.append(line)

    def mines_counter(self, mine_count):
        for row in self.board:
            for cell in row:
                if isinstance(cell, MineCell):
                    mine_count += 1

    def on_marked(self, x: int, y: int) -> None:
        cell = self.board[y][x]
        cell.on_marked()
