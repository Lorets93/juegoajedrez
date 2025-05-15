import pygame
import clase_interface as win

# Constants
WIDTH, HEIGHT = 640,360  # Board size
MIN_RATIO = 1
MAX_RATIO = 2
# WHITE = (238, 238, 210) # Unused
# BLACK = (118, 150, 86) # Unused
BACKGROUND = (48, 46, 43)

# Initialize pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chess Board")

interface=win.Interface(WIN)


def main():
    global WIN, WIDTH,HEIGHT
    WIN.fill(BACKGROUND)
    run = True
    interface.draw_board()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Handle window resizing
            """
            There is a minimum resolution of 1:1, this means 
            The board adapts to window's height, while the width has no limit up to what would make the window have a resolution of 16:9
            
            """
            if event.type == pygame.VIDEORESIZE:
                WIDTH,HEIGHT = pygame.display.get_window_size()
                
                if WIDTH/HEIGHT < MIN_RATIO:
                    HEIGHT, WIDTH = max(HEIGHT,WIDTH), max(HEIGHT,WIDTH)

                if WIDTH/HEIGHT > MAX_RATIO:
                    HEIGHT, WIDTH = min(HEIGHT,WIDTH), min(HEIGHT,WIDTH)*MAX_RATIO

                WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE) # Update window size

                WIN.fill(BACKGROUND)
                interface.draw_board()
                #interface.draw_sidebar()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()