import pygame
from ui import Button
from modes.graph_editor import run_graph_editor

def run_graph_mode(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    btn_start = Button((300, 280, 200, 50), "Editor de grafos")
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
                if btn_start.clicked(event.pos):
                    run_graph_editor(screen)

                if btn_back.clicked(event.pos):
                    return

        title = font.render("Recorrido de grafos", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(400, 200)))

        btn_start.draw(screen, font, mouse)
        btn_back.draw(screen, font, mouse)

        pygame.display.flip()
