import pygame, pygame.draw
import sys
from pygame.locals import *
pygame.init()

# CREDIT:
# - Tech With Tim via YouTube for help with button class.

# Window dimensions
window_width = 800
window_height = 600

# Colors - using RGB values.  
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Initializing the window.
game_menu = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Connect 5')
clock = pygame.time.Clock()

class button():
    """ Creates an instance of a button on the game menu.
    """
    def __init__(self, color, x, y, width, height, text=''):
        """
        Initializes the attributes of the button.
        
        @param color: an RGB value stored in a tuple for the color of the button.
        @type color: tuple
        @param x: value given to place where the button goes lies in the x-plane within the window.
        @type x: int
        @param y: value given to place where the button goes lies in the y-plane within the window.
        @type y: int
        @param width: value to instantiate the width of the button.
        @type width: int
        @param height: value to instantiate the height of the button.
        @type height: int
        @param text: text that will go within the button.
        @type text: str

        returns None.
        """
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, game_menu, outline=None):
        """
        Draws the button on the game menu.

        @param game_menu: window of the game.
        @type: window
        @param outline: creates outline of the box with the given outline colour (using RGB tuple).
        @type: tuple

        returns None.
        """
        if outline:
            pygame.draw.rect(game_menu, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(game_menu, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('arial', 25)
            text = font.render(self.text, True, black)
            game_menu.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        
    def hover(self, coord):
        """
        Returns true or false if the user's mouse is hovered above a specific region.

        @param coord: coord is the mouse position/tuple of (x, y) coordinates.
        @type: tuple

        returns Boolean.
        """
        if coord[0] > self.x and coord[0] < self.x + self.width:
            if coord[1] > self.y and coord[1] < self.y + self.height:
                return True
        return False

def redraw_window():
    """
    Used within the game loop, the buttons will constantly be redrawn until the loop exits.

    returns None.
    """
    game_menu.fill((255, 255, 255))
    single_player_button.draw(game_menu, (0, 0, 0))
    pvp_button.draw(game_menu, (0, 0, 0))
    exit_button.draw(game_menu, (0, 0, 0))

is_crashed = False
single_player_button = button(white, 275, 100, 250, 100, 'Single Player')
pvp_button = button(white, 275, 200, 250, 100, 'PVP Mode')
exit_button = button(white, 275, 300, 250, 100, 'Exit')

while not is_crashed:
    redraw_window()
    pygame.display.update()
    clock.tick(60) # Frames per second.
    for event in pygame.event.get(): # Creates a list of events that the user does with cursor.
        
        coord = pygame.mouse.get_pos() # Grabs the position of the mouse.
        
        if event.type == pygame.QUIT:
            crashed = True
            pygame.quit()
            quit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if single_player_button.hover(coord):
                print('Player chooses Single Player mode.')
            elif pvp_button.hover(coord):
                print('Player chooses PVP mode.')
            elif exit_button.hover(coord):
                print('Player chooses to exit.')

        if event.type == pygame.MOUSEMOTION:
            if single_player_button.hover(coord):
                single_player_button.color = red
            elif pvp_button.hover(coord):
                pvp_button.color = red
            elif exit_button.hover(coord):
                exit_button.color = red
            else:
                single_player_button.color = white
                pvp_button.color = white
                exit_button.color = white
                
        print(event)
