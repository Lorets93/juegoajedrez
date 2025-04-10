import pygame
import sys
import os

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT = (237, 237, 237)
DARK = (59, 59, 59)
TURQUOISE = (61, 213, 168)
TURQUOISE_DARK = (41, 173, 138)

# Pantalla
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
BOARD_SIZE = 480
SQUARE_SIZE = BOARD_SIZE // 8

initial_positions = {
    "rook": [(0, 0), (7, 0), (0, 7), (7, 7)],
    "knight": [(1, 0), (6, 0), (1, 7), (6, 7)],
    "bishop": [(2, 0), (5, 0), (2, 7), (5, 7)],
    "queen": [(3, 0), (3, 7)],
    "king": [(4, 0), (4, 7)],
    "pawn": [(i, 1) for i in range(8)] + [(i, 6) for i in range(8)],
}

class PantallaInicio:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game")

        self.font_large = pygame.font.SysFont("Arial", 60, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 28, bold=True)

        self.piece_images = {}
        self.load_piece_images()

        self.start_pressed = False
        self.settings_pressed = False

        self.running = True

    def load_piece_images(self):
        pieces = ["rook", "knight", "bishop", "queen", "king", "pawn"]
        colors = ["w", "b"]
        for color in colors:
            for piece in pieces:
                name = f"{piece}_{color}"
                path = os.path.join("images", f"{name}.png")
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                self.piece_images[name] = image

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = LIGHT if (row + col) % 2 == 0 else DARK
                rect = pygame.Rect(col * SQUARE_SIZE + 400, row * SQUARE_SIZE + 60, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def draw_pieces(self):
        for piece, positions in initial_positions.items():
            for col, row in positions:
                color = "b" if row < 2 else "w"
                name = f"{piece}_{color}"
                image = self.piece_images[name]
                x = col * SQUARE_SIZE + 400
                y = row * SQUARE_SIZE + 60
                self.screen.blit(image, (x, y))

    def draw_button(self, rect, text, is_pressed):
        color = TURQUOISE_DARK if is_pressed else TURQUOISE
        offset = 2 if is_pressed else 0
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        text_surface = self.font_button.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery + offset))
        self.screen.blit(text_surface, text_rect)

    def draw_sidebar(self):
        pygame.draw.rect(self.screen, BLACK, (0, 0, 400, SCREEN_HEIGHT))

        lines = ["LET'S", "PLAY", "CHESS"]
        for i, line in enumerate(lines):
            text = self.font_large.render(line, True, WHITE)
            self.screen.blit(text, (50, 60 + i * 80))

        # Botones
        self.start_button_rect = pygame.Rect(100, 350, 200, 50)
        self.settings_button_rect = pygame.Rect(100, 420, 200, 50)

        self.draw_button(self.start_button_rect, "START", self.start_pressed)
        self.draw_button(self.settings_button_rect, "SETTINGS", self.settings_pressed)

    def run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.draw_sidebar()
            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()
            self.handle_events()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    self.start_pressed = True
                elif self.settings_button_rect.collidepoint(event.pos):
                    self.settings_pressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.start_pressed and self.start_button_rect.collidepoint(event.pos):
                    print("Game Started!")
                elif self.settings_pressed and self.settings_button_rect.collidepoint(event.pos):
                    print("Settings Clicked!")

                # Resetear estados visuales
                self.start_pressed = False
                self.settings_pressed = False


if __name__ == "__main__":
    juego = PantallaInicio()
    juego.run()