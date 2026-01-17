import pygame
from ui import Button
from graphs.bfs import bfs
from graphs.dfs import dfs
from modes.graph_visualizer import run_graph_visualization

def run_graph_mode(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    algorithms = [("BFS", bfs), ("DFS", dfs)]
    selected = 0

    btn_algo = Button((300, 240, 200, 40), algorithms[selected][0])
    btn_start = Button((300, 320, 200, 50), "Iniciar")
    btn_back = Button((20, 20, 120, 40), "Volver")

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
                if btn_algo.clicked(event.pos):
                    selected = (selected + 1) % len(algorithms)
                    btn_algo.text = algorithms[selected][0]

                if btn_start.clicked(event.pos):
                    run_graph_visualization(screen, algorithms[selected][1])

                if btn_back.clicked(event.pos):
                    return

        screen.blit(font.render("Recorrido de grafos", True, (255, 255, 255)), (280, 160))
        btn_algo.draw(screen, font, mouse)
        btn_start.draw(screen, font, mouse)
        btn_back.draw(screen, font, mouse)

        pygame.display.flip()
