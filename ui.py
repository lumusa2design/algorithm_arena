import pygame

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, screen, font, mouse_pos):
        color = (90, 90, 90) if self.rect.collidepoint(mouse_pos) else (60, 60, 60)
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2, border_radius=6)

        label = font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
