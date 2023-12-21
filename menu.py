import pygame
import sys

class Menu:
    def __init__(self, screen, width, height):
        self.status = True
        self.screen = screen
        self.width = width
        self.height = height
        self.SKYBLUE = (135, 206, 235)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.HOVER_COLOR = (100, 100, 100)
        self.font = pygame.font.Font(None, 36)
        self.button_x = self.width // 2 - 150
        self.play_button = pygame.Rect(self.button_x, 200, 300, 50)
        self.quit_button = pygame.Rect(self.button_x, 300, 300, 50)
        self.font = pygame.font.Font(None, 36)
        self.button_x = self.width // 2 - 150
        self.play_button = pygame.Rect(self.button_x, 200, 300, 50)
        self.quit_button = pygame.Rect(self.button_x, 300, 300, 50)
    def draw_button(self, x, y, width, height, text, hover=False):
        button_color = self.HOVER_COLOR if hover else self.BLACK
        pygame.draw.rect(self.screen, button_color, (x, y, width, height))
        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        self.screen.blit(text_surface, text_rect)
    def draw_text(self, text, x, y, font_size=24):
        color = self.BLACK
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.collidepoint(*pygame.mouse.get_pos()):
                    self.status = False
                elif self.quit_button.collidepoint(*pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
    def show(self):
        self.status = True
        while self.status:
            self.screen.fill(self.SKYBLUE)
            self.handle_events()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.draw_button(self.button_x, 200, 300, 50, 'Play', self.play_button.collidepoint(mouse_x, mouse_y))
            self.draw_button(self.button_x, 300, 300, 50, 'Quit', self.quit_button.collidepoint(mouse_x, mouse_y))
            self.draw_text("ZQSD to move, SPACE to jump, CLICK-LEFT to draw (semi-working), C to pause", self.width // 2, 420)

            pygame.display.update()