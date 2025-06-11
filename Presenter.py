
import pygame
import Model as m
import View

BOARD_SIZE_RATIO = 0.9
BOARD_MARGIN_RATIO = (1 - BOARD_SIZE_RATIO) / 2

class ChessPresenter:
    def __init__(self, win):
        self.win = win
        self.view = View.Interface(win)
        self.model = m.Board()

        self.current_turn = "w"
        self.selected_piece = None
        self.selected_pos = None
        self.move_log = []

        self.game_started = False

        self.class_map = {
            "pawn": m.Pawn,
            "knight": m.Knight,
            "bishop": m.Bishop,
            "rook": m.Rook,
            "queen": m.Queen,
            "king": m.King,
        }

        self.piece_objects = self.load_piece_objects()

    def load_piece_objects(self):
        objs = {}
        for piece_key in self.model.current_positions.keys():
            name, color = piece_key.split("_")
            cls = self.class_map.get(name, m.Piece)
            objs[piece_key] = cls(name, color)
        return objs

    def get_square_under_mouse(self, pos):
        board_margin = self.win.get_size()[1] * BOARD_MARGIN_RATIO
        board_size = self.win.get_size()[1] * BOARD_SIZE_RATIO
        square_size = board_size / 8
        x, y = pos
        col = int((x - board_margin) // square_size)
        row = int((y - board_margin) // square_size)
        if 0 <= col < 8 and 0 <= row < 8:
            return (col, row)
        return None

    def handle_click(self, pos):
        if self.view.start_button_rect and self.view.start_button_rect.collidepoint(pos):
            self.reset_game()
            return

        if self.view.settings_button_rect and self.view.settings_button_rect.collidepoint(pos):
            return

        if not self.game_started or self.view.game_over:
            return

        sq = self.get_square_under_mouse(pos)
        if not sq:
            self.selected_piece = None
            self.selected_pos = None
            return

        if not self.selected_piece:
            for piece_key, positions in self.model.current_positions.items():
                if sq in positions and piece_key.endswith(f"_{self.current_turn}"):
                    self.selected_piece = piece_key
                    self.selected_pos = sq
                    break
        else:
            piece_obj = self.piece_objects.get(self.selected_piece)
            if not piece_obj:
                return

            legal_moves = piece_obj.get_moves(self.selected_pos, self.model)
            if sq in legal_moves:
                start_not = m.pos_to_notation(self.selected_pos)
                end_not = m.pos_to_notation(sq)
                move_str = f"{start_not} -> {end_not}"
                self.model.move_piece(self.selected_piece, self.selected_pos, sq)
                self.move_log.append(move_str)

                # Cambiar turno primero
                self.current_turn = "b" if self.current_turn == "w" else "w"
                attacked_color = self.current_turn  # el que ahora juega, es el que ha sido atacado

                # Verificar si el rey fue comido directamente
                if self.model.game_over:
                    winner = "Blancas" if self.model.winner == "white" else "Negras"
                    self.view.display_message(f"{winner} ganan!", (255, 0, 0), duration=4000)
                    pygame.time.delay(1000)
                    self.reset_game()
                    return

                # Verificar jaque / jaque mate
                if self.model.is_king_in_check(attacked_color):
                    self.view.display_message("Jaque", (255, 0, 0), duration=1500)

                    if self.model.is_checkmate(attacked_color):
                        self.view.display_message("Jaque Mate", (255, 0, 0), duration=3000)
                        winner = "Blancas" if attacked_color == "b" else "Negras"
                        self.view.display_message(f"{winner} ganan!", (255, 0, 0), duration=4000)
                        pygame.time.delay(1000)
                        self.reset_game()
                        return

            self.selected_piece = None
            self.selected_pos = None

    def reset_game(self):
        self.model = m.Board()
        self.piece_objects = self.load_piece_objects()
        self.current_turn = "w"
        self.selected_piece = None
        self.selected_pos = None
        self.move_log.clear()
        self.view.game_over = False
        self.game_started = True

    def update(self):
        legal_moves = []
        if self.selected_piece and self.selected_pos and not self.view.game_over:
            piece_obj = self.piece_objects.get(self.selected_piece)
            if piece_obj:
                legal_moves = piece_obj.get_moves(self.selected_pos, self.model)

        if self.game_started:
            self.view.update(self.model.current_positions, legal_moves, self.move_log)
        else:
            self.view.update(self.model.initial_positions)



