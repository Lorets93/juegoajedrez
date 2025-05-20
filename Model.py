import pygame
import sys

# Colores
BLACK = (48, 46, 43)
WHITE = (255, 255, 255)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (0, 128, 0)
BUTTON_BG = (30, 90, 60)
BUTTON_BG_PRESSED = (20, 60, 40)
SIDEBAR_BG = (25, 50, 35)
TEXT_COLOR = (230, 230, 230)

# Tamaños
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Parámetros tablero
BOARD_SIZE_RATIO = 0.9
BOARD_MARGIN_RATIO = (1 - BOARD_SIZE_RATIO) / 2

# Posiciones iniciales
initial_positions = {
    "rook_w": [(0, 7), (7, 7)],
    "knight_w": [(1, 7), (6, 7)],
    "bishop_w": [(2, 7), (5, 7)],
    "queen_w": [(3, 7)],
    "king_w": [(4, 7)],
    "pawn_w": [(col, 6) for col in range(8)],
    "rook_b": [(0, 0), (7, 0)],
    "knight_b": [(1, 0), (6, 0)],
    "bishop_b": [(2, 0), (5, 0)],
    "queen_b": [(3, 0)],
    "king_b": [(4, 0)],
    "pawn_b": [(col, 1) for col in range(8)],
}

def pos_to_notation(pos):
    col_to_file = "abcdefgh"
    col, row = pos
    return f"{col_to_file[col]}{8 - row}"

# Model: lógica y estado del juego y piezas
class Piece:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.image = pygame.image.load(f"images/{name}_{color}.png")

    def get_moves(self, pos, board):
        raise NotImplementedError()

class Pawn(Piece):
    def get_moves(self, pos, board):
        moves = []
        col, row = pos
        direction = -1 if self.color == "w" else 1
        start_row = 6 if self.color == "w" else 1

        forward = (col, row + direction)
        if board.is_square_empty(forward):
            moves.append(forward)
            double_forward = (col, row + 2 * direction)
            if row == start_row and board.is_square_empty(double_forward):
                moves.append(double_forward)

        for dc in [-1, 1]:
            diag = (col + dc, row + direction)
            if 0 <= diag[0] < 8 and 0 <= diag[1] < 8:
                if board.is_square_occupied_by_opponent(diag, self.color):
                    moves.append(diag)
        return moves

class Knight(Piece):
    def get_moves(self, pos, board):
        moves = []
        col, row = pos
        offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                   (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dc, dr in offsets:
            new_col, new_row = col + dc, row + dr
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                if board.is_square_empty((new_col, new_row)) or board.is_square_occupied_by_opponent((new_col, new_row), self.color):
                    moves.append((new_col, new_row))
        return moves

class Bishop(Piece):
    def get_moves(self, pos, board):
        moves = []
        col, row = pos
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dc, dr in directions:
            for i in range(1, 8):
                new_col, new_row = col + dc * i, row + dr * i
                if 0 <= new_col < 8 and 0 <= new_row < 8:
                    if board.is_square_empty((new_col, new_row)):
                        moves.append((new_col, new_row))
                    elif board.is_square_occupied_by_opponent((new_col, new_row), self.color):
                        moves.append((new_col, new_row))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Rook(Piece):
    def get_moves(self, pos, board):
        moves = []
        col, row = pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dc, dr in directions:
            for i in range(1, 8):
                new_col, new_row = col + dc * i, row + dr * i
                if 0 <= new_col < 8 and 0 <= new_row < 8:
                    if board.is_square_empty((new_col, new_row)):
                        moves.append((new_col, new_row))
                    elif board.is_square_occupied_by_opponent((new_col, new_row), self.color):
                        moves.append((new_col, new_row))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Queen(Piece):
    def get_moves(self, pos, board):
        moves = []
        col, row = pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dc, dr in directions:
            for i in range(1, 8):
                new_col, new_row = col + dc * i, row + dr * i
                if 0 <= new_col < 8 and 0 <= new_row < 8:
                    if board.is_square_empty((new_col, new_row)):
                        moves.append((new_col, new_row))
                    elif board.is_square_occupied_by_opponent((new_col, new_row), self.color):
                        moves.append((new_col, new_row))
                        break
                    else:
                        break
                else:
                    break
        return moves

class King(Piece):
    def get_moves(self, pos, board):
        moves = []
        col, row = pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dc, dr in directions:
            new_col, new_row = col + dc, row + dr
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                if board.is_square_empty((new_col, new_row)) or board.is_square_occupied_by_opponent((new_col, new_row), self.color):
                    moves.append((new_col, new_row))
        return moves

class Board:
    def __init__(self):
        self.current_positions = {}
        for k, v in initial_positions.items():
            self.current_positions[k] = list(v)

    def is_square_empty(self, square):
        for positions in self.current_positions.values():
            if square in positions:
                return False
        return True

    def is_square_occupied_by_opponent(self, square, color):
        opponent = "b" if color == "w" else "w"
        for piece, positions in self.current_positions.items():
            if piece.endswith(f"_{opponent}") and square in positions:
                return True
        return False

    def move_piece(self, piece_key, start_pos, end_pos):
        # Captura
        for p, pos_list in list(self.current_positions.items()):
            if p != piece_key and end_pos in pos_list:
                pos_list.remove(end_pos)
                if not pos_list:
                    del self.current_positions[p]
        # Mover pieza
        if start_pos in self.current_positions[piece_key]:
            self.current_positions[piece_key].remove(start_pos)
        self.current_positions[piece_key].append(end_pos)
"""
# View: renderizado UI y tablero
class ChessView:
    def __init__(self, win):
        self.win = win
        self.b_margin = BOARD_MARGIN_RATIO
        self.b_size = BOARD_SIZE_RATIO

        self.b_img = pygame.image.load("images/board.png").convert_alpha()

        self.update_dimensions()

        self.font_title = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_move = pygame.font.SysFont("Arial", 18)
        self.font_button = pygame.font.SysFont("Arial", 20, bold=True)

    def update_dimensions(self):
        h = self.win.get_size()[1]
        self.sidebar_width = int(self.win.get_size()[0] - (h * self.b_size + h * self.b_margin * 3))
        self.sidebar_rect = pygame.Rect(
            h * (3 * self.b_margin + self.b_size) + h * self.b_margin,
            h * self.b_margin,
            self.sidebar_width,
            h * self.b_size)

        bh = h * 0.075
        bw = bh
        bx = self.sidebar_rect.left - h * 0.0875
        by1 = h * 0.42
        by2 = h * 0.51
        self.start_button_rect = pygame.Rect(bx, by1, bw, bh)
        self.settings_button_rect = pygame.Rect(bx, by2, bw, bh)

    def round_corners(self, img, r):
        mask = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=r)
        img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def draw_board(self):
        h = self.win.get_size()[1]
        margin = h * self.b_margin
        b_s = int(h * self.b_size)

        board = pygame.transform.smoothscale(self.b_img, (b_s, b_s))
        self.round_corners(board, round(h * 0.01))
        self.win.blit(board, (margin, margin))

    def draw_pieces(self, current_positions, piece_objects):
        h = self.win.get_size()[1]#
        margin = h * self.b_margin#
        square_size = (h * self.b_size) / 8#

        for piece_key, positions in current_positions.items():
            piece_obj = piece_objects.get(piece_key)
            if not piece_obj:
                continue
            for pos in positions:
                col, row = pos
                img = pygame.transform.smoothscale(piece_obj.image, (int(square_size), int(square_size)))
                self.win.blit(img, (margin + col * square_size, margin + row * square_size))

    def draw_legal_moves_highlights(self, legal_moves):
        if not legal_moves:
            return
        h = self.win.get_size()[1]
        margin = h * self.b_margin
        square_size = (h * self.b_size) / 8

        overlay = pygame.Surface((int(square_size), int(square_size)), pygame.SRCALPHA)
        overlay.fill((144, 238, 144, 100))  # translucent light green

        for move in legal_moves:
            c, r = move
            pos_x = int(margin + c * square_size)
            pos_y = int(margin + r * square_size)
            self.win.blit(overlay, (pos_x, pos_y))

    def draw_sidebar(self, move_log, start_pressed, settings_pressed):
        pygame.draw.rect(self.win, SIDEBAR_BG, self.sidebar_rect, border_radius=8)

        text_title = self.font_title.render("CHESS", True, TEXT_COLOR)
        title_rect = text_title.get_rect(center=(self.sidebar_rect.centerx, self.sidebar_rect.top + 40))
        self.win.blit(text_title, title_rect)

        moves_start_y = title_rect.bottom + 20
        max_moves_to_show = int((self.sidebar_rect.height - (moves_start_y - self.sidebar_rect.top) - 100) / 22)
        displayed_moves = move_log[-max_moves_to_show:]

        y = moves_start_y
        for i, move in enumerate(displayed_moves, start=len(move_log) - len(displayed_moves) + 1):
            move_text = f"{i}. {move}"
            text_surf = self.font_move.render(move_text, True, TEXT_COLOR)
            self.win.blit(text_surf, (self.sidebar_rect.left + 20, y))
            y += 22

        self.draw_button(self.start_button_rect, start_pressed, "Play")
        self.draw_button(self.settings_button_rect, settings_pressed, "Settings")

    def draw_button(self, rect, pressed, label):
        color = BUTTON_BG_PRESSED if pressed else BUTTON_BG
        pygame.draw.rect(self.win, color, rect, border_radius=8)
        text = self.font_button.render(label, True, TEXT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        self.win.blit(text, text_rect)

    def draw(self, current_positions, piece_objects, legal_moves, move_log, start_pressed, settings_pressed):
        self.win.fill(BLACK)
        self.draw_board()
        self.draw_legal_moves_highlights(legal_moves)
        self.draw_pieces(current_positions, piece_objects)
        self.draw_sidebar(move_log, start_pressed, settings_pressed)
        pygame.display.flip()
"""










