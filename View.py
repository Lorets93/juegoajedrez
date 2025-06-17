import pygame
import os

BLACK = (48, 46, 43)
WHITE = (255, 255, 255)
LIGHT = (237, 237, 237)
DARK = (137, 169, 103)
TEXT_COLOR = (230, 230, 230)

class Interface:
    def __init__(self, win):
        self.win = win
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

        self.sound_on = True
        self.dark_theme = False
        self.language = "en"
        self.settings_buttons = {}

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

        # Elige la imagen según el tema
        board_path = "images/board_dark.png" if self.dark_theme else "images/board_light.png"
        board_img = pygame.image.load(board_path).convert_alpha()
        board = pygame.transform.scale(board_img, (b_size, b_size))

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

            if self.language == "es":
                lines = ["JUGUEMOS", "A", "AJEDREZ"]
            else:
                lines = ["LET'S", "PLAY", "CHESS"]
            for i, line in enumerate(lines):
                text = dynamic_font.render(line, True, WHITE)
                rect = text.get_rect(center=(sdb_posx + sdb_dimx / 2, sdb_posy + sdb_dimy * 0.1 + i * font_size))
                self.win.blit(text, rect)

            self.draw_buttons(sdb_posx)
            return sdb_posx, sdb_dimx, sdb_posy, sdb_dimy

    def draw_buttons(self, sdb_posx):
        h = self.win.get_size()[1]
        b_dim = h * 0.08
        b_posx = sdb_posx - h * 0.0875
        b_posy_up = h * 0.42
        b_posy_down = b_posy_up + b_dim + h * 0.045  # 0.045 da el mismo espacio proporcional entre botones

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
        icon_path = os.path.join("images", "settings.png")
        try:
            icon = pygame.image.load(icon_path).convert_alpha()
            # Escala la imagen para que encaje dentro del botón con un pequeño margen
            icon = pygame.transform.smoothscale(icon, (rect.width - 8, rect.height - 8))
            self.win.blit(icon, (rect.x + 4, rect.y + 4))
        except pygame.error:
            # Fallback en caso de error (imagen no encontrada o corrupta)
            font_size = int(rect.height * 0.4)
            font = pygame.font.SysFont("Arial", font_size, bold=True)
            fallback_text = "⚙"
            text = font.render(fallback_text, True, WHITE)
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

    def display_message(self, message, color, font_size=48):
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        text = font.render(message, True, color)
        rect = text.get_rect(center=(self.win.get_width() // 2, self.win.get_height() // 2 - 40))

        # Texto del botón traducido
        close_label = "Cerrar" if self.language == "es" else "Close"
        button_width = 120
        button_height = 40
        close_rect = pygame.Rect(
            (self.win.get_width() - button_width) // 2,
            rect.bottom + 30,
            button_width,
            button_height
        )

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and close_rect.collidepoint(event.pos):
                    return

            # Fondo translúcido
            overlay = pygame.Surface(self.win.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.win.blit(overlay, (0, 0))

            # Mensaje
            self.win.blit(text, rect)

            # Botón traducido
            pygame.draw.rect(self.win, (100, 40, 40), close_rect, border_radius=8)
            button_text = pygame.font.SysFont("Arial", 24, bold=True).render(close_label, True, WHITE)
            self.win.blit(button_text, button_text.get_rect(center=close_rect.center))

            pygame.display.flip()

    def write_moves(self, move_log, sdb_posx, sdb_dimx, sdb_posy, sdb_dimy):
        max_moves = int(sdb_dimy * 0.675 / 22)
        displayed = move_log[-max_moves:]

        x = sdb_posx + sdb_dimx * self.movestext_x
        y = sdb_posy + sdb_dimy * self.movestext_y

        for i, move in enumerate(displayed, start=len(move_log) - len(displayed) + 1):
            text = self.font_move.render(f"{i}. {move}", True, TEXT_COLOR)
            self.win.blit(text, (x, y))
            y += 22

    def draw_settings_panel(self):
        w, h = self.win.get_size()
        panel_width = w * 0.5
        panel_height = h * 0.6
        panel_x = (w - panel_width) // 2
        panel_y = (h - panel_height) // 2

        # Fondo oscuro translúcido
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.win.blit(overlay, (0, 0))

        # Panel principal
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 240))
        self.round_corners(panel, 12)
        self.win.blit(panel, (panel_x, panel_y))

        font = pygame.font.SysFont("Arial", 24, bold=True)
        options = [
            ("toggle_language", "Idioma: " + ("Español" if self.language == "es" else "English")),
            ("toggle_sound", "Sonido: " + ("Sí" if self.sound_on else "No")),
            ("toggle_theme", "Tema: " + ("Oscuro" if self.dark_theme else "Claro")),
            ("show_help", "Ver reglas"),
        ]

        self.settings_buttons.clear()
        button_width = panel_width * 0.8
        button_height = 45
        spacing = 20
        start_y = panel_y + 40

        for i, (key, label) in enumerate(options):
            btn_x = (w - button_width) // 2
            btn_y = start_y + i * (button_height + spacing)
            rect = pygame.Rect(btn_x, btn_y, button_width, button_height)

            pygame.draw.rect(self.win, DARK, rect, border_radius=8)
            text = font.render(label, True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            self.win.blit(text, text_rect)

            self.settings_buttons[key] = rect

        # Botón "Cerrar"
        close_y = start_y + len(options) * (button_height + spacing) + 10
        close_rect = pygame.Rect(btn_x, close_y, button_width, button_height)
        pygame.draw.rect(self.win, (100, 40, 40), close_rect, border_radius=8)
        close_text = font.render("Cerrar", True, WHITE)
        self.win.blit(close_text, close_text.get_rect(center=close_rect.center))
        self.settings_buttons["close_settings"] = close_rect

    def handle_settings_click(self, pos):
        for key, rect in self.settings_buttons.items():
            if rect.collidepoint(pos):
                return key
        return None

    def display_help(self):
        font = pygame.font.SysFont("Arial", 20, bold=False)
        rules = [
            "Reglas básicas del ajedrez:",
            "- Cada jugador mueve una pieza por turno.",
            "- El objetivo es dar jaque mate al rey enemigo.",
            "- No puedes hacer movimientos que dejen tu rey en jaque.",
            "- Usa el botón 'Start' para reiniciar la partida.",
        ]

        w, h = self.win.get_size()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.win.blit(overlay, (0, 0))

        panel_width = w * 0.6
        panel_height = h * 0.5
        panel_x = (w - panel_width) // 2
        panel_y = (h - panel_height) // 2

        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 240))
        self.round_corners(panel, 12)
        self.win.blit(panel, (panel_x, panel_y))

        for i, line in enumerate(rules):
            text = font.render(line, True, WHITE)
            self.win.blit(text, (panel_x + 30, panel_y + 30 + i * 30))

        # Botón cerrar
        button_width = 100
        button_height = 40
        close_rect = pygame.Rect(
            panel_x + (panel_width - button_width) // 2,
            panel_y + panel_height - 60,
            button_width,
            button_height
        )
        pygame.draw.rect(self.win, (100, 40, 40), close_rect, border_radius=8)
        close_text = font.render("Cerrar", True, WHITE)
        self.win.blit(close_text, close_text.get_rect(center=close_rect.center))

        pygame.display.flip()

        # Esperar clic en "Cerrar"
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if close_rect.collidepoint(event.pos):
                        waiting = False

    def update(self, positions, legal_moves=None, move_log=None, show_settings=False):
        self.win.fill(BLACK)
        self.draw_board()
        self.draw_pieces(positions)
        sidebar = self.draw_sidebar()
        if sidebar and move_log is not None:
            self.write_moves(move_log, *sidebar)
        if legal_moves:
            self.draw_legal_moves_highlights(legal_moves)
        if show_settings:
            self.draw_settings_panel()
        pygame.display.flip()
