import pygame
import os

# Colores
BLACK = (48, 46, 43)
WHITE = (255, 255, 255)
LIGHT = (237, 237, 237)
DARK = (137, 169, 103)
TEXT_COLOR = (230, 230, 230)

class Interface:
    def __init__(self, win):
        self.win = win
        self.b_img = pygame.image.load("images/board.png").convert_alpha()

        self.b_size = 0.9
        self.b_margin = (1 - self.b_size) / 2

        self.movestext_x = 0.2
        self.movestext_y = 0.3

        self.font_button = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_move = pygame.font.SysFont("Arial", 18)

        self.start_button_rect = None
        self.settings_button_rect = None
        self.start_pressed = False
        self.settings_pressed = False

        self.game_over = False

        self.piece_images = {}
        self.load_piece_images()

    def load_piece_images(self):
        pieces = ["rook", "knight", "bishop", "queen", "king", "pawn"]
        colors = ["w", "b"]
        for color in colors:
            for piece in pieces:
                name = f"{piece}_{color}"
                path = os.path.join("images", f"{name}.png")
                self.piece_images[name] = pygame.image.load(path)

    def draw_board(self):
        h = self.win.get_size()[1]
        b_pos = h * self.b_margin
        b_size = h * self.b_size
        board = pygame.transform.scale(self.b_img, (b_size, b_size))
        self.round_corners(board, round(h * 0.01))
        self.win.blit(board, (b_pos, b_pos))

    def draw_pieces(self, positions):
        h = self.win.get_size()[1]
        margin = h * self.b_margin
        square_size = h * self.b_size / 8

        for piece, pos_list in positions.items():
            image = self.piece_images.get(piece)
            if image:
                for col, row in pos_list:
                    x = col * square_size + margin
                    y = row * square_size + margin
                    scaled = pygame.transform.smoothscale(image, (square_size, square_size))
                    self.win.blit(scaled, (x, y))

    def draw_sidebar(self):
        h = self.win.get_size()[1]
        w = self.win.get_size()[0]
        sdb_posx = h * (3 * self.b_margin + self.b_size)
        sdb_dimx = w * 0.975 - sdb_posx
        sdb_dimy = h * self.b_size
        sdb_posy = h * self.b_margin

        if sdb_dimx > h * 0.1:
            sidebar = pygame.Surface((sdb_dimx, sdb_dimy), pygame.SRCALPHA)
            sidebar.fill((0, 0, 0, int(256 * 0.4)))
            self.round_corners(sidebar, round(h * 0.01))
            self.win.blit(sidebar, (sdb_posx, sdb_posy))

            font_size = min(int(sdb_dimy * 0.15), int(sdb_dimx * 0.12))
            dynamic_font = pygame.font.SysFont("Arial", font_size, bold=True)

            lines = ["LET'S", "PLAY", "CHESS"]
            for i, line in enumerate(lines):
                text = dynamic_font.render(line, True, WHITE)
                rect = text.get_rect(center=(sdb_posx + sdb_dimx / 2, sdb_posy + sdb_dimy * 0.1 + i * font_size))
                self.win.blit(text, rect)

            self.draw_buttons(sdb_posx)
            return sdb_posx, sdb_dimx, sdb_posy, sdb_dimy

    def draw_buttons(self, sdb_posx):
        h = self.win.get_size()[1]
        b_dim = h * 0.075
        b_posx = sdb_posx - h * 0.0875
        b_posy_up = h * 0.42
        b_posy_down = h * 0.51

        self.start_button_rect = pygame.Rect(b_posx, b_posy_up, b_dim, b_dim)
        self.settings_button_rect = pygame.Rect(b_posx, b_posy_down, b_dim, b_dim)

        self.create_button(self.start_button_rect, "", self.start_pressed)
        self.create_button(self.settings_button_rect, "", self.settings_pressed)
        self.draw_play_icon(self.start_button_rect)
        self.draw_settings_text(self.settings_button_rect)

    def create_button(self, rect, text, is_pressed):
        color = BLACK if is_pressed else DARK
        pygame.draw.rect(self.win, color, rect, border_radius=8)
        if text:
            text_surface = self.font_button.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=rect.center)
            self.win.blit(text_surface, text_rect)

    def draw_play_icon(self, rect):
        padding = rect.width * 0.25
        point1 = (rect.left + padding, rect.top + padding)
        point2 = (rect.left + padding, rect.bottom - padding)
        point3 = (rect.right - padding, rect.top + rect.height / 2)
        pygame.draw.polygon(self.win, WHITE, [point1, point2, point3])

    def draw_settings_text(self, rect):
        font_size = int(rect.height * 0.5)
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        text = font.render("Settings", True, WHITE)
        text_rect = text.get_rect(center=rect.center)

        if text_rect.width > rect.width:
            scale = rect.width / text_rect.width
            font_size = max(int(font_size * scale), 10)
            font = pygame.font.SysFont("Arial", font_size, bold=True)
            text = font.render("Settings", True, WHITE)
            text_rect = text.get_rect(center=rect.center)

        self.win.blit(text, text_rect)

    def round_corners(self, img, r):
        mask = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=r)
        img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def draw_legal_moves_highlights(self, legal_moves):
        if not legal_moves:
            return

        h = self.win.get_size()[1]
        margin = h * self.b_margin
        square_size = h * self.b_size / 8

        for col, row in legal_moves:
            overlay = pygame.Surface((int(square_size), int(square_size)), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (48, 46, 43, 180), (square_size // 2, square_size // 2), int(square_size * 0.15))
            self.win.blit(overlay, (int(margin + col * square_size), int(margin + row * square_size)))

    def write_moves(self, move_log, sdb_posx, sdb_dimx, sdb_posy, sdb_dimy):
        max_moves = int(sdb_dimy * 0.675 / 22)
        displayed = move_log[-max_moves:]

        x = sdb_posx + sdb_dimx * self.movestext_x
        y = sdb_posy + sdb_dimy * self.movestext_y

        for i, move in enumerate(displayed, start=len(move_log) - len(displayed) + 1):
            text = self.font_move.render(f"{i}. {move}", True, TEXT_COLOR)
            self.win.blit(text, (x, y))
            y += 22

    def update(self, positions, legal_moves=None, move_log=None):
        self.win.fill(BLACK)
        self.draw_board()
        self.draw_pieces(positions)
        sidebar = self.draw_sidebar()
        if sidebar and move_log is not None:
            self.write_moves(move_log, *sidebar)
        if legal_moves:
            self.draw_legal_moves_highlights(legal_moves)
        pygame.display.flip()

    def display_message(self, message, color, font_size=48, duration=2000):
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        text = font.render(message, True, color)
        rect = text.get_rect(center=(self.win.get_width() // 2, self.win.get_height() // 2))
        overlay = pygame.Surface(self.win.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.win.blit(overlay, (0, 0))
        self.win.blit(text, rect)
        pygame.display.flip()
        pygame.time.delay(duration)

    def set_game_over(self, winner_name):
        self.display_message(f"{winner_name} gana!", (255, 0, 0), duration=4000)
        self.game_over = True
