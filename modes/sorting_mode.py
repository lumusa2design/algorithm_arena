import pygame
from ui import Button
from sorting.bubble_sort import bubble_sort
from sorting.comb_sort import comb_sort
from modes.sorting_visualizer import run_sorting_visualization

def run_sorting_mode(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)

    ALGORITHMS = ["Bubble Sort", "Comb Sort", "Quick Sort"]
    selected_left = 0
    selected_right = 1
    mode = "SINGLE"

    btn_single = Button((100, 180, 200, 40), "Algoritmo único")
    btn_compare = Button((100, 240, 200, 40), "Comparar algoritmos")

    btn_left = Button((400, 180, 200, 40), ALGORITHMS[selected_left])
    btn_right = Button((400, 240, 200, 40), ALGORITHMS[selected_right])

    btn_start = Button((300, 360, 200, 50), "Iniciar")
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
                if btn_single.clicked(event.pos):
                    mode = "SINGLE"
                if btn_compare.clicked(event.pos):
                    mode = "COMPARE"

                if btn_left.clicked(event.pos):
                    selected_left = (selected_left + 1) % len(ALGORITHMS)
                    btn_left.text = ALGORITHMS[selected_left]

                if btn_right.clicked(event.pos):
                    selected_right = (selected_right + 1) % len(ALGORITHMS)
                    btn_right.text = ALGORITHMS[selected_right]

                if btn_back.clicked(event.pos):
                    return

                if btn_start.clicked(event.pos):
                    if mode == "SINGLE":
                        run_sorting_visualization(
                            screen,
                            mode="SINGLE",
                            left_algo=ALGORITHMS[selected_left]
                        )
                    else:
                        run_sorting_visualization(
                            screen,
                            mode="COMPARE",
                            left_algo=ALGORITHMS[selected_left],
                            right_algo=ALGORITHMS[selected_right]
                        )


        screen.blit(font.render("Modo de ordenación", True, (255,255,255)), (280, 120))

        btn_single.draw(screen, font, mouse)
        btn_compare.draw(screen, font, mouse)

        btn_left.draw(screen, font, mouse)
        if mode == "COMPARE":
            btn_right.draw(screen, font, mouse)

        btn_start.draw(screen, font, mouse)
        btn_back.draw(screen, font, mouse)

        pygame.display.flip()
