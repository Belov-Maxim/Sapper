from .base import Cell
from exceptions.generics import GameOver


class MineCell(Cell):
    def on_clicked(self) -> None:
        raise GameOver('Вы проиграли')
