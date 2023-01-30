import pygame
from exceptions.generics import GameOver
import colors
import config
from board import Minesweeper


clock = pygame.time.Clock()

start_ticks = pygame.time.get_ticks()
seconds = (pygame.time.get_ticks() - start_ticks) / 1000


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        if (config.SCREEN_SIZE[0] % config.CELL_SIZE) != 0 or (config.SCREEN_SIZE[1] % config.CELL_SIZE) != 0:
            raise ValueError('Размер экрана должен быть кратен размеру клетки')

        self.board_width = config.SCREEN_SIZE[0] // config.CELL_SIZE
        self.board_height = config.SCREEN_SIZE[1] // config.CELL_SIZE
        self.board = Minesweeper(self.screen, self.board_width, self.board_height,
                                 mines_count=self.board_width + self.board_height)
        self.is_running = True

    def _check_victory(self):
        return all([mine.is_marked for mine in self.board.mines])

    def run(self) -> None:
        game_over_timer = 0
        pygame.display.set_caption("SAPER")

        while self.is_running:
            try:
                seconds2 = (pygame.time.get_ticks() - start_ticks) // 1000
                pygame.display.set_caption(f"SAPER                Флаги:{self.board.available_marks}                   "
                                           f"                               Время:" + str(seconds2))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        coords = self.board.click_cell_position(*event.pos)
                        if coords:
                            if event.button == 1:  # LMB
                                self.board.on_clicked(*coords)
                            if event.button == 3:  # RMB
                                self.board.on_marked(*coords)

                if self._check_victory():
                    raise GameOver('Вы победили')

                self.screen.fill(colors.GREY)
                self.board.render()
                pygame.display.flip()
                self.clock.tick(100)
                self.board.mines_counter(self.board.mines_count)

            except GameOver as error:
                f1 = pygame.font.Font(None, 56)
                text1 = f1.render(f'{error.message}', True, (180, 0, 0))
                self.screen.blit(text1, (275, 300))
                print(f"Game ended with message: {error.message}")
                pygame.display.update()
                self.is_running = False
        ab = True
        while ab:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ab = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ab = False
    pygame.quit()
