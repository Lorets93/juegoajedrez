import pygame, os, sys

# Colores definidos como tupla RGB
BLACK = (48, 46, 43)
WHITE = (255, 255, 255)
LIGHT = (237, 237, 237)
DARK = (137, 169, 103)
TURQUOISE = (61, 213, 168)
TURQUOISE_DARK = (41, 173, 138)

# Tamaño de la ventana y de cada casilla del tablero
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SQUARE_SIZE = 60  # Tamaño de cada casilla del tablero

# Posiciones iniciales de cada tipo de pieza en el tablero
initial_positions = {
    "rook": [(0, 0), (7, 0), (0, 7), (7, 7)],
    "knight": [(1, 0), (6, 0), (1, 7), (6, 7)],
    "bishop": [(2, 0), (5, 0), (2, 7), (5, 7)],
    "queen": [(3, 0), (3, 7)],
    "king": [(4, 0), (4, 7)],
    "pawn": [(i, 1) for i in range(8)] + [(i, 6) for i in range(8)],
}


# Clase principal que representa la interfaz del menú inicial
class Interface:
    def __init__(self, win):
        self.win = win

        # Imagen del tablero de fondo
        self.b_img = pygame.image.load("images/board.png").convert_alpha()
        self.b_pos = (0, 0)  # Esquina superior izquierda del tablero
        self.b_size = 0.9  # Tamaño del tablero relativo a la altura de la ventana
        self.b_margin = (1 - self.b_size) / 2  # Margen vertical

        self.start_pressed = False
        self.settings_pressed = False
        self.font_button = pygame.font.SysFont("Arial", 28, bold=True)

        self.piece_images = {}  # Diccionario para guardar imágenes de piezas
        self.load_piece_images()

    # Cargar imágenes de piezas y botones desde carpeta 'images'
    def load_piece_images(self):
        pieces = ["rook", "knight", "bishop", "queen", "king", "pawn"]
        colors = ["w", "b"]
        for color in colors:
            for piece in pieces:
                name = f"{piece}_{color}"
                path = os.path.join("images", f"{name}.png")
                self.piece_images[name] = pygame.image.load(path)

        # También cargamos iconos de "play" y "settings"
        self.piece_images["play"] = pygame.image.load("images/play.png")
        self.piece_images["settings"] = pygame.image.load("images/settings.png")

    # Dibuja las piezas en el tablero según las posiciones iniciales
    def draw_pieces(self):
        board_margin = self.win.get_size()[1] * self.b_margin
        board_size = self.win.get_size()[1] * self.b_size
        square_size = board_size / 8

        for piece, positions in initial_positions.items():
            for col, row in positions:
                color = "b" if row < 2 else "w"
                name = f"{piece}_{color}"
                image = self.piece_images.get(name)
                if image:
                    x = col * square_size + board_margin
                    y = row * square_size + board_margin
                    image_scaled = pygame.transform.smoothscale(image, (square_size, square_size))
                    self.win.blit(image_scaled, (x, y))

    # Dibuja la imagen del tablero con esquinas redondeadas
    def draw_board(self):
        b_pos = self.win.get_size()[1] * self.b_margin
        b_dim = self.win.get_size()
        b_s = b_dim[1] * self.b_size

        board = pygame.transform.scale(self.b_img, (b_s, b_s))
        self.round_corners(board, round(self.win.get_size()[1] * 0.01))
        self.win.blit(board, (b_pos, b_pos))

    # Dibuja la barra lateral con título y botones
    def draw_sidebar(self):
        sdb_posy = self.win.get_size()[1] * self.b_margin
        sdb_posx = self.win.get_size()[1] * (3 * self.b_margin + self.b_size)

        sdb_dimx, sdb_dimy = self.win.get_size()
        sdb_dimx = sdb_dimx * 0.975 - sdb_posx
        sdb_dimy = sdb_dimy * self.b_size

        if sdb_dimx > self.win.get_size()[1] * 0.1:
            sidebar = pygame.Surface((sdb_dimx, sdb_dimy), pygame.SRCALPHA)
            sidebar.fill((0, 0, 0, 256 * 0.4))
            self.round_corners(sidebar, round(self.win.get_size()[1] * 0.01))
            self.win.blit(sidebar, (sdb_posx, sdb_posy))

            # Fuente dinámica para el título
            font_size = min(int(sdb_dimy * 0.09), int(sdb_dimx * 0.12))
            dynamic_font = pygame.font.SysFont("Arial", font_size, bold=True)

            lines = ["LET'S", "PLAY", "CHESS"]
            for i, line in enumerate(lines):
                text = dynamic_font.render(line, True, WHITE)
                self.win.blit(text, (sdb_posx + sdb_dimx / 3, sdb_posy + sdb_dimy * 0.1 + i * font_size))

            # Posiciones y tamaño de los botones
            b_posx = sdb_posx - self.win.get_size()[1] * 0.0875
            b_posy_down, b_posy_up = self.win.get_size()[1] * 0.51, self.win.get_size()[1] * 0.42
            b_dim = self.win.get_size()[1] * 0.075

            self.start_button_rect = pygame.Rect(b_posx, b_posy_up, b_dim, b_dim,
                                                 border_radius=self.win.get_size()[1] * 0.01)
            self.settings_button_rect = pygame.Rect(b_posx, b_posy_down, b_dim, b_dim,
                                                    border_radius=self.win.get_size()[1] * 0.01)

            self.draw_button(self.start_button_rect, "", self.start_pressed, "play")
            self.draw_button(self.settings_button_rect, "", self.settings_pressed, "settings")

    # Dibuja un botón con imagen
    def draw_button(self, rect, text, is_pressed, image_key=None):
        color = BLACK if is_pressed else DARK
        pygame.draw.rect(self.win, color, rect, border_radius=8)

        if image_key and image_key in self.piece_images:
            img = self.piece_images[image_key]
            img = pygame.transform.smoothscale(img, (rect.width, rect.height))
            self.win.blit(img, rect)

        if text:
            text_surface = self.font_button.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=rect.center)
            self.win.blit(text_surface, text_rect)

    # Aplica esquinas redondeadas a una imagen
    def round_corners(self, img, r):
        mask = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=r)
        img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # Actualiza la pantalla completa
    def update(self):
        self.win.fill(BLACK)
        self.draw_board()
        self.draw_pieces()
        self.draw_sidebar()
        pygame.display.flip()

    # Maneja eventos de clic del mouse
    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos):
                self.start_pressed = True
                pygame.quit()
                Juego_ajedrez().run()  # Llama a tu clase de juego (debes definirla aparte)
                sys.exit()
            elif self.settings_button_rect.collidepoint(event.pos):
                self.settings_pressed = True
                print("Configuraciones...")  # Aquí puedes abrir tu menú de ajustes


# Función principal para iniciar el programa
def main():
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Chess Interface")
    interface = Interface(win)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            interface.handle_mouse_event(event)

        interface.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()