import random
import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 0
        self.top = 0
        self.cell_size = 20

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):
        x, y = mouse_pos
        x -= self.left
        y -= self.top
        x //= self.cell_size
        y //= self.cell_size
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        return x, y

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (0, 0, 0), (
                self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, (255, 255, 255), (
                self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size), 1)

    def on_click(self, cell):
        x, y = cell
        print("Cell clicked:", x, y)


class Minesweeper(Board):
    def __init__(self, width, height, n):
        super().__init__(width, height)
        self.board = [[-1] * width for _ in range(height)]
        i = 0
        while i < n:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == -1:
                self.board[y][x] = 10
                i += 1
    def open_cell2(self, cell):
        x, y = cell
        if self.board[y][x] == 10:
            return
        s = 0
        for dy in range(-1, 2):
            if s == 0:
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                            continue
                        if self.board[y + dy][x + dx] == -1:
                            self.open_cell((x + dx, y + dy))

    def open_cell(self, cell):
        x, y = cell
        if self.board[y][x] == 10:
            return
        s = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                    continue
                if self.board[y + dy][x + dx] == 10:
                    s += 1
            self.board[y][x] = s

            if s == 0:
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                            continue
                        if self.board[y + dy][x + dx] == -1:
                            self.open_cell((x + dx, y + dy))

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 10:
                    pygame.draw.rect(screen, pygame.Color("red"), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                        self.cell_size))
                if self.board[y][x] >= 0 and self.board[y][x] != 10:
                    font = pygame.font.Font(None, self.cell_size - 6)
                    text = font.render(str(self.board[y][x]), 1, (100, 255, 100))
                    screen.blit(text, (x * self.cell_size + self.left + 3, y * self.cell_size + self.top + 3
                                       ))
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def on_click(self, cell):
        self.open_cell2(cell)


def main():
    pygame.init()
    size = 400, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption("SAPER")
    board = Minesweeper(10, 15, 10)
    board.set_view(20, 20, 30)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = board.get_click(event.pos)
                if coords is not None:
                    board.on_click(coords)

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()


if __name__ == '__main__':
    main()
