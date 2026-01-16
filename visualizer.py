import pygame

WIDTH, HEIGHT = 800, 600
PANEL = (30, 30, 30)
TEXT = (220, 220, 220)

def draw_panel(screen, x, title, font):
    pygame.draw.rect(screen, PANEL, (x, 0, 400, HEIGHT))
    pygame.draw.line(screen, (80, 80, 80), (x, 0), (x, HEIGHT), 2)
    screen.blit(font.render(title, True, TEXT), (x + 130, 10))

def draw_bars(screen, arr, x_offset, width, highlight=None):
    bar_width = width // len(arr)
    max_val = max(arr)

    for i, val in enumerate(arr):
        color = (180, 180, 180)
        if highlight and i in highlight["indices"]:
            color = highlight["color"]
        BAR_AREA_HEIGHT = 320      # altura máxima de barras
        BOTTOM_MARGIN = 200        # espacio para texto + botones

        height = int((val / max_val) * BAR_AREA_HEIGHT)
        y = HEIGHT - height - BOTTOM_MARGIN

        pygame.draw.rect(
            screen,
            color,
            (
                x_offset + i * bar_width,
                HEIGHT - height - 120,
                bar_width - 2,
                height
            )
        )
