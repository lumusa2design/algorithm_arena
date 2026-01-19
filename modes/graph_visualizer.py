import pygame
from ui import Button

GRAY = (180, 180, 180)
YELLOW = (255, 220, 120)
GREEN = (90, 255, 140)
BLUE = (120, 160, 255)

def run_graph_visualization(screen, algorithm, graph, positions, start):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)
    small = pygame.font.SysFont("consolas", 14)

    gen = algorithm(graph, start)

    visited = set()
    seen = set()
    visit_order = []
    seen_order = []

    dist = {}
    container = []
    active_edge = None
    algo = ""

    explanation = "Pulsa Paso -> para avanzar"

    zoom = 1.0
    offset = [0, 0]
    dragging = False
    last_mouse = (0, 0)

    btn_next = Button((440, 540, 160, 40), "Paso ->")
    btn_back = Button((20, 20, 120, 40), "Volver")

    def transform(p):
        return int(p[0] * zoom + offset[0]), int(p[1] * zoom + offset[1])

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
                if event.button in (2, 3):
                    dragging = True
                    last_mouse = event.pos

                if btn_back.clicked(event.pos):
                    return

                if btn_next.clicked(event.pos):
                    try:
                        data = next(gen)
                        algo = data.get("algo", algo)

                        visited = data.get("visited", visited)
                        seen = data.get("seen", seen)
                        dist = data.get("dist", dist)

                        if "queue" in data:
                            container = data["queue"]
                            explanation = "Cola (BFS)"

                        elif "stack" in data:
                            container = data["stack"]
                            explanation = "Pila (DFS)"

                        elif "pq" in data:
                            container = data["pq"]
                            explanation = "Cola de prioridad (Dijkstra)"

                        if data["action"] == "visit":
                            n = data["node"]
                            if n not in visit_order:
                                visit_order.append(n)
                            explanation = f"{algo}: visitando nodo {n}"
                            active_edge = None

                        if data["action"] == "edge":
                            u, v = data["edge"]
                            if v not in seen_order:
                                seen_order.append(v)
                            explanation = f"{algo}: explorando {u} → {v}"
                            active_edge = (u, v)

                        if data["action"] == "relax":
                            u, v, w = data["edge"]
                            if v not in seen_order:
                                seen_order.append(v)
                            explanation = f"Dijkstra: relajando {u} → {v} (peso {w})"
                            active_edge = (u, v)

                    except StopIteration:
                        explanation = f"{algo} terminado"

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in (2, 3):
                    dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - last_mouse[0]
                dy = event.pos[1] - last_mouse[1]
                offset[0] += dx
                offset[1] += dy
                last_mouse = event.pos

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    zoom = min(2.5, zoom + 0.1)
                else:
                    zoom = max(0.3, zoom - 0.1)

        for u, edges in graph.items():
            for v, w in edges:
                pygame.draw.line(
                    screen,
                    (100, 100, 100),
                    transform(positions[u]),
                    transform(positions[v]),
                    2
                )

                mx = (positions[u][0] + positions[v][0]) // 2
                my = (positions[u][1] + positions[v][1]) // 2
                screen.blit(
                    small.render(str(w), True, (220, 220, 220)),
                    transform((mx, my))
                )

        if active_edge:
            pygame.draw.line(
                screen,
                BLUE,
                transform(positions[active_edge[0]]),
                transform(positions[active_edge[1]]),
                4
            )

        for n, pos in positions.items():
            if n in visited:
                color = GREEN
            elif n in seen:
                color = YELLOW
            else:
                color = GRAY

            x, y = transform(pos)
            pygame.draw.circle(screen, color, (x, y), int(22 * zoom))
            pygame.draw.circle(screen, (40, 40, 40), (x, y), int(22 * zoom), 2)

            lbl = font.render(str(n), True, (0, 0, 0))
            screen.blit(lbl, lbl.get_rect(center=(x, y)))

            if algo == "Dijkstra" and n in dist:
                d = dist[n]
                txt = "∞" if d == float("inf") else str(d)
                screen.blit(
                    small.render(txt, True, (255, 255, 255)),
                    (x - 10, y + int(26 * zoom))
                )

        pygame.draw.rect(screen, (25, 25, 25), (600, 0, 200, 600))
        pygame.draw.line(screen, (80, 80, 80), (600, 0), (600, 600), 2)

        y = 20
        screen.blit(font.render("Estructura", True, (255, 255, 255)), (610, y))
        y += 30
        for item in container:
            screen.blit(small.render(str(item), True, (220, 220, 220)), (620, y))
            y += 16

        y += 10
        screen.blit(font.render("Vistos", True, (255, 255, 255)), (610, y))
        y += 25
        for n in seen_order:
            screen.blit(small.render(str(n), True, YELLOW), (620, y))
            y += 14

        y += 10
        screen.blit(font.render("Visitados", True, (255, 255, 255)), (610, y))
        y += 25
        for n in visit_order:
            screen.blit(small.render(str(n), True, GREEN), (620, y))
            y += 14

        pygame.draw.rect(screen, (25, 25, 25), (0, 480, 800, 120))
        pygame.draw.line(screen, (80, 80, 80), (0, 480), (800, 480), 2)
        screen.blit(small.render(explanation, True, (220, 220, 220)), (20, 500))

        btn_next.draw(screen, font, mouse)
        btn_back.draw(screen, font, mouse)

        pygame.display.flip()
