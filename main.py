
# Punto de entrada del juego de ajedrez. Inicializa Pygame, crea la ventana y gestiona el bucle principal.
import pygame
import sys

import Presenter

def main():
    # Inicializa todos los módulos de Pygame
    pygame.init()
    # Dimensiones iniciales de la ventana
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 600
    # Crea la ventana del juego y permite que sea redimensionable
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Chess Game")
    # Reloj para controlar los FPS
    clock = pygame.time.Clock()
    # Crea una instancia del presentador, que conecta la vista y el modelo
    presenter = Presenter.ChessPresenter(win)
    # Bucle principal del juego
    running = True
    while running:
        clock.tick(60)  # 60 FPS
        # Procesamiento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Cierra la ventana
            elif event.type == pygame.MOUSEBUTTONDOWN:
                presenter.handle_click(event.pos) # Llama al presentador para gestionar clics
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if presenter.settings_open:
                    presenter.settings_open = False # Cierra el panel de configuración
        # Actualiza la pantalla a través del presentador
        presenter.update()
    # Al cerrar el juego
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
