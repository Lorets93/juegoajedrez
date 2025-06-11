import pygame
import os
import sys
import Model as m
import View

# Parámetros tablero
BOARD_SIZE_RATIO = 0.9
BOARD_MARGIN_RATIO = (1 - BOARD_SIZE_RATIO) / 2

class ChessPresenter:
    def __init__(self, win):
        self.model = m.Board()
        self.view = View.Interface(win)
        self.win = win

        self.font = pygame.font.SysFont("Arial", 18)
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

        self.start_pressed = False
        self.settings_pressed = False

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
        if self.view.game_over:
            return  # No permitir más clics si el juego ha terminado

        if self.view.start_button_rect.collidepoint(pos):
            self.game_started = not self.game_started
            self.start_pressed = True
            self.reset_game()
            return
        elif self.view.settings_button_rect.collidepoint(pos):
            self.settings_pressed = True
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

            moves = piece_obj.get_moves(self.selected_pos, self.model)
            if sq in moves:
                start_not = m.pos_to_notation(self.selected_pos)
                end_not = m.pos_to_notation(sq)
                move_str = f"{start_not} -> {end_not}"
                self.model.move_piece(self.selected_piece, self.selected_pos, sq)
                self.move_log.append(move_str)

                # Cambiar turno
                self.current_turn = "b" if self.current_turn == "w" else "w"

                # Verificar jaque o jaque mate
                if self.model.is_king_in_check(self.current_turn):
                    self.view.display_message("Jaque", (255, 0, 0))
                    if self.model.is_checkmate(self.current_turn):
                        self.view.display_message("Jaque Mate", (255, 0, 0), duration=3000)
                        winner_name = "Blancas" if self.current_turn == "b" else "Negras"
                        self.view.set_game_over(winner_name)

            self.selected_piece = None
            self.selected_pos = None

    def reset_game(self):
        self.model = m.Board()
        self.piece_objects = self.load_piece_objects()
        self.current_turn = "w"
        self.move_log.clear()
        self.selected_piece = None
        self.selected_pos = None
        self.start_pressed = False
        self.settings_pressed = False
        self.view.game_over = False

    def update(self):
        legal_moves = []
        if self.selected_piece and self.selected_pos:
            piece_obj = self.piece_objects.get(self.selected_piece)
            if piece_obj:
                legal_moves = piece_obj.get_moves(self.selected_pos, self.model)
        if self.game_started:
            self.view.update(self.model.current_positions, legal_moves, self.move_log)
        else:
            self.view.update(self.model.initial_positions)
