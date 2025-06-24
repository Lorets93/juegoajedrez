# main.py

# Punto de entrada del juego de ajedrez. Inicializa Pygame, crea la ventana y gestiona el bucle principal.
import pygame
import sys
import Presenter

# Definimos eventos personalizados para manejar scroll desde botones en pantalla
SCROLL_UP_EVENT = pygame.USEREVENT + 1
SCROLL_DOWN_EVENT = pygame.USEREVENT + 2

def main():
    # Inicializa todos los módulos de Pygame
    pygame.init()

    # Define dimensiones iniciales de la ventana
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 600

    # Crea la ventana del juego, permitiendo que sea redimensionable
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Chess Game")

    # Reloj para mantener una tasa de fotogramas constante (FPS)
    clock = pygame.time.Clock()

    # Crea una instancia del presentador, que conecta la vista y el modelo
    presenter = Presenter.ChessPresenter(win)

    # Bucle principal del juego
    running = True
    while running:
        # Limita la velocidad a 60 fotogramas por segundo
        clock.tick(60)

        # Manejo de todos los eventos
        for event in pygame.event.get():
            # Cierre de la ventana
            if event.type == pygame.QUIT:
                running = False

            # Click de ratón (presionado)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                presenter.handle_mouse_event(event, down=True)

            # Click de ratón (soltado)
            elif event.type == pygame.MOUSEBUTTONUP:
                presenter.handle_mouse_event(event, down=False)

            # Pulsación de teclas
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if presenter.settings_open:
                        presenter.settings_open = False  # Cierra el panel de configuración
                elif event.key == pygame.K_UP:
                    presenter.scroll_moves(-1)  # Scroll hacia arriba
                elif event.key == pygame.K_DOWN:
                    presenter.scroll_moves(1)   # Scroll hacia abajo

            # Scroll de rueda del ratón
            elif event.type == pygame.MOUSEWHEEL:
                presenter.scroll_moves(-event.y)

            # Scroll mediante botones de flechas (eventos personalizados)
            elif event.type == SCROLL_UP_EVENT:
                presenter.scroll_moves(-1)
            elif event.type == SCROLL_DOWN_EVENT:
                presenter.scroll_moves(1)

        # Actualiza pantalla y lógica desde el presentador
        presenter.update()

    # Limpieza final al salir del juego
    pygame.quit()
    sys.exit()

# Ejecuta el juego si se llama directamente este archivo
if __name__ == "__main__":
    main()
