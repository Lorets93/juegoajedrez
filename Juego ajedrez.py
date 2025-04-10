import pygame
import os


# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT = (240, 240, 240)
DARK = (50, 50, 50)
TURQUOISE = (61, 213, 168)
GRAY = (100, 100, 100)

# Pantalla
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BOARD_SIZE = 480
SQUARE_SIZE = BOARD_SIZE // 8

class StartJuego:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game - Start")
        self.clock = pygame.time.Clock()

        self.font_medium = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_big = pygame.font.SysFont("Arial", 32, bold=True)

        self.piece_images = {}
        self.load_piece_images()

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
                color = WHITE if (row + col) % 2 == 0 else BLACK
                rect = pygame.Rect(col * SQUARE_SIZE + 60, row * SQUARE_SIZE + 60, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def draw_pieces(self):
        initial_positions = {
            "rook": [(0, 0), (7, 0), (0, 7), (7, 7)],
            "knight": [(1, 0), (6, 0), (1, 7), (6, 7)],
            "bishop": [(2, 0), (5, 0), (2, 7), (5, 7)],
            "queen": [(3, 0), (3, 7)],
            "king": [(4, 0), (4, 7)],
            "pawn": [(i, 1) for i in range(8)] + [(i, 6) for i in range(8)]
        }

        for piece, positions in initial_positions.items():
            for col, row in positions:
                color = "b" if row < 2 else "w"
                name = f"{piece}_{color}"
                image = self.piece_images[name]
                x = col * SQUARE_SIZE + 60
                y = row * SQUARE_SIZE + 60
                self.screen.blit(image, (x, y))

    def draw_ui(self):
        # Info jugadores
        pygame.draw.circle(self.screen, LIGHT, (60 + BOARD_SIZE // 2, 30), 20)
        pygame.draw.circle(self.screen, LIGHT, (60 + BOARD_SIZE // 2, 570), 20)
        player1 = self.font_medium.render("PLAYER 1", True, WHITE)
        player2 = self.font_medium.render("PLAYER 2", True, WHITE)
        self.screen.blit(player1, (60 + BOARD_SIZE // 2 - 60, 570))
        self.screen.blit(player2, (60 + BOARD_SIZE // 2 - 60, 10))

        # Tiempos
        pygame.draw.rect(self.screen, DARK, (60 + BOARD_SIZE + 80, 100, 200, 50), border_radius=5)
        pygame.draw.rect(self.screen, DARK, (60 + BOARD_SIZE + 80, 200, 200, 50), border_radius=5)

        time_icon = self.font_medium.render("\u23F1", True, WHITE)
        time_text = self.font_medium.render("10 min", True, WHITE)
        self.screen.blit(time_icon, (60 + BOARD_SIZE + 90, 110))
        self.screen.blit(time_text, (60 + BOARD_SIZE + 130, 110))

        game_mode_text = self.font_medium.render("CLASSIC", True, WHITE)
        self.screen.blit(game_mode_text, (60 + BOARD_SIZE + 130, 210))

        # Etiquetas
        movement_label = self.font_medium.render("MOVEMENT TIME", True, WHITE)
        game_mode_label = self.font_medium.render("GAME MODE", True, WHITE)
        self.screen.blit(movement_label, (60 + BOARD_SIZE + 80, 70))
        self.screen.blit(game_mode_label, (60 + BOARD_SIZE + 80, 170))

        # Botón PLAY
        play_button = pygame.Rect(60 + BOARD_SIZE + 110, 300, 120, 50)
        pygame.draw.rect(self.screen, TURQUOISE, play_button, border_radius=6)
        play_text = self.font_big.render("PLAY", True, BLACK)
        self.screen.blit(play_text, (60 + BOARD_SIZE + 135, 310))

    def run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.draw_board()
            self.draw_pieces()
            self.draw_ui()

            pygame.display.flip()
            self.handle_events()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
if __name__ == "__main__":
    juego = StartJuego()
    juego.run()