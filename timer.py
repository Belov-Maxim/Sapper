import pygame
clock = pygame.time.Clock()

start_ticks = pygame.time.get_ticks()
seconds = (pygame.time.get_ticks()-start_ticks) / 1000
while True:
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    print(seconds)

