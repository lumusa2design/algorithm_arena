import pygame

WIDTH, HEIGHT = 800, 600

def draw_panel(screen, x, title, font):
    pygame.draw.rect(screen, (30, 30, 30), (x, 0, 400, HEIGHT))
    pygame.draw.line(screen, (80, 80, 80), (x, 0), (x, HEIGHT), 2)
    screen.blit(font.render(title, True, (255, 255, 255)), (x + 140, 10))


def draw_bars(screen, arr, x_offset, width, highlight=None):
    bar_width = width // len(arr)
    max_val = max(arr)

    for i, val in enumerate(arr):
        color = (180, 180, 180)
        if highlight and i in highlight["indices"]:
            color = highlight["color"]

        height = int((val / max_val) * (HEIGHT - 160))
        pygame.draw.rect(
            screen,
            color,
            (
                x_offset + i * bar_width,
                HEIGHT - height - 80,
                bar_width - 2,
                height
            )
        )
