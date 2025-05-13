from gerard_clase_interface import Interface, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
import sys
import os  # Importamos os para manejar rutas de archivos

# Diccionario inicial corregido para que blancas estén abajo y negras estén arriba
def positions_to_fen(current_positions):
    board = [["" for _ in range(8)] for _ in range(8)]

    # Asigna las piezas en el tablero
    for piece, positions in current_positions.items():
        for col, row in positions:
            symbol = piece.split("_")[0][0]  # Primer carácter del nombre de la pieza (e.g., 'r' para 'rook')
            color = piece.split("_")[1]  # Color (w o b)
            board[row][col] = symbol.upper() if color == "w" else symbol.lower()

    # Construye la cadena FEN
    fen_rows = []
    for row in board:
        empty_count = 0
        row_result = ""
        for cell in row:
            if cell == "":
                empty_count += 1
            else:
                if empty_count > 0:
                    row_result += str(empty_count)
                    empty_count = 0
                row_result += cell
        if empty_count > 0:
            row_result += str(empty_count)
        fen_rows.append(row_result)

    # Une las filas con '/'
    fen_board = "/".join(fen_rows)

    # Añade información adicional (turno, enroques, etc., por ahora simulamos con valores por defecto)
    fen_full = fen_board + " w KQkq - 0 1"

    return fen_full


# Posiciones iniciales de piezas estándar con colores
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

fen = positions_to_fen(initial_positions)
print(fen)  # Visual check: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1



class ChessGame(Interface):
    def __init__(self, win):
        super().__init__(win)
        self.selected_piece = None
        self.selected_piece_pos = None
        self.current_positions = {}
        # Deep copy positions, to avoid mutable issues
        for k, v in initial_positions.items():
            self.current_positions[k] = list(v)
        self.moves_log = []  # Lista para registrar los movimientos
        self.font = pygame.font.SysFont("Arial", 22)  # Fuente para los movimientos
        self.current_turn = "w"  # Turno inicial: blancas

        # Cargar imágenes de las piezas
        self.load_piece_images()

        # Barra lateral
        self.r_margin = 0.75  # Margen derecho donde comienza la barra lateral
        self.sbar_width = 0.25  # Ancho de la barra lateral

    def load_piece_images(self):
        """
        Carga las imágenes de las piezas con base en el nuevo formato ('pawn_w.png', etc.).
        """
        pieces = ["king", "queen", "rook", "bishop", "knight", "pawn"]  # Rey, Reina, Torre, Alfil, Caballo, Peón
        colors = ["w", "b"]  # Blanco (white) y negro (black)

        self.piece_images = {}
        for piece in pieces:
            for color in colors:
                image_path = f"images/{piece}_{color}.png"  # Formato de nombres: p.ej. 'pawn_w.png'
                if os.path.exists(image_path):  # Verificar si la ruta existe
                    self.piece_images[f"{piece}_{color}"] = pygame.image.load(image_path)
                else:
                    print(f"⚠️ No se encontró la imagen: {image_path}. Esta pieza no se dibujará.")

    def get_square_under_mouse(self, pos):
        """Obtiene la celda (columna, fila) debajo del ratón."""
        board_margin = self.win.get_size()[1] * self.b_margin
        board_size = self.win.get_size()[1] * self.b_size
        square_size = board_size / 8

        x, y = pos
        col = int((x - board_margin) // square_size)
        row = int((y - board_margin) // square_size)

        if 0 <= col < 8 and 0 <= row < 8:
            return col, row
        return None

    def is_move_legal(self, piece, start_pos, end_pos):
        """
        Verifica si un movimiento dado es legal según las reglas básicas para peones y las reglas de turno.
        Para simplificar, solo valida movimientos de peones correctamente, el resto se debe extender para cumplir reglas completas.
        """
        col_start, row_start = start_pos
        col_end, row_end = end_pos

        color = piece.split("_")[1]
        piece_type = piece.split("_")[0]

        # Impedir mover si la pieza no corresponde al turno actual
        if color != self.current_turn:
            print(f"⚠️ No es el turno de las piezas {color}.")
            return False

        # Movimiento fuera del tablero
        if not (0 <= col_end < 8 and 0 <= row_end < 8):
            return False

        # Comprobar si la casilla destino tiene una pieza del mismo color (bloquea movimiento)
        for other_piece, positions in self.current_positions.items():
            if other_piece.split("_")[1] == color and end_pos in positions:
                print("⚠️ No puedes mover a una casilla ocupada por tu propia pieza.")
                return False

        # Validar para peones:
        if piece_type == "pawn":
            direction = -1 if color == "w" else 1  # Blancas se mueven hacia filas menores (arriba), negras hacia filas mayores (abajo)
            start_row = 6 if color == "w" else 1

            # Movimiento adelante simple
            if col_start == col_end and row_end == row_start + direction:
                # Verificar que la casilla está libre
                if not self.is_square_occupied(end_pos):
                    return True

            # Movimiento adelante doble desde posición inicial
            if col_start == col_end and row_start == start_row and row_end == row_start + 2 * direction:
                intermediate_square = (col_start, row_start + direction)
                if not self.is_square_occupied(end_pos) and not self.is_square_occupied(intermediate_square):
                    return True

            # Captura diagonal
            if abs(col_end - col_start) == 1 and row_end == row_start + direction:
                if self.is_square_occupied_by_opponent(end_pos, color):
                    return True

            return False  # Movimiento inválido para peón si no cumplió ninguna condición

        # Validar para otras piezas: solo permitimos movimientos de caballo (ejemplo)
        if piece_type == "knight":
            dc = abs(col_end - col_start)
            dr = abs(row_end - row_start)
            if (dc == 2 and dr == 1) or (dc == 1 and dr == 2):
                return True
            else:
                return False

        # Para simplificar, permitir movimientos sin reglas para otras piezas (pero se puede y debe extender)
        # Esto es para poder hacer prueba inicial del turno y selección
        # Se recomienda implementar las reglas para hell piezas restantes por separado

        return True

    def is_square_occupied(self, square):
        """Indica si una casilla está ocupada por cualquier pieza."""
        for positions in self.current_positions.values():
            if square in positions:
                return True
        return False

    def is_square_occupied_by_opponent(self, square, color):
        """Indica si una casilla está ocupada por una pieza del oponente."""
        opponent_color = "b" if color == "w" else "w"
        for piece, positions in self.current_positions.items():
            if piece.split("_")[1] == opponent_color and square in positions:
                return True
        return False

    def handle_click(self, pos):
        """Gestión del clic:
        - Selecciona una pieza en el primer clic.
        - Mueve la pieza con el segundo clic."""
        square = self.get_square_under_mouse(pos)

        if self.selected_piece is None:
            # Seleccionar la pieza que está en ese cuadrado
            if square:
                for piece, positions in self.current_positions.items():
                    if square in positions and piece.split("_")[1] == self.current_turn:
                        self.selected_piece = piece
                        self.selected_piece_pos = square
                        print(f"Seleccionada {piece} en {self.format_square(square)}")
                        return
            print("⚠️ No hay pieza seleccionable en esta casilla o no es tu turno.")
        else:
            # Mover la pieza seleccionada al cuadrado destino si movimiento es legal
            if square and self.is_move_legal(self.selected_piece, self.selected_piece_pos, square):
                # Detectar si captura pieza rival
                pieces_to_remove = []
                for piece, positions in self.current_positions.items():
                    if piece != self.selected_piece and square in positions:
                        pieces_to_remove.append(piece)

                # Eliminar piezas capturadas
                for piece_to_remove in pieces_to_remove:
                    self.current_positions[piece_to_remove].remove(square)
                    if not self.current_positions[piece_to_remove]:
                        del self.current_positions[piece_to_remove]

                # Mover pieza seleccionada
                if self.selected_piece_pos in self.current_positions[self.selected_piece]:
                    self.current_positions[self.selected_piece].remove(self.selected_piece_pos)
                self.current_positions[self.selected_piece].append(square)

                # Registrar movimiento en el log
                move_msg = f"{self.selected_piece.upper()} de {self.format_square(self.selected_piece_pos)} a {self.format_square(square)}"
                self.moves_log.append(move_msg)
                print("Movimiento:", move_msg)

                # Cambiar turno
                self.current_turn = "b" if self.current_turn == "w" else "w"
                print(f"Turno actual: {'Blancas' if self.current_turn == 'w' else 'Negras'}")

            else:
                print("⚠️ Movimiento ilegal o posición inválida.")

            # Reiniciar selección siempre después del intento de mover
            self.selected_piece = None
            self.selected_piece_pos = None

    def format_square(self, square):
        """Convierte un cuadrado (col, row) en notación ajedrecística (por ejemplo 'a2')."""
        col, row = square
        return f"{chr(97 + col)}{8 - row}"

    def draw_pieces(self):
        """Dibuja las piezas en el tablero."""
        board_margin = self.win.get_size()[1] * self.b_margin
        board_size = self.win.get_size()[1] * self.b_size
        square_size = board_size / 8

        for piece, positions in self.current_positions.items():
            for col, row in positions:
                image = self.piece_images.get(piece)
                if image:
                    x = col * square_size + board_margin
                    y = row * square_size + board_margin
                    image_scaled = pygame.transform.smoothscale(image, (int(square_size), int(square_size)))
                    self.win.blit(image_scaled, (x, y))
                else:
                    print(f"⚠️ Imagen no encontrada para: {piece}")

    def draw_board_guide(self):
        """Dibuja una guía con las coordenadas (a1-h8) alrededor del tablero con texto blanco."""
        board_margin = self.win.get_size()[1] * self.b_margin  # Margen del tablero
        board_size = self.win.get_size()[1] * self.b_size  # Tamaño del tablero
        square_size = board_size / 8  # Tamaño por casilla de tablero

        # Letras (a-h) en la parte superior e inferior
        columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for i, col in enumerate(columns):
            # Texto en la parte inferior
            text = self.font.render(col, True, (255, 255, 255))  # Texto en blanco
            x = i * square_size + board_margin + (square_size - text.get_width()) / 2
            y_bottom = board_margin + board_size + 5  # Ajuste debajo del tablero
            self.win.blit(text, (x, y_bottom))

            # Texto en la parte superior
            y_top = board_margin - square_size * 0.8  # Ajuste encima del tablero
            self.win.blit(text, (x, y_top))

        # Números (1-8) en los lados izquierdo y derecho
        rows = [str(i) for i in range(8, 0, -1)]  # Notación estándar de ajedrez (8 a 1)
        for i, row in enumerate(rows):
            # Texto en el lado izquierdo
            text = self.font.render(row, True, (255, 255, 255))  # Texto en blanco
            x_left = board_margin - text.get_width() - 5  # Ajuste a la izquierda del tablero
            y = i * square_size + board_margin + (square_size - text.get_height()) / 2
            self.win.blit(text, (x_left, y))

            # Texto en el lado derecho
            x_right = board_margin + board_size + 5  # Ajuste a la derecha del tablero
            self.win.blit(text, (x_right, y))

def main():
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Chess Game")
    game = ChessGame(win)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)

        game.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
