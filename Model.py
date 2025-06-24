
# Contiene la lógica del tablero y las piezas. No usa interfaz gráfica.
class Board:
    def __init__(self):
        # Define las posiciones iniciales de cada pieza
        self.initial_positions = {
            "rook_b": [(0, 0), (7, 0)],
            "knight_b": [(1, 0), (6, 0)],
            "bishop_b": [(2, 0), (5, 0)],
            "queen_b": [(3, 0)],
            "king_b": [(4, 0)],
            "pawn_b": [(i, 1) for i in range(8)],
            "rook_w": [(0, 7), (7, 7)],
            "knight_w": [(1, 7), (6, 7)],
            "bishop_w": [(2, 7), (5, 7)],
            "queen_w": [(3, 7)],
            "king_w": [(4, 7)],
            "pawn_w": [(i, 6) for i in range(8)],
        }
        self.current_positions = {k: list(v) for k, v in self.initial_positions.items()}
        self.game_over = False
        self.winner = None

    def move_piece(self, piece_key, start_pos, end_pos, simulate=False):
        # Mueve una pieza y actualiza las posiciones.
        if start_pos in self.current_positions[piece_key]:
            self.current_positions[piece_key].remove(start_pos)

        # Ver si se captura alguna pieza
        for p, positions in self.current_positions.items():
            if end_pos in positions:
                if not simulate:
                    positions.remove(end_pos)
                    # Si se comió al rey
                    if p.startswith("king"):
                        self.game_over = True
                        self.winner = "white" if p.endswith("b") else "black"
                else:
                    positions.remove(end_pos)
                break

        if not simulate:
            self.current_positions[piece_key].append(end_pos)

    def get_all_pieces(self):
        # Devuelve una lista de todas las piezas en el tablero
        all_pieces = []
        for piece, positions in self.current_positions.items():
            for pos in positions:
                all_pieces.append((piece, pos))
        return all_pieces

    def get_king_position(self, color):
        # Devuelve la posición actual del rey del color indicado
        key = f"king_{color}"
        positions = self.current_positions.get(key, [])
        return positions[0] if positions else None

    def is_king_in_check(self, color):
        # Verifica si el rey está en jaque
        king_pos = self.get_king_position(color)
        if not king_pos:
            return False
        opponent_color = "b" if color == "w" else "w"
        for piece_key, positions in self.current_positions.items():
            if piece_key.endswith(opponent_color):
                for pos in positions:
                    piece_type = piece_key.split("_")[0]
                    piece_obj = self.get_piece_object(piece_type, opponent_color)
                    moves = piece_obj.get_moves(pos, self, simulate=True)
                    if king_pos in moves:
                        return True
        return False

    def is_checkmate(self, color):
        # Verifica si el jugador está en jaque mate
        if not self.is_king_in_check(color):
            return False

        for piece_key, positions in self.current_positions.items():
            if piece_key.endswith(color):
                for pos in positions:
                    piece_type = piece_key.split("_")[0]
                    piece_obj = self.get_piece_object(piece_type, color)
                    legal_moves = piece_obj.get_moves(pos, self)
                    for move in legal_moves:
                        temp_board = self.copy()
                        temp_board.move_piece(piece_key, pos, move, simulate=True)
                        if not temp_board.is_king_in_check(color):
                            return False
        return True

    def copy(self):
        # Crea una copia del estado actual del tablero
        new_board = Board()
        new_board.current_positions = {k: list(v) for k, v in self.current_positions.items()}
        return new_board

    def get_piece_object(self, name, color):
        # Devuelve una instancia de clase de pieza (ej. Rook, Queen...)
        piece_classes = {
            "pawn": Pawn,
            "knight": Knight,
            "bishop": Bishop,
            "rook": Rook,
            "queen": Queen,
            "king": King,
        }
        return piece_classes[name](name, color)


def pos_to_notation(pos):
    # Convierte una posición (col, row) en notación tipo 'e4'
    files = "abcdefgh"
    return f"{files[pos[0]]}{8 - pos[1]}"

# Clase base para todas las piezas
class Piece:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def get_moves(self, pos, board, simulate=False):
        return []

# Clase para los peones
class Pawn(Piece):
    def get_moves(self, pos, board, simulate=False):
        moves = []
        direction = -1 if self.color == "w" else 1
        one_step = (pos[0], pos[1] + direction)
        if 0 <= one_step[1] <= 7 and not self.is_occupied(one_step, board):
            moves.append(one_step)
            # Movimiento inicial de dos casillas
            start_row = 6 if self.color == "w" else 1
            if pos[1] == start_row:
                two_step = (pos[0], pos[1] + 2 * direction)
                if not self.is_occupied(two_step, board):
                    moves.append(two_step)

        # Capturas diagonales
        for dx in [-1, 1]:
            target = (pos[0] + dx, pos[1] + direction)
            if 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                if self.is_enemy_piece(target, board):
                    moves.append(target)
        return moves

    def is_occupied(self, pos, board):
        return any(pos in positions for positions in board.current_positions.values())

    def is_enemy_piece(self, pos, board):
        for piece_key, positions in board.current_positions.items():
            if pos in positions and not piece_key.endswith(self.color):
                return True
        return False

# Clase para los caballos
class Knight(Piece):
    def get_moves(self, pos, board, simulate=False):
        moves = []
        deltas = [
            (1, 2), (2, 1), (2, -1), (1, -2),
            (-1, -2), (-2, -1), (-2, 1), (-1, 2)
        ]
        for dx, dy in deltas:
            x, y = pos[0] + dx, pos[1] + dy
            if 0 <= x <= 7 and 0 <= y <= 7:
                if not self.is_friendly_piece((x, y), board):
                    moves.append((x, y))
        return moves

    def is_friendly_piece(self, pos, board):
        for piece_key, positions in board.current_positions.items():
            if pos in positions and piece_key.endswith(self.color):
                return True
        return False

# Clase para los alfiles
class Bishop(Piece):
    def get_moves(self, pos, board, simulate=False):
        return self.get_sliding_moves(pos, board, [(1, 1), (1, -1), (-1, 1), (-1, -1)])

    def get_sliding_moves(self, pos, board, directions):
        moves = []
        for dx, dy in directions:
            x, y = pos
            while True:
                x += dx
                y += dy
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if self.is_friendly_piece((x, y), board):
                        break
                    moves.append((x, y))
                    if self.is_enemy_piece((x, y), board):
                        break
                else:
                    break
        return moves

    def is_friendly_piece(self, pos, board):
        for piece_key, positions in board.current_positions.items():
            if pos in positions and piece_key.endswith(self.color):
                return True
        return False

    def is_enemy_piece(self, pos, board):
        for piece_key, positions in board.current_positions.items():
            if pos in positions and not piece_key.endswith(self.color):
                return True
        return False

# Clase para las torres(hereda la lógica del alfil pero cambia las direcciones)
class Rook(Bishop):
    def get_moves(self, pos, board, simulate=False):
        return self.get_sliding_moves(pos, board, [(0, 1), (1, 0), (0, -1), (-1, 0)])

# Clase para la reina (combinación de torre y alfil)
class Queen(Bishop):
    def get_moves(self, pos, board, simulate=False):
        return self.get_sliding_moves(
            pos,
            board,
            [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0)]
        )

# Clase para el rey
class King(Piece):
    def get_moves(self, pos, board, simulate=False):
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x, y = pos[0] + dx, pos[1] + dy
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if not self.is_friendly_piece((x, y), board):
                        moves.append((x, y))
        return moves

    def is_friendly_piece(self, pos, board):
        for piece_key, positions in board.current_positions.items():
            if pos in positions and piece_key.endswith(self.color):
                return True
        return False

