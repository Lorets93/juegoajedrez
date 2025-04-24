import pygame, os, sys
# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT = (237, 237, 237)
DARK = (59, 59, 59)
TURQUOISE = (61, 213, 168)
TURQUOISE_DARK = (41, 173, 138)

# Tamaños
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SQUARE_SIZE = 60  # Puedes ajustar para que escale dinámicamente

# Posiciones iniciales
initial_positions = {
    "rook": [(0, 0), (7, 0), (0, 7), (7, 7)],
    "knight": [(1, 0), (6, 0), (1, 7), (6, 7)],
    "bishop": [(2, 0), (5, 0), (2, 7), (5, 7)],
    "queen": [(3, 0), (3, 7)],
    "king": [(4, 0), (4, 7)],
    "pawn": [(i, 1) for i in range(8)] + [(i, 6) for i in range(8)],
}
class Interface:
    def __init__(self, win):
        self.win=win

        self.b_img = pygame.image.load("images/board.png").convert_alpha() # board image
        self.b_pos = (0, 0) # tuple - board top-left corner position
        self.b_size = 0.9 # board size relative to window height (%)
        self.b_margin = (1-self.b_size)/2 # board margin to window height (%)
        self.font_large = pygame.font.SysFont("Arial", 60, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 28, bold=True)

        self.start_pressed = False
        self.settings_pressed = False

        self.piece_images = {}
        self.load_piece_images()

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
                    image_scaled = pygame.transform.scale(image, (square_size, square_size))
                    self.win.blit(image_scaled, (x, y))

    def update(self):
        return




    def main_menu(self):
        return

    def game(self):

        return

    def draw_board(self):
        #defining position coords
        #b_x, b_y= self.win.get_size() # get window size (for any resizing)
        b_pos= self.win.get_size()[1]*self.b_margin # take the percentage for the margin

        #defining board size
        b_dim= self.win.get_size() # get window size (for any resizing)
        b_s = b_dim[1]*self.b_size # takes percentage of screen size, also adjusts size with ratio for it to be a square

        board = pygame.transform.scale(self.b_img, (b_s, b_s))  # actual resizing of the image, with adjusted size

        self.round_corners(board, round(self.win.get_size()[1]*0.01)) # round corners -> 1% of screen height

        self.win.blit(board, (b_pos, b_pos)) # draw the board on top-left corner coords

    def draw_sidebar(self):
        sdb_posx = self.win.get_size()[0]*9/16
        sdb_posy = self.win.get_size()[1]*self.b_margin

        sdb_dimx, sdb_dimy = self.win.get_size()
        sdb_dimx = sdb_dimx*6.5/16
        sdb_dimy = sdb_dimy*self.b_size

        sidebar=pygame.Surface((sdb_dimx, sdb_dimy), pygame.SRCALPHA)
        sidebar.fill((0, 0, 0, 256*0.4))
        self.round_corners(sidebar, round(self.win.get_size()[1]*0.01))
        self.win.blit(sidebar, (sdb_posx, sdb_posy))

        # Título
        lines = ["LET'S", "PLAY", "CHESS"]
        for i, line in enumerate(lines):
            text = self.font_large.render(line, True, WHITE)
            self.win.blit(text, (sdb_posx + 50, sdb_posy + 40 + i * 80))

        # Botones
        self.start_button_rect = pygame.Rect(sdb_posx + 50, sdb_posy + 350, 200, 50)
        self.settings_button_rect = pygame.Rect(sdb_posx + 50, sdb_posy + 420, 200, 50)

        self.draw_button(self.start_button_rect, "START", self.start_pressed)
        self.draw_button(self.settings_button_rect, "SETTINGS", self.settings_pressed)

    def draw_button(self, rect, text, is_pressed):
        color = TURQUOISE_DARK if is_pressed else TURQUOISE
        offset = 2 if is_pressed else 0
        pygame.draw.rect(self.win, color, rect, border_radius=8)
        text_surface = self.font_button.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery + offset))
        self.win.blit(text_surface, text_rect)


        def update(self):
            self.win.fill(BLACK)
            self.draw_board()
            self.draw_pieces()
            self.draw_sidebar()
            pygame.display.flip()

    def round_corners(self, img, r):
         # Create a transparent mask surface
        mask = pygame.Surface(img.get_size(), pygame.SRCALPHA)

        # Draw a rounded rectangle on the mask
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=r)

        # Apply the rounded mask to the image
        img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def update(self):
        self.win.fill(BLACK)
        self.draw_board()
        self.draw_pieces()
        self.draw_sidebar()
        pygame.display.flip()


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

        interface.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()