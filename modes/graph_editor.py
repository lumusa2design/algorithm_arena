import pygame
import math
from ui import Button
from modes.graph_visualizer import run_graph_visualization
from graphs.bfs import bfs
from graphs.dfs import dfs

NODE_RADIUS = 20

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def run_graph_editor(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    graph = {}
    positions = {}
    next_id = 0

    selected_node = None
    start_node = None

    algorithms = [("BFS", bfs), ("DFS", dfs)]
    algo_index = 0

    btn_algo = Button((620, 20, 160, 40), algorithms[algo_index][0])
    btn_run = Button((620, 70, 160, 40), "Ejecutar")
    btn_back = Button((620, 120, 160, 40), "Volver")

    explanation = (
        "Click izquierdo: crear nodo\n"
        "Click derecho: conectar nodos\n"
        "Tecla S: nodo inicial"
    )

    running = True
    while running:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and selected_node is not None:
                    start_node = selected_node

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.clicked(event.pos):
                    return

                if btn_algo.clicked(event.pos):
                    algo_index = (algo_index + 1) % len(algorithms)
                    btn_algo.text = algorithms[algo_index][0]

                if btn_run.clicked(event.pos):
                    if start_node is not None:
                        run_graph_visualization(
                            screen,
                            algorithms[algo_index][1],
                            graph,
                            positions,
                            start_node
                        )


                if event.button == 1:
                    for node, pos in positions.items():
                        if distance(pos, event.pos) <= NODE_RADIUS:
                            selected_node = node
                            break
                    else:
                        graph[next_id] = []
                        positions[next_id] = event.pos
                        selected_node = next_id
                        next_id += 1

                if event.button == 3:
                    for node, pos in positions.items():
                        if distance(pos, event.pos) <= NODE_RADIUS:
                            if selected_node is not None and node != selected_node:
                                graph[selected_node].append(node)
                                graph[node].append(selected_node)
                            break

        for node, neighbors in graph.items():
            for n in neighbors:
                pygame.draw.line(
                    screen,
                    (100, 100, 100),
                    positions[node],
                    positions[n],
                    2
                )

        for node, (x, y) in positions.items():
            if node == start_node:
                color = (255, 200, 100)
            elif node == selected_node:
                color = (90, 255, 140)
            else:
                color = (180, 180, 180)

            pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
            pygame.draw.circle(screen, (40, 40, 40), (x, y), NODE_RADIUS, 2)
            label = font.render(str(node), True, (0, 0, 0))
            screen.blit(label, label.get_rect(center=(x, y)))

        pygame.draw.rect(screen, (25, 25, 25), (600, 0, 200, 600))
        pygame.draw.line(screen, (80, 80, 80), (600, 0), (600, 600), 2)

        y = 200
        for line in explanation.split("\n"):
            screen.blit(font.render(line, True, (220, 220, 220)), (610, y))
            y += 22

        btn_algo.draw(screen, font, mouse)
        btn_run.draw(screen, font, mouse)
        btn_back.draw(screen, font, mouse)

        pygame.display.flip()
