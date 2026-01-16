import pygame

BG_DARK = (20, 20, 20)
PANEL = (30, 30, 30)
BORDER = (90, 90, 90)
BTN = (70, 70, 70)
BTN_HOVER = (100, 100, 100)

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, screen, font, mouse):
        color = BTN_HOVER if self.rect.collidepoint(mouse) else BTN
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BORDER, self.rect, 2, border_radius=8)
        label = font.render(self.text, True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
