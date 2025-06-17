import pygame
import sys

import Presenter

def main():
    pygame.init()
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 600
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Chess Game")

    clock = pygame.time.Clock()

    presenter = Presenter.ChessPresenter(win)

    running = True
    while running:
        clock.tick(60)  # 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                presenter.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if presenter.settings_open:
                    presenter.settings_open = False

        presenter.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
