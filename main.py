import pygame
from ui import Button
from modes.sorting_mode import run_sorting_mode
from modes.graph_mode import run_graph_mode
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Algorithm Arena")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 24)

STATE_MAIN = "MAIN"
STATE_SORTING = "SORTING"

state = STATE_MAIN

btn_sorting = Button((300, 220, 200, 50), "Ordenación")
btn_graphs = Button((300, 300, 200, 50), "Recorrido de Grafos")
btn_exit = Button((300, 380, 200, 50), "Salir")

running = True
while running:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    screen.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == STATE_MAIN:
                if btn_sorting.clicked(event.pos):
                    run_sorting_mode(screen)
                if btn_graphs.clicked(event.pos):
                    run_graph_mode(screen)
                if btn_exit.clicked(event.pos):
                    running = False

    title = font.render("Algorithm Arena", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(400, 140)))

    btn_sorting.draw(screen, font, mouse)
    btn_graphs.draw(screen, font, mouse)
    btn_exit.draw(screen, font, mouse)

    pygame.display.flip()

pygame.quit()
