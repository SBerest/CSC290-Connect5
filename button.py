import pygame, pygame.draw
from pygame.locals import *
pygame.init()
# CREDIT:
# - Tech With Tim via YouTube for help with button class.

class Button():
    ''' Creates an instance of a button on the game menu.
    '''

    def __init__(self, color, x, y, width, height, text=''):
        '''
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
        '''
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, game_menu, outline=None):
        '''
        Draws the button on the game menu.
        @param game_menu: window of the game.
        @type: window
        @param outline: creates outline of the box with the given outline colour (using RGB tuple).
        @type: tuple
        returns None.
        '''
        if outline:
            pygame.draw.rect(game_menu, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(game_menu, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Open Sans', 25)
            text = font.render(self.text, True, (255,255,255))
            game_menu.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def hover(self, coord):
        '''
        Returns true or false if the user's mouse is hovered above a specific region.
        @param coord: coord is the mouse position/tuple of (x, y) coordinates.
        @type: tuple
        returns Boolean.
        '''
        if coord[0] > self.x and coord[0] < self.x + self.width:
            if coord[1] > self.y and coord[1] < self.y + self.height:
                return True
        return False
        