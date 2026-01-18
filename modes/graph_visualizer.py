import pygame
from ui import Button

def run_graph_visualization(screen, algorithm, graph, positions, start_node):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)
    small = pygame.font.SysFont("consolas", 16)

    visited = set()
    active_edge = None

    gen = algorithm(graph, start_node)

    btn_next = Button((440, 540, 160, 40), "Paso ->")
    btn_back = Button((20, 20, 120, 40), "Volver")

    explanation = "Pulsa Paso -> para comenzar"

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
                        action = next(gen)

                        if action[0] == "visit":
                            visited.add(action[1])
                            active_edge = None
                            explanation = f"Visitando nodo {action[1]}"

                        else:
                            active_edge = (action[1], action[2])
                            explanation = f"Explorando arista {action[1]} → {action[2]}"

                    except StopIteration:
                        explanation = "Recorrido terminado"

        for node, neighbors in graph.items():
            for n in neighbors:
                pygame.draw.line(
                    screen,
                    (100, 100, 100),
                    positions[node],
                    positions[n],
                    2
                )

        if active_edge:
            pygame.draw.line(
                screen,
                (255, 200, 100),
                positions[active_edge[0]],
                positions[active_edge[1]],
                4
            )

        for node, (x, y) in positions.items():
            if node in visited:
                color = (90, 255, 140)
            else:
                color = (180, 180, 180)

            pygame.draw.circle(screen, color, (x, y), 22)
            pygame.draw.circle(screen, (40, 40, 40), (x, y), 22, 2)
            label = font.render(str(node), True, (0, 0, 0))
            screen.blit(label, label.get_rect(center=(x, y)))

        pygame.draw.rect(screen, (25, 25, 25), (0, 480, 800, 120))
        pygame.draw.line(screen, (80, 80, 80), (0, 480), (800, 480), 2)

        screen.blit(small.render(explanation, True, (220, 220, 220)), (20, 500))

        btn_next.draw(screen, font, mouse)
        btn_back.draw(screen, font, mouse)

        pygame.display.flip()
