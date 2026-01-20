import pygame
import math
from ui import Button
from graphs.bfs import bfs
from graphs.dfs import dfs
from graphs.dijkstra import dijkstra
from modes.graph_visualizer import run_graph_visualization

NODE_RADIUS = 20

def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def run_graph_editor(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)
    small = pygame.font.SysFont("consolas", 15)

    graph = {}
    positions = {}
    next_id = 0

    selected = None
    start_node = None
    target_node = None

    input_weight = False
    weight_buffer = ""
    pending_edge = None

    algorithms = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("Dijkstra", dijkstra)
    ]
    algo_index = 0

    btn_algo = Button((620, 20, 160, 40), algorithms[algo_index][0])
    btn_run = Button((620, 70, 160, 40), "Ejecutar")
    btn_back = Button((620, 120, 160, 40), "Volver")

    explanation = (
        "Click izq: crear/seleccionar nodo\n"
        "Click der: conectar nodos\n"
        "S: nodo inicio\n"
        "D: nodo destino"
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
                if input_weight:
                    if event.key == pygame.K_RETURN:
                        weight = int(weight_buffer) if weight_buffer.isdigit() else 1
                        u, v = pending_edge
                        graph.setdefault(u, []).append((v, weight))
                        graph.setdefault(v, []).append((u, weight))
                        input_weight = False
                        pending_edge = None
                        weight_buffer = ""
                    elif event.key == pygame.K_BACKSPACE:
                        weight_buffer = weight_buffer[:-1]
                    elif event.unicode.isdigit():
                        weight_buffer += event.unicode
                else:
                    if event.key == pygame.K_s and selected is not None:
                        start_node = selected
                    if event.key == pygame.K_d and selected is not None:
                        target_node = selected

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
                            start_node,
                            target_node
                        )

                if event.button == 1:
                    for node, pos in positions.items():
                        if dist(pos, event.pos) <= NODE_RADIUS:
                            selected = node
                            break
                    else:
                        positions[next_id] = event.pos
                        graph[next_id] = []
                        selected = next_id
                        next_id += 1

                if event.button == 3 and not input_weight:
                    for node, pos in positions.items():
                        if dist(pos, event.pos) <= NODE_RADIUS:
                            if selected is not None and node != selected:
                                input_weight = True
                                weight_buffer = ""
                                pending_edge = (selected, node)
                            break

        for u, edges in graph.items():
            for v, w in edges:
                pygame.draw.line(
                    screen,
                    (100, 100, 100),
                    positions[u],
                    positions[v],
                    2
                )
                mx = (positions[u][0] + positions[v][0]) // 2
                my = (positions[u][1] + positions[v][1]) // 2
                screen.blit(
                    small.render(str(w), True, (220, 220, 220)),
                    (mx, my)
                )

        for node, (x, y) in positions.items():
            if node == start_node:
                color = (255, 200, 100)
            elif node == target_node:
                color = (255, 100, 100)
            elif node == selected:
                color = (90, 255, 140)
            else:
                color = (180, 180, 180)

            pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
            pygame.draw.circle(screen, (40, 40, 40), (x, y), NODE_RADIUS, 2)
            lbl = font.render(str(node), True, (0, 0, 0))
            screen.blit(lbl, lbl.get_rect(center=(x, y)))

        pygame.draw.rect(screen, (25, 25, 25), (600, 0, 200, 600))
        pygame.draw.line(screen, (80, 80, 80), (600, 0), (600, 600), 2)

        y = 200
        for line in explanation.split("\n"):
            screen.blit(font.render(line, True, (220, 220, 220)), (610, y))
            y += 22

        if input_weight:
            pygame.draw.rect(screen, (25, 25, 25), (180, 260, 440, 80))
            pygame.draw.rect(screen, (90, 90, 90), (180, 260, 440, 80), 2)
            txt = font.render(f"Peso: {weight_buffer}", True, (255, 255, 255))
            screen.blit(txt, (200, 290))

        btn_algo.draw(screen, font, mouse)
        btn_run.draw(screen, font, mouse)
        btn_back.draw(screen, font, mouse)

        pygame.display.flip()
