import pygame
import random
from sorting import bubble_sort
from visualizer import draw_bars

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

speed = 60
paused = False

arr = [random.randint(10, 100) for _ in range(50)]
generator = bubble_sort.bubble_sort(arr)

running = True
highlight = None

while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                speed = min(240, speed + 10)
            if event.key == pygame.K_DOWN:
                speed = max(10, speed - 10)
            if event.key == pygame.K_SPACE:
                paused = not paused

    if not paused:
        try:
            action, i, j = next(generator)
            if action == "compare":
                highlight = {"indices": (i, j), "color": (255, 80, 80)}
            elif action == "swap":
                highlight = {"indices": (i, j), "color": (80, 255, 80)}
        except StopIteration:
            highlight = None

    draw_bars(screen, arr, highlight)
    pygame.display.flip()

pygame.quit()
