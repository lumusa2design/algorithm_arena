import pygame
import random

from sorting.bubble_sort import bubble_sort
from sorting.comb_sort import comb_sort
from visualizer import draw_bars, draw_panel
from ui import Button

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Algorithm Arena – Educativo")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 20)
small = pygame.font.SysFont("consolas", 16)

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Comb Sort": comb_sort
}

EXPLANATIONS = {
    "Bubble Sort": {
        "compare": "Bubble compara elementos adyacentes para empujar el mayor al final",
        "swap": "Intercambio porque el elemento izquierdo es mayor"
    },
    "Comb Sort": {
        "compare": "Comb compara con un gap para eliminar elementos pequeños mal posicionados",
        "swap": "Intercambio usando gap para reducir desorden rápidamente"
    }
}

mode = "SELECT"
left_algo = "Bubble Sort"
right_algo = "Comb Sort"

btn_start = Button((300, 500, 200, 50), "Iniciar comparación")
btn_left = Button((100, 220, 200, 40), left_algo)
btn_right = Button((500, 220, 200, 40), right_algo)

btn_prev = Button((200, 540, 160, 40), "<- Paso")
btn_next = Button((440, 540, 160, 40), "Paso ->")

def setup():
    global arr1, arr2, gen1, gen2, state1, state2, history, step, explanation
    base = [random.randint(10, 100) for _ in range(40)]
    arr1 = base.copy()
    arr2 = base.copy()
    gen1 = ALGORITHMS[left_algo](arr1)
    gen2 = ALGORITHMS[right_algo](arr2)
    state1 = {"highlight": None}
    state2 = {"highlight": None}
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
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == "SELECT":
                if btn_left.clicked(event.pos):
                    left_algo = list(ALGORITHMS)[(list(ALGORITHMS).index(left_algo) + 1) % len(ALGORITHMS)]
                    btn_left.text = left_algo
                if btn_right.clicked(event.pos):
                    right_algo = list(ALGORITHMS)[(list(ALGORITHMS).index(right_algo) + 1) % len(ALGORITHMS)]
                    btn_right.text = right_algo
                if btn_start.clicked(event.pos):
                    setup()
                    mode = "COMPARE"
            else:
                if btn_next.clicked(event.pos):
                    try:
                        a1 = next(gen1)
                        a2 = next(gen2)

                        state1["highlight"] = {
                            "indices": (a1[1], a1[2]),
                            "color": (255, 90, 90) if a1[0] == "compare" else (90, 255, 140)
                        }
                        state2["highlight"] = {
                            "indices": (a2[1], a2[2]),
                            "color": (255, 90, 90) if a2[0] == "compare" else (90, 255, 140)
                        }

                        explanation = (
                            f"{left_algo}: {EXPLANATIONS[left_algo][a1[0]]}\n"
                            f"{right_algo}: {EXPLANATIONS[right_algo][a2[0]]}"
                        )

                        history.append((arr1.copy(), arr2.copy(), state1.copy(), state2.copy()))
                        step += 1

                    except StopIteration:
                        explanation = "Alguno de los algoritmos ha terminado"

                if btn_prev.clicked(event.pos) and step > 0:
                    step -= 1
                    arr1[:], arr2[:], state1, state2 = history[step]

    if mode == "SELECT":
        screen.blit(font.render("Selecciona algoritmos", True, (255, 255, 255)), (290, 140))
        btn_left.draw(screen, font, mouse)
        btn_right.draw(screen, font, mouse)
        btn_start.draw(screen, font, mouse)
    else:
        draw_panel(screen, 0, left_algo, font)
        draw_panel(screen, 400, right_algo, font)

        draw_bars(screen, arr1, 0, 400, state1["highlight"])
        draw_bars(screen, arr2, 400, 400, state2["highlight"])

        pygame.draw.rect(screen, (25, 25, 25), (0, 380, 800, 120))
        pygame.draw.line(screen, (80, 80, 80), (0, 380), (800, 380), 2)

        y = 390
        for line in explanation.split("\n"):
            screen.blit(small.render(line, True, (220, 220, 220)), (20, y))
            y += 22

        pygame.draw.rect(screen, (30, 30, 30), (0, 520, 800, 80))
        pygame.draw.line(screen, (90, 90, 90), (0, 520), (800, 520), 2)

        btn_prev.draw(screen, font, mouse)
        btn_next.draw(screen, font, mouse)

    pygame.display.flip()

pygame.quit()
