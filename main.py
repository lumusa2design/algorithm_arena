import time
import pygame
from ui import Button
from modes.sorting_mode import run_sorting_mode
from modes.graph_mode import run_graph_mode
from modes.math_root_finding_mode import run_math_root_finding_mode

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Algorithm Arena")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 24)

STATE_MAIN = "MAIN"
state = STATE_MAIN

# ---- Layout ----
BTN_W = 220
BTN_X = 400 - BTN_W // 2
BTN_Y = [240, 310, 380, 450]

btn_sorting = Button((BTN_X, BTN_Y[0], BTN_W, 50), "Ordenación")
btn_graphs = Button((BTN_X, BTN_Y[1], BTN_W, 50), "Recorrido de Grafos")
btn_math_root_finding = Button((BTN_X, BTN_Y[2], BTN_W, 50), "Búsqueda de Raíces")
btn_exit = Button((BTN_X, BTN_Y[3], BTN_W, 50), "Salir")

# ---- Animación ----
anim_start = time.time()
ANIM_DURATION = 0.4

def ease_out(t):
    return 1 - (1 - t) * (1 - t)

running = True
while running:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    screen.fill((20, 20, 20))

    elapsed = time.time() - anim_start
    t = min(1.0, elapsed / ANIM_DURATION)
    e = ease_out(t)
    offset_y = int((1 - e) * 80)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == STATE_MAIN:
                if btn_sorting.clicked(event.pos):
                    run_sorting_mode(screen)
                    anim_start = time.time()
                if btn_graphs.clicked(event.pos):
                    run_graph_mode(screen)
                    anim_start = time.time()
                if btn_math_root_finding.clicked(event.pos):
                    run_math_root_finding_mode(screen)
                    anim_start = time.time()
                if btn_exit.clicked(event.pos):
                    running = False

    title = font.render("Algorithm Arena", True, (255, 255, 255))
    title.set_alpha(int(e * 255))
    screen.blit(title, title.get_rect(center=(400, 120)))

    for btn, y in zip(
        [btn_sorting, btn_graphs, btn_math_root_finding, btn_exit],
        BTN_Y
    ):
        btn.rect.y = y + offset_y
        btn.draw(screen, font, mouse)

    pygame.display.flip()

pygame.quit()
