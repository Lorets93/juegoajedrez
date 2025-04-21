import pygame

class Interface:
    def __init__(self, win):
        self.win=win

        self.b_img = pygame.image.load("images/board.png").convert_alpha() # board image
        self.b_pos = (0, 0) # tuple - board top-left corner position
        self.b_size = 0.9 # board size relative to window height (%)
        self.b_margin = (1-self.b_size)/2 # board margin to window height (%)

    def update(self):
        return




    def main_menu(self):
        return

    def game(self):

        return

    def draw_board(self):
        #defining position coords
        #b_x, b_y= self.win.get_size() # get window size (for any resizing)
        b_pos= self.win.get_size()[1]*self.b_margin # take the percentage for the margin

        #defining board size
        b_dim= self.win.get_size() # get window size (for any resizing)
        b_s = b_dim[1]*self.b_size # takes percentage of screen size, also adjusts size with ratio for it to be a square

        board = pygame.transform.scale(self.b_img, (b_s, b_s))  # actual resizing of the image, with adjusted size

        self.round_corners(board, round(self.win.get_size()[1]*0.01)) # round corners -> 1% of screen height

        self.win.blit(board, (b_pos, b_pos)) # draw the board on top-left corner coords

    def draw_sidebar(self):
        sdb_posx = self.win.get_size()[0]*9/16
        sdb_posy = self.win.get_size()[1]*self.b_margin

        sdb_dimx, sdb_dimy = self.win.get_size()
        sdb_dimx = sdb_dimx*6.5/16
        sdb_dimy = sdb_dimy*self.b_size

        sidebar=pygame.Surface((sdb_dimx, sdb_dimy), pygame.SRCALPHA)
        sidebar.fill((0, 0, 0, 256*0.4))
        self.round_corners(sidebar, round(self.win.get_size()[1]*0.01))
        self.win.blit(sidebar, (sdb_posx, sdb_posy))
    
    def round_corners(self, img, r):
         # Create a transparent mask surface
        mask = pygame.Surface(img.get_size(), pygame.SRCALPHA)

        # Draw a rounded rectangle on the mask
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=r)

        # Apply the rounded mask to the image
        img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
