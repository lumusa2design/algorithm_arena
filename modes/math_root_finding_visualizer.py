import pygame

WIDTH, HEIGHT = 900, 600
MARGIN_X = 80

def run_math_root_finding_visualizer(screen, algo, f, x_range):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)
    small = pygame.font.SysFont("consolas", 14)

    gen = algo.run()
    state = None
    finished = False

    def map_x(x):
        a, b = x_range
        return int(MARGIN_X + (x - a) / (b - a) * (WIDTH - 2 * MARGIN_X))

    def map_y(y):
        return int(HEIGHT // 2 - y * 40)

    xs = [x_range[0] + i * (x_range[1] - x_range[0]) / 400 for i in range(401)]
    ys = [f(x) for x in xs]

    running = True
    while running:
        clock.tick(60)
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not finished:
                    try:
                        state = next(gen)
                        if "done" in state:
                            finished = True
                    except StopIteration:
                        finished = True
                if event.key == pygame.K_r:
                    gen = algo.run()
                    state = None
                    finished = False
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.draw.line(
            screen, (120, 120, 120),
            (MARGIN_X, HEIGHT // 2),
            (WIDTH - MARGIN_X, HEIGHT // 2), 1
        )

        points = [(map_x(x), map_y(y)) for x, y in zip(xs, ys)]
        pygame.draw.lines(screen, (80, 180, 255), False, points, 2)

        if state and "a" in state:
            a, b, m = state["a"], state["b"], state["m"]

            pygame.draw.line(screen, (255, 80, 80), (map_x(a), 0), (map_x(a), HEIGHT), 2)
            pygame.draw.line(screen, (255, 80, 80), (map_x(b), 0), (map_x(b), HEIGHT), 2)
            pygame.draw.line(screen, (80, 255, 120), (map_x(m), 0), (map_x(m), HEIGHT), 2)

            info = [
                f"Iteración: {state['iter']}",
                f"a = {a:.5f}   f(a) = {state['fa']:.5f}",
                f"m = {m:.5f}   f(m) = {state['fm']:.5f}",
                f"b = {b:.5f}   f(b) = {state['fb']:.5f}",
            ]

            y = 20
            for line in info:
                screen.blit(font.render(line, True, (220, 220, 220)), (20, y))
                y += 22

        footer = "SPACE: paso | R: reiniciar | ESC: volver"
        screen.blit(small.render(footer, True, (160, 160, 160)), (20, HEIGHT - 40))

        pygame.display.flip()
