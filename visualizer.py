import pygame

WIDTH, HEIGHT = 800, 600
BAR_COLOR = (200, 200, 200)
COMPARE_COLOR = (255, 80, 80)
SWAP_COLOR = (80, 255, 80)

def draw_bars(screen, arr, highlight=None):
    screen.fill((20, 20, 20))
    bar_width = WIDTH // len(arr)
    max_val = max(arr)

    for i, val in enumerate(arr):
        color = BAR_COLOR
        if highlight and i in highlight:
            color = highlight["color"]

        height = int((val / max_val) * (HEIGHT - 50))
        pygame.draw.rect(
            screen,
            color,
            (i * bar_width, HEIGHT - height, bar_width - 2, height)
        )
