import pygame

def pos_to_notation(pos):
    col_to_file = "abcdefgh"
    col, row = pos
    return f"{col_to_file[col]}{8 - row}"

# Modelo: piezas
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

# Modelo: tablero
class Board:
    def __init__(self):
        self.initial_positions = {
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
        self.current_positions = {k: list(v) for k, v in self.initial_positions.items()}
        self.game_over = False
        self.winner = None

    def is_square_empty(self, square):
        return all(square not in positions for positions in self.current_positions.values())

    def is_square_occupied_by_opponent(self, square, color):
        opponent = "b" if color == "w" else "w"
        return any(
            piece.endswith(f"_{opponent}") and square in positions
            for piece, positions in self.current_positions.items()
        )

    def get_king_position(self, color):
        return self.current_positions.get(f"king_{color}", [None])[0]

    def get_moves(self, piece_key, pos):
        name, color = piece_key.split('_')
        piece_class_map = {
            "pawn": Pawn,
            "knight": Knight,
            "bishop": Bishop,
            "rook": Rook,
            "queen": Queen,
            "king": King
        }
        piece_class = piece_class_map.get(name)
        if not piece_class:
            return []
        piece = piece_class(name, color)
        return piece.get_moves(pos, self)

    def is_king_in_check(self, color):
        king_pos = self.get_king_position(color)
        if king_pos is None:
            return False
        opponent_color = "b" if color == "w" else "w"
        for piece, positions in self.current_positions.items():
            if piece.endswith(f"_{opponent_color}"):
                for pos in positions:
                    moves = self.get_moves(piece, pos)
                    if king_pos in moves:
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_king_in_check(color):
            return False
        for piece_key, positions in self.current_positions.items():
            if piece_key.endswith(f"_{color}"):
                for pos in positions:
                    moves = self.get_moves(piece_key, pos)
                    for move in moves:
                        captured = self.move_piece(piece_key, pos, move, simulate=True)
                        if not self.is_king_in_check(color):
                            self.move_piece(piece_key, move, pos, simulate=True)
                            self.restore_captured(captured)
                            return False
                        self.move_piece(piece_key, move, pos, simulate=True)
                        self.restore_captured(captured)
        return True

    def restore_captured(self, captured_pieces):
        for piece_key, pos in captured_pieces:
            if piece_key in self.current_positions:
                self.current_positions[piece_key].append(pos)
            else:
                self.current_positions[piece_key] = [pos]

    def move_piece(self, piece_key, start_pos, end_pos, simulate=False):
        if self.game_over and not simulate:
            return []

        captured_pieces = []
        for p, positions in list(self.current_positions.items()):
            if end_pos in positions:
                if p.startswith("king") and not simulate:
                    self.game_over = True
                    self.winner = "white" if p.endswith("b") else "black"
                if simulate:
                    captured_pieces.append((p, end_pos))
                positions.remove(end_pos)
                if not positions:
                    del self.current_positions[p]

        if start_pos in self.current_positions.get(piece_key, []):
            self.current_positions[piece_key].remove(start_pos)
            self.current_positions[piece_key].append(end_pos)
        elif simulate:
            if piece_key in self.current_positions and end_pos not in self.current_positions[piece_key]:
                self.current_positions[piece_key].append(end_pos)
            elif piece_key not in self.current_positions:
                self.current_positions[piece_key] = [end_pos]

        return captured_pieces