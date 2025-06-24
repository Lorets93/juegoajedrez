# Define la interfaz gráfica del juego de ajedrez. Se encarga de dibujar tablero, piezas, botones, mensajes y sonidos.

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

        # Fuentes para botones y texto de movimientos
        self.movestext_x = 0.2
        self.movestext_y = 0.3

        self.font_button = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_move = pygame.font.SysFont("Arial", 18)
        # Estados de botones y juego
        self.start_button_rect = None
        self.settings_button_rect = None
        self.start_pressed = False
        self.settings_pressed = False

        self.game_over = False
        # Carga de imágenes de piezas
        self.piece_images = {}
        self.load_piece_images()
        # Configuración inicial
        self.sound_on = True
        self.dark_theme = False
        self.language = "en"
        self.settings_buttons = {}
        # Sonidos
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound("sounds/piecemove.wav")
        self.check_sound = pygame.mixer.Sound("sounds/checkmate.wav")
        self.victory_sound = pygame.mixer.Sound("sounds/victory.wav")
        # Scroll en historial de movimientos
        self.scroll_offset = 0
        self.max_scroll_offset = 0
        self.up_scroll_rect = None
        self.down_scroll_rect = None

    def load_piece_images(self):
        # Carga las imágenes de cada tipo de pieza
        pieces = ["rook", "knight", "bishop", "queen", "king", "pawn"]
        colors = ["w", "b"]
        for color in colors:
            for piece in pieces:
                name = f"{piece}_{color}"
                path = os.path.join("images", f"{name}.png")
                self.piece_images[name] = pygame.image.load(path)

    def draw_board(self):
        # Dibuja el fondo del tablero
        h = self.win.get_size()[1]
        b_pos = h * self.b_margin
        b_size = h * self.b_size
        board_path = "images/board_dark.png" if self.dark_theme else "images/board_light.png"
        board_img = pygame.image.load(board_path).convert_alpha()
        board = pygame.transform.scale(board_img, (b_size, b_size))
        self.round_corners(board, round(h * 0.01))
        self.win.blit(board, (b_pos, b_pos))

    def draw_pieces(self, positions):
        # Dibuja todas las piezas en sus posiciones actuales
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
        # Dibuja la barra lateral con el título, botones y espacio para movimientos
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
            # Texto dinámico
            if self.language == "es":
                lines = ["AJEDREZ"] if self.start_pressed else ["JUGUEMOS", "A", "AJEDREZ"]
            else:
                lines = ["CHESS"] if self.start_pressed else ["LET'S", "PLAY", "CHESS"]
            for i, line in enumerate(lines):
                text = dynamic_font.render(line, True, WHITE)
                rect = text.get_rect(center=(sdb_posx + sdb_dimx / 2, sdb_posy + sdb_dimy * 0.1 + i * font_size))
                self.win.blit(text, rect)

            self.draw_buttons(sdb_posx)
            return sdb_posx, sdb_dimx, sdb_posy, sdb_dimy

    def draw_buttons(self, sdb_posx):
        # Dibuja los botones de Play y Settings con efecto de clic
        h = self.win.get_size()[1]
        b_dim = h * 0.08
        b_posx = sdb_posx - h * 0.0875
        b_posy_up = h * 0.42
        b_posy_down = b_posy_up + b_dim + h * 0.045

        offset = 3  # efecto de empuje
        start_offset = offset if self.start_pressed else 0
        settings_offset = offset if self.settings_pressed else 0

        self.start_button_rect = pygame.Rect(b_posx, b_posy_up + start_offset, b_dim, b_dim)
        self.settings_button_rect = pygame.Rect(b_posx, b_posy_down + settings_offset, b_dim, b_dim)

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
        # Dibuja el triángulo del botón de Play
        padding = rect.width * 0.25
        point1 = (rect.left + padding, rect.top + padding)
        point2 = (rect.left + padding, rect.bottom - padding)
        point3 = (rect.right - padding, rect.top + rect.height / 2)
        pygame.draw.polygon(self.win, WHITE, [point1, point2, point3])

    def draw_settings_text(self, rect):
        # Dibuja el icono de ajustes
        icon_path = os.path.join("images", "settings.png")
        try:
            icon = pygame.image.load(icon_path).convert_alpha()
            icon = pygame.transform.smoothscale(icon, (rect.width - 8, rect.height - 8))
            self.win.blit(icon, (rect.x + 4, rect.y + 4))
        except pygame.error:
            font_size = int(rect.height * 0.4)
            font = pygame.font.SysFont("Arial", font_size, bold=True)
            fallback_text = "⚙"
            text = font.render(fallback_text, True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            self.win.blit(text, text_rect)

    def round_corners(self, img, r):
        # Redondea las esquinas de una superficie
        mask = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=r)
        img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def draw_legal_moves_highlights(self, legal_moves):
        # Dibuja los círculos para las jugadas legales
        if not legal_moves:
            return

        h = self.win.get_size()[1]
        margin = h * self.b_margin
        square_size = h * self.b_size / 8

        for col, row in legal_moves:
            overlay = pygame.Surface((int(square_size), int(square_size)), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (48, 46, 43, 180), (square_size // 2, square_size // 2), int(square_size * 0.15))
            self.win.blit(overlay, (int(margin + col * square_size), int(margin + row * square_size)))

    def display_message(self, message, color, font_size=36):
        w, h = self.win.get_size()
        panel_width = w * 0.5
        panel_height = h * 0.2
        panel_x = (w - panel_width) // 2
        panel_y = (h - panel_height) // 2

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.win.blit(overlay, (0, 0))

        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((40, 40, 40, 230))
        self.round_corners(panel, 12)
        self.win.blit(panel, (panel_x, panel_y))

        font = pygame.font.SysFont("Arial", font_size, bold=True)
        text = font.render(message, True, color)
        rect = text.get_rect(center=(w // 2, panel_y + panel_height // 2 - 20))
        self.win.blit(text, rect)

        button_width = 120
        button_height = 40
        close_rect = pygame.Rect(
            w // 2 - button_width // 2,
            panel_y + panel_height - button_height - 10,
            button_width,
            button_height
        )
        close_label = "Cerrar" if self.language == "es" else "Close"
        button_font = pygame.font.SysFont("Arial", 22, bold=True)
        button_text = button_font.render(close_label, True, WHITE)
        button_text_rect = button_text.get_rect(center=close_rect.center)

        pygame.draw.rect(self.win, (100, 40, 40), close_rect, border_radius=8)
        self.win.blit(button_text, button_text_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if close_rect.collidepoint(event.pos):
                        waiting = False

    def write_moves(self, move_log, sdb_posx, sdb_dimx, sdb_posy, sdb_dimy):
        line_height = 22
        max_visible_lines = int(sdb_dimy * 0.675 / line_height)
        total_lines = len(move_log)

        self.max_scroll_offset = max(0, total_lines - max_visible_lines)
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll_offset))

        displayed = move_log[self.scroll_offset:self.scroll_offset + max_visible_lines]

        x = sdb_posx + sdb_dimx * self.movestext_x
        y = sdb_posy + sdb_dimy * self.movestext_y

        # Encabezado
        title_text = "Lista de movimientos" if self.language == "es" else "Move List"
        title_surface = self.font_move.render(title_text, True, WHITE)
        self.win.blit(title_surface, (x, y - 30))

        for i, move in enumerate(displayed, start=self.scroll_offset + 1):
            text = self.font_move.render(f"{i}. {move}", True, TEXT_COLOR)
            self.win.blit(text, (x, y))
            y += line_height

        # Botones de scroll ▲▼
        btn_width = 30
        btn_height = 30
        margin = 10
        btn_x = sdb_posx + sdb_dimx - btn_width - margin
        up_y = sdb_posy + sdb_dimy * self.movestext_y - 35
        down_y = up_y + max_visible_lines * line_height + 5

        self.scroll_up_button = pygame.Rect(btn_x, up_y, btn_width, btn_height)
        self.scroll_down_button = pygame.Rect(btn_x, down_y, btn_width, btn_height)

        pygame.draw.rect(self.win, DARK, self.scroll_up_button, border_radius=4)
        pygame.draw.rect(self.win, DARK, self.scroll_down_button, border_radius=4)

        arrow_font = pygame.font.SysFont("Arial", 22, bold=True)
        up_arrow = arrow_font.render("▲", True, WHITE)
        down_arrow = arrow_font.render("▼", True, WHITE)
        self.win.blit(up_arrow, up_arrow.get_rect(center=self.scroll_up_button.center))
        self.win.blit(down_arrow, down_arrow.get_rect(center=self.scroll_down_button.center))

    def draw_settings_panel(self):
        w, h = self.win.get_size()
        panel_width = w * 0.5
        panel_height = h * 0.6
        panel_x = (w - panel_width) // 2
        panel_y = (h - panel_height) // 2

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.win.blit(overlay, (0, 0))

        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 240))
        self.round_corners(panel, 12)
        self.win.blit(panel, (panel_x, panel_y))

        font = pygame.font.SysFont("Arial", 24, bold=True)

        lang = self.language
        label_lang = "Idioma" if lang == "es" else "Language"
        label_sound = "Sonido" if lang == "es" else "Sound"
        label_theme = "Tema" if lang == "es" else "Theme"
        label_rules = "Ver reglas" if lang == "es" else "See rules"
        label_close = "Cerrar" if lang == "es" else "Close"

        val_yes = "Sí" if lang == "es" else "Yes"
        val_no = "No" if lang == "es" else "No"
        val_dark = "Oscuro" if lang == "es" else "Dark"
        val_light = "Claro" if lang == "es" else "Light"

        options = [
            ("toggle_language", f"{label_lang}: {'Español' if lang == 'es' else 'English'}"),
            ("toggle_sound", f"{label_sound}: {val_yes if self.sound_on else val_no}"),
            ("toggle_theme", f"{label_theme}: {val_dark if self.dark_theme else val_light}"),
            ("show_help", label_rules),
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

        close_y = start_y + len(options) * (button_height + spacing) + 10
        close_rect = pygame.Rect((w - button_width) // 2, close_y, button_width, button_height)
        pygame.draw.rect(self.win, (100, 40, 40), close_rect, border_radius=8)
        close_text = font.render(label_close, True, WHITE)
        close_text_rect = close_text.get_rect(center=close_rect.center)
        self.win.blit(close_text, close_text_rect)

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

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if close_rect.collidepoint(event.pos):
                        waiting = False

    def play_move_sound(self):
        if self.sound_on:
            pygame.mixer.stop()
            self.move_sound.play()

    def play_check_sound(self):
        if self.sound_on:
            pygame.mixer.stop()
            self.check_sound.play()

    def play_victory_sound(self):
        if self.sound_on:
            pygame.mixer.stop()
            self.victory_sound.play()

    def draw_coordinates(self):
        # Dibuja letras y números alrededor del tablero (a–h y 1–8)
        h = self.win.get_size()[1]
        margin = h * self.b_margin
        square_size = h * self.b_size / 8

        font = pygame.font.SysFont("Arial", int(square_size * 0.25), bold=True)
        files = "abcdefgh"
        ranks = "87654321"

        # Dibujar letras (a–h) abajo
        for i in range(8):
            label = font.render(files[i], True, WHITE)
            x = margin + i * square_size + square_size / 2 - label.get_width() / 2
            y = margin + 8 * square_size + 2
            self.win.blit(label, (x, y))

        # Dibujar números (1–8) izquierda
        for i in range(8):
            label = font.render(ranks[i], True, WHITE)
            x = margin - label.get_width() - 4
            y = margin + i * square_size + square_size / 2 - label.get_height() / 2
            self.win.blit(label, (x, y))

    def update(self, positions, legal_moves=None, move_log=None, show_settings=False):
        # Actualiza la pantalla en cada fotograma
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
        if self.start_pressed:
            self.draw_coordinates()
        pygame.display.flip()

    def display_promotion_choice(self, color):
        """
        Muestra una ventana emergente para que el jugador elija la pieza con la que desea promover su peón.
        Devuelve el nombre de la pieza elegida (queen, rook, bishop, knight).
        """
        w, h = self.win.get_size()
        panel_width = 300
        panel_height = 150
        panel_x = (w - panel_width) // 2
        panel_y = (h - panel_height) // 2

        # Crea fondo translúcido
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.win.blit(overlay, (0, 0))

        # Crea el panel central
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((40, 40, 40, 230))
        self.round_corners(panel, 12)
        self.win.blit(panel, (panel_x, panel_y))

        # Título del panel
        font = pygame.font.SysFont("Arial", 24, bold=True)
        label = "Elige pieza" if self.language == "es" else "Choose piece"
        text = font.render(label, True, WHITE)
        self.win.blit(text, (panel_x + 20, panel_y + 10))

        # Lista de piezas disponibles para promoción
        pieces = ["queen", "rook", "bishop", "knight"]
        buttons = []
        button_size = 60
        spacing = 10
        start_x = panel_x + (panel_width - (len(pieces) * (button_size + spacing))) // 2

        # Dibuja cada botón con su imagen correspondiente
        for i, p in enumerate(pieces):
            rect = pygame.Rect(start_x + i * (button_size + spacing), panel_y + 50, button_size, button_size)
            buttons.append((p, rect))
            piece_image = self.piece_images.get(f"{p}_{color}")
            if piece_image:
                img = pygame.transform.smoothscale(piece_image, (button_size, button_size))
                self.win.blit(img, rect)

        # Muestratodo en pantalla
        pygame.display.flip()

        # Espera a que el jugador haga clic en una de las opciones
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for p, rect in buttons:
                        if rect.collidepoint(event.pos):
                            return p  # Devuelve la pieza elegida

        return None  # Si no se elige ninguna (no debería pasar)


