import pygame
import random

from sorting.bubble_sort import bubble_sort
from sorting.comb_sort import comb_sort
from visualizer import draw_bars, draw_panel
from ui import Button

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Algorithm Arena")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 26)

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Comb Sort": comb_sort
}

mode = "SELECT"
left_algo = "Bubble Sort"
right_algo = "Comb Sort"

btn_start = Button((300, 500, 200, 50), "Iniciar comparación")
btn_left = Button((100, 200, 200, 40), left_algo)
btn_right = Button((500, 200, 200, 40), right_algo)

btn_prev = Button((10, 550, 120, 40), "◀ Paso")
btn_next = Button((140, 550, 120, 40), "Paso ▶")

def setup_compare():
    global arr1, arr2, gen1, gen2, state1, state2, history, step
    base = [random.randint(10, 100) for _ in range(40)]
    arr1 = base.copy()
    arr2 = base.copy()
    gen1 = ALGORITHMS[left_algo](arr1)
    gen2 = ALGORITHMS[right_algo](arr2)
    state1 = {"highlight": None, "steps": 0}
    state2 = {"highlight": None, "steps": 0}
    history = []
    step = -1

running = True
while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    screen.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == "SELECT":
                if btn_left.clicked(event.pos):
                    left_algo = list(ALGORITHMS)[(list(ALGORITHMS).index(left_algo)+1)%len(ALGORITHMS)]
                    btn_left.text = left_algo
                if btn_right.clicked(event.pos):
                    right_algo = list(ALGORITHMS)[(list(ALGORITHMS).index(right_algo)+1)%len(ALGORITHMS)]
                    btn_right.text = right_algo
                if btn_start.clicked(event.pos):
                    setup_compare()
                    mode = "COMPARE"

            elif mode == "COMPARE":
                if btn_next.clicked(event.pos):
                    try:
                        a1 = next(gen1)
                        a2 = next(gen2)
                        state1["steps"] += 1
                        state2["steps"] += 1
                        state1["highlight"] = {"indices": (a1[1], a1[2]), "color": (255,80,80) if a1[0]=="compare" else (80,255,80)}
                        state2["highlight"] = {"indices": (a2[1], a2[2]), "color": (255,80,80) if a2[0]=="compare" else (80,255,80)}
                        history.append((arr1.copy(), arr2.copy(), state1.copy(), state2.copy()))
                        step += 1
                    except StopIteration:
                        pass

                if btn_prev.clicked(event.pos) and step > 0:
                    step -= 1
                    arr1[:], arr2[:], state1, state2 = history[step]

    if mode == "SELECT":
        screen.blit(font.render("Selecciona algoritmos", True, (255,255,255)), (280, 100))
        btn_left.draw(screen, font, mouse_pos)
        btn_right.draw(screen, font, mouse_pos)
        btn_start.draw(screen, font, mouse_pos)

    else:
        draw_panel(screen, 0, left_algo, font)
        draw_panel(screen, 400, right_algo, font)
        draw_bars(screen, arr1, 0, 400, state1["highlight"])
        draw_bars(screen, arr2, 400, 400, state2["highlight"])
        btn_prev.draw(screen, font, mouse_pos)
        btn_next.draw(screen, font, mouse_pos)

    pygame.display.flip()

pygame.quit()
