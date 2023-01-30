import config
from .base import Cell
from .mine import MineCell
import pygame
from typing import Tuple
import colors


class VoidCell(Cell):
    def __init__(self, surface: pygame.Surface, board, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]):
        super(VoidCell, self).__init__(surface, board, x, y, width, height, color)
        self.font = pygame.font.SysFont('Arial', config.CELL_SIZE // 2)

        self.text_colors = {
            0: colors.BLACK,
            1: colors.BLUE,
            2: colors.GREEN,
            3: colors.RED,
            4: colors.RED,
            5: colors.RED,
            6: colors.RED,
            7: colors.RED,
            8: colors.RED,
            9: colors.RED,
        }

    def count_mines(self):
        return len([cell for cell in self.look_around() if isinstance(cell, MineCell)])

    def render(self, *render_args, **render_kwargs) -> pygame.Rect:
        rect = super(VoidCell, self).render(*render_args, **render_kwargs)
        mines_count = self.count_mines()

        if self.is_clicked:
            self.surface.blit(
                self.font.render(
                    str(mines_count),
                    True,
                    self.text_colors[mines_count]
                ),
                (self.x + config.CELL_SIZE // 2 - config.CELL_SIZE // 4, self.y)
            )
        return rect

    def on_clicked(self) -> None:
        if self.is_clicked:
            return

        self.is_clicked = True
        self.is_marked = False  # Не показывать флажок если уже нажали

        self.color = colors.LIGHT_GREY

        if self.count_mines() == 0:
            for cell in self.look_around():
                if isinstance(cell, VoidCell):
                    cell.on_clicked()
