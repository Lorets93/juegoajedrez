import pygame
import os
import sys

import Model
import Presenter

# Colores
BLACK = (48, 46, 43)
WHITE = (255, 255, 255)
LIGHT = (237, 237, 237)
DARK = (137, 169, 103)
TURQUOISE = (61, 213, 168)
TURQUOISE_DARK = (41, 173, 138)
TEXT_COLOR = (230, 230, 230)

# Tamaños
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SQUARE_SIZE = 60  # Puedes ajustar para que escale dinámicamente

class Interface:
    def __init__(self, win):
        self.win = win

        self.b_img = pygame.image.load("images/board.png").convert_alpha()  # board image
        self.b_pos = (0, 0)  # tuple - board top-left corner position
        self.b_size = 0.9  # board size relative to window height (%)
        self.b_margin = (1 - self.b_size) / 2  # board margin to window height (%)

        self.movestext_y = 0.3
        self.movestext_x= 0.2

        self.start_button_rect=None
        self.settings_button_rect=None

        self.start_pressed = False
        self.settings_pressed = False
        self.font_button = pygame.font.SysFont("Arial", 28, bold=True)

        self.font_move = pygame.font.SysFont("Arial", 18)

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
                self.piece_images[name] = image

    def draw_pieces(self, positions):
        board_margin = self.win.get_size()[1] * self.b_margin
        board_size = self.win.get_size()[1] * self.b_size
        square_size = board_size / 8

        for piece, positions in positions.items():
            for col, row in positions:
                #color = "b" if row < 2 else "w"
                #name = f"{piece}_{color}"
                image = self.piece_images.get(piece)
                if image:
                    x = col * square_size + board_margin
                    y = row * square_size + board_margin
                    image_scaled = pygame.transform.smoothscale(image, (square_size, square_size))
                    self.win.blit(image_scaled, (x, y))

    def draw_board(self):
        b_pos = self.win.get_size()[1] * self.b_margin

        b_dim = self.win.get_size()
        b_s = b_dim[1] * self.b_size

        board = pygame.transform.scale(self.b_img, (b_s, b_s))

        self.round_corners(board, round(self.win.get_size()[1] * 0.01))

        self.win.blit(board, (b_pos, b_pos))

    def draw_sidebar(self):
        sdb_posy = self.win.get_size()[1] * self.b_margin

        sdb_posx = self.win.get_size()[1] * (3 * self.b_margin + self.b_size)

        sdb_dimx, sdb_dimy = self.win.get_size()
        sdb_dimx = sdb_dimx * 0.975 - sdb_posx
        sdb_dimy = sdb_dimy * self.b_size

        if sdb_dimx > self.win.get_size()[1] * 0.1:
            sidebar = pygame.Surface((sdb_dimx, sdb_dimy), pygame.SRCALPHA)
            sidebar.fill((0, 0, 0, int(256 * 0.4)))
            self.round_corners(sidebar, round(self.win.get_size()[1] * 0.01))
            self.win.blit(sidebar, (sdb_posx, sdb_posy))

            # Aumentar el tamaño de la fuente
            font_size = min(int(sdb_dimy * 0.15), int(sdb_dimx * 0.12))  # Aumentar el factor

            # Crear una fuente dinámica
            dynamic_font = pygame.font.SysFont("Arial", font_size, bold=True)

            # Dibujar cada línea con la fuente dinámica
            lines = ["LET'S", "PLAY", "CHESS"]
            for i, line in enumerate(lines):
                text = dynamic_font.render(line, True, WHITE)
                text_rect = text.get_rect(center=(sdb_posx + sdb_dimx / 2, sdb_posy + sdb_dimy * 0.1 + i * font_size))
                self.win.blit(text, text_rect)
            self.draw_buttons(sdb_posx)

            return sdb_posx, sdb_dimx, sdb_posy, sdb_dimy

    def draw_buttons(self, sdb_posx):
        # Buttons
        b_posx = sdb_posx - self.win.get_size()[1] * 0.0875
        b_posy_down, b_posy_up = self.win.get_size()[1] * 0.51, self.win.get_size()[1] * 0.42
        b_dim = self.win.get_size()[1] * 0.075

        self.start_button_rect = pygame.Rect(b_posx, b_posy_up, b_dim, b_dim,
                                             border_radius=self.win.get_size()[1] * 0.01)
        self.settings_button_rect = pygame.Rect(b_posx, b_posy_down, b_dim, b_dim,
                                                border_radius=self.win.get_size()[1] * 0.01)

        self.create_button(self.start_button_rect, "", self.start_pressed)
        self.create_button(self.settings_button_rect, "", self.settings_pressed)

        # Dibujar triángulo de "play" en el botón de inicio
        self.draw_play_icon(self.start_button_rect)

        # Dibujar texto "Settings" en el botón de configuración, ajustado al espacio
        self.draw_settings_text(self.settings_button_rect)

    def create_button(self, rect, text, is_pressed):
        color = BLACK if is_pressed else DARK
        offset = 2 if is_pressed else 0
        pygame.draw.rect(self.win, color, rect, border_radius=8)
        if text:
            text_surface = self.font_button.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery + offset))
            self.win.blit(text_surface, text_rect)

    def draw_play_icon(self, rect):
        # Dibujar un triángulo apuntando a la derecha (símbolo play)
        padding = rect.width * 0.25
        point1 = (rect.left + padding, rect.top + padding)
        point2 = (rect.left + padding, rect.bottom - padding)
        point3 = (rect.right - padding, rect.top + rect.height / 2)
        pygame.draw.polygon(self.win, WHITE, [point1, point2, point3])

    def draw_settings_text(self, rect):
        # Dibujar el texto "Setting" adaptado al área del botón para que quepa bien
        font_size = int(rect.height * 0.5)
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        text = font.render("Settings", True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        # Escalar texto si no cabe en el botón
        if text_rect.width > rect.width:
            scale_factor = rect.width / text_rect.width
            font_size = max(int(font_size * scale_factor), 10)
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
        """
        h = self.win.get_size()[1]
        margin = h * self.b_margin
        square_size = (h * self.b_size) / 8

        overlay = pygame.Surface((int(square_size), int(square_size)), pygame.SRCALPHA)
        overlay.fill((48, 46, 43))  # translucent light green

        for move in legal_moves:
            c, r = move
            pos_x = int(margin + c * square_size)
            pos_y = int(margin + r * square_size)
            self.win.blit(overlay, (pos_x, pos_y))
        """

        h = self.win.get_size()[1]
        margin = h * self.b_margin
        square_size = (h * self.b_size) / 8

        for col, row in legal_moves:
            center_x = int(margin + col * square_size)
            center_y = int(margin + row * square_size)
            radius = int(square_size * 0.15)  # You can tweak this size
            highlight = pygame.Surface((int(square_size), int(square_size)), pygame.SRCALPHA)
            pygame.draw.circle(highlight, (48, 46, 43, 180), (square_size // 2, square_size // 2), radius)
            self.win.blit(highlight, (center_x, center_y))

    def write_moves(self, move_log, sdb_posx, sdb_dimx, sdb_posy, sdb_dimy):

        max_moves_to_show = int(sdb_dimy*0.675/22)
        displayed_moves = move_log[-max_moves_to_show:]

        x=sdb_posx+sdb_dimx*self.movestext_x
        y = sdb_posy+sdb_dimy*self.movestext_y
        
        for i, move in enumerate(displayed_moves, start=len(move_log) - len(displayed_moves) + 1):
            move_text = f"{i}. {move}"
            text_surf = self.font_move.render(move_text, True, TEXT_COLOR)
            self.win.blit(text_surf, (x, y))
            y += 22

    def update(self, positions, legal_moves, move_log):
        self.win.fill(BLACK)
        self.draw_board()
        self.draw_pieces(positions)
        sdb_posx, sdb_dimx, sdb_posy, sdb_dimy=self.draw_sidebar()
        self.write_moves(move_log, sdb_posx, sdb_dimx, sdb_posy, sdb_dimy)
        self.draw_legal_moves_highlights(legal_moves)
        pygame.display.flip()











