import pygame

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
        # Posiciones iniciales
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
        self.current_positions = {}
        for k, v in self.initial_positions.items():
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








