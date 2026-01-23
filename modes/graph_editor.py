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
    small = pygame.font.SysFont("consolas", 14)

    graph = {}
    positions = {}
    next_id = 0

    selected = None
    start_node = None
    target_node = None

    dragging_node = False
    drag_offset = (0, 0)

    input_weight = False
    weight_buffer = ""
    pending_edge = None

    zoom = 1.0
    offset = [0, 0]
    dragging_view = False
    last_mouse = (0, 0)

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
        "Click izq: crear/seleccionar\n"
        "Arrastrar: mover nodo\n"
        "Click der: conectar\n"
        "Rueda: zoom | Botón medio: mover vista\n"
        "S: inicio | D: destino | Supr: borrar"
    )

    def world_from_screen(p):
        return ((p[0] - offset[0]) / zoom, (p[1] - offset[1]) / zoom)

    def screen_from_world(p):
        return (int(p[0] * zoom + offset[0]), int(p[1] * zoom + offset[1]))

    def delete_node(n):
        nonlocal start_node, target_node, selected
        graph.pop(n, None)
        positions.pop(n, None)
        for u in graph:
            graph[u] = [(v, w) for v, w in graph[u] if v != n]
        if start_node == n:
            start_node = None
        if target_node == n:
            target_node = None
        if selected == n:
            selected = None

    running = True
    while running:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEWHEEL:
                zoom = min(2.5, max(0.3, zoom + event.y * 0.1))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    dragging_view = True
                    last_mouse = event.pos

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
                    wp = world_from_screen(event.pos)
                    for n, pos in positions.items():
                        if dist(pos, wp) <= NODE_RADIUS:
                            selected = n
                            dragging_node = True
                            drag_offset = (pos[0] - wp[0], pos[1] - wp[1])
                            break
                    else:
                        positions[next_id] = wp
                        graph[next_id] = []
                        selected = next_id
                        next_id += 1

                if event.button == 3 and not input_weight:
                    wp = world_from_screen(event.pos)
                    for n, pos in positions.items():
                        if dist(pos, wp) <= NODE_RADIUS:
                            if selected is not None and n != selected:
                                input_weight = True
                                weight_buffer = ""
                                pending_edge = (selected, n)
                            break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_node = False
                if event.button == 2:
                    dragging_view = False

            if event.type == pygame.MOUSEMOTION:
                if dragging_view:
                    dx = event.pos[0] - last_mouse[0]
                    dy = event.pos[1] - last_mouse[1]
                    offset[0] += dx
                    offset[1] += dy
                    last_mouse = event.pos

                if dragging_node and selected is not None:
                    wp = world_from_screen(event.pos)
                    positions[selected] = (wp[0] + drag_offset[0], wp[1] + drag_offset[1])

            if event.type == pygame.KEYDOWN:
                if input_weight:
                    if event.key == pygame.K_RETURN:
                        w = int(weight_buffer) if weight_buffer.isdigit() else 1
                        u, v = pending_edge
                        graph.setdefault(u, []).append((v, w))
                        graph.setdefault(v, []).append((u, w))
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
                    if event.key in (pygame.K_DELETE, pygame.K_BACKSPACE) and selected is not None:
                        delete_node(selected)

        for u, edges in graph.items():
            for v, w in edges:
                pygame.draw.line(
                    screen,
                    (100, 100, 100),
                    screen_from_world(positions[u]),
                    screen_from_world(positions[v]),
                    2
                )
                mx = (positions[u][0] + positions[v][0]) / 2
                my = (positions[u][1] + positions[v][1]) / 2
                screen.blit(
                    small.render(str(w), True, (220, 220, 220)),
                    screen_from_world((mx, my))
                )

        for n, pos in positions.items():
            if n == start_node:
                color = (255, 200, 100)
            elif n == target_node:
                color = (255, 100, 100)
            elif n == selected:
                color = (90, 255, 140)
            else:
                color = (180, 180, 180)

            x, y = screen_from_world(pos)
            pygame.draw.circle(screen, color, (x, y), int(NODE_RADIUS * zoom))
            pygame.draw.circle(screen, (40, 40, 40), (x, y), int(NODE_RADIUS * zoom), 2)
            lbl = font.render(str(n), True, (0, 0, 0))
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
            screen.blit(
                font.render(f"Peso: {weight_buffer}", True, (255, 255, 255)),
                (200, 290)
            )

        btn_algo.draw(screen, font, mouse)
        btn_run.draw(screen, font, mouse)
        btn_back.draw(screen, font, mouse)

        pygame.display.flip()
