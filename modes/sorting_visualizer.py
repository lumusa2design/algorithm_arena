import pygame
import random

from sorting.bubble_sort import bubble_sort
from sorting.comb_sort import comb_sort
from sorting.quick_sort import quick_sort
from visualizer import draw_bars, draw_panel
from ui import Button

ALGO_MAP = {
    "Bubble Sort": bubble_sort,
    "Comb Sort": comb_sort,
    "Quick Sort": quick_sort
}

def run_sorting_visualization(screen, mode, left_algo, right_algo=None):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)
    small = pygame.font.SysFont("consolas", 16)

    base = [random.randint(10, 100) for _ in range(40)]
    arr1 = base.copy()
    gen1 = ALGO_MAP[left_algo](arr1)
    state1 = {"highlight": None}

    if mode == "COMPARE":
        arr2 = base.copy()
        gen2 = ALGO_MAP[right_algo](arr2)
        state2 = {"highlight": None}

    btn_prev = Button((200, 540, 160, 40), "<- Paso")
    btn_next = Button((440, 540, 160, 40), "Paso ->")
    btn_back = Button((20, 20, 120, 40), "Volver")

    history = []
    step = -1
    explanation = "Pulsa Paso -> para avanzar"

    running = True
    while running:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.clicked(event.pos):
                    return

                if btn_next.clicked(event.pos):
                    try:
                        a1 = next(gen1)
                        state1["highlight"] = {
                            "indices": (a1[1], a1[2]),
                            "color": (255, 90, 90) if a1[0] == "compare" else (90, 255, 140)
                        }

                        if mode == "COMPARE":
                            a2 = next(gen2)
                            state2["highlight"] = {
                                "indices": (a2[1], a2[2]),
                                "color": (255, 90, 90) if a2[0] == "compare" else (90, 255, 140)
                            }

                        history.append((
                            arr1.copy(),
                            arr2.copy() if mode == "COMPARE" else None,
                            state1.copy(),
                            state2.copy() if mode == "COMPARE" else None
                        ))
                        step += 1

                    except StopIteration:
                        explanation = "Algoritmo terminado"

                if btn_prev.clicked(event.pos) and step > 0:
                    step -= 1
                    h = history[step]
                    arr1[:] = h[0]
                    state1 = h[2]
                    if mode == "COMPARE":
                        arr2[:] = h[1]
                        state2 = h[3]

        draw_panel(screen, 0, left_algo, font)
        draw_bars(screen, arr1, 0, 400, state1["highlight"])

        if mode == "COMPARE":
            draw_panel(screen, 400, right_algo, font)
            draw_bars(screen, arr2, 400, 400, state2["highlight"])

        pygame.draw.rect(screen, (25, 25, 25), (0, 380, 800, 120))
        pygame.draw.line(screen, (80, 80, 80), (0, 380), (800, 380), 2)

        screen.blit(small.render(explanation, True, (220, 220, 220)), (20, 390))

        pygame.draw.rect(screen, (30, 30, 30), (0, 520, 800, 80))
        pygame.draw.line(screen, (90, 90, 90), (0, 520), (800, 520), 2)

        btn_prev.draw(screen, font, mouse)
        btn_next.draw(screen, font, mouse)
        btn_back.draw(screen, font, mouse)

        pygame.display.flip()
