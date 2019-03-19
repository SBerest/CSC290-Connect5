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
button_color = (199, 154, 95)
button_select_color =(184, 155, 118)
title_color = (254, 254, 254)
tile_pos = []
# Initializing the window.
game_menu = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Connect 5')
clock = pygame.time.Clock()

# Loading in the pictures for the menu.
background_image = pygame.image.load("assets/background_image.jpg")
background_blur = pygame.image.load("assets/background_blur.jpg")
instructions_image = pygame.image.load("assets/instructions.jpg")
game_picture = pygame.image.load("assets/gameboard.png")
black_tile = pygame.image.load("assets/Black.png")
white_tile = pygame.image.load("assets/White.png")
black_ghost = pygame.image.load("assets/Black_trans.png")
white_ghost = pygame.image.load("assets/White_trans.png")

def title_display(text):
    """
    Setting up the title for the game menu.

    @param text: title of the game
    @return: None
    """
    font = pygame.font.SysFont('Haettenschweiler', 125)
    title = font.render(text, True, title_color)
    game_menu.blit(title, (150,25))

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
            pygame.draw.rect(game_menu, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(game_menu, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Open Sans', 25)
            text = font.render(self.text, True, white)
            game_menu.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

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

def draw_main_menu():
    """
    Used within the game loop, the buttons, title, and images will constantly be redrawn until the loop exits.
    returns None.
    """
    game_menu.fill((255, 255, 255))
    game_menu.blit(background_image, [0, 0])
    game_menu.blit(game_picture, [0,200])
    game_menu.blit(game_picture, [485, 200])
    title_display('Connect Five')
    single_player_button.draw(game_menu, (0, 0, 0))
    pvp_button.draw(game_menu, (0, 0, 0))
    exit_button.draw(game_menu, (0, 0, 0))
    help_button.draw(game_menu, (0, 0, 0))

    
def draw_help_screen():
    '''
    Draws the help screen
    '''
    game_menu.fill((255, 255, 255))
    game_menu.blit(background_image, [0, 0])
    game_menu.blit(instructions_image, [50,200])
    title_display('Instructions')
    back_button.draw(game_menu, (0, 0, 0))
    
    
    
def draw_board():
    '''
    draws the board for both PvP and Vs Ai
    '''
    game_menu.fill((255,255,255))
    game_menu.blit(background_blur,[0,0])
    back_button.draw(game_menu, (0, 0, 0))
    myfont = pygame.font.SysFont('Time New Roman', 20)
    
    #If the mouse is near the grid draw the preview of where it's placed
    if hover_pos != (-1,-1):
        game_menu.blit(white_ghost,(hover_pos))
    
    #Draw all tiles already placed
    for tile in tile_pos:
        game_menu.blit(white_tile,(tile[0]-13,tile[1]-13))
    
    #If any tiles are placed print out the position of the most recently placed one
    if len(tile_pos) > 0:
        tile = tile_pos[len(tile_pos)-1]

        click_x = (tile[0]-60)//30
        click_y = (tile[1]-60)//30
        
        coordinates = "["+str(click_x)+","+str(click_y)+"]"
        textsurface = myfont.render(coordinates, False, (0, 0, 0))
        game_menu.blit(textsurface,(600,500))
    
    
is_crashed = False
single_player_button = button(button_color, 300, 200, 200, 75, 'Single Player')
pvp_button = button(button_color, 300, 300, 200, 75, 'PVP Mode')
exit_button = button(button_color, 300, 500, 200, 75, 'Exit')
help_button = button(button_color, 300, 400, 200, 75, 'Instructions')
back_button = button(button_color, 695, 560, 100, 35, 'Back')
mode = 0
hover_pos = (-1,-1)


#The display logic
while not is_crashed:
    if mode == 0: #On the main menu
        pygame.display.set_caption('Connect Five')
        draw_main_menu()
        pygame.display.update()
        clock.tick(60)  # Frames per second.
        
        for event in pygame.event.get():  # Creates a list of events that the user does with cursor.
            coord = pygame.mouse.get_pos()  # Grabs the position of the mouse.
            if event.type == pygame.QUIT:
                crashed = True
                pygame.quit()
                quit()

            #On mouse release
            if event.type == pygame.MOUSEBUTTONUP:
                if single_player_button.hover(coord):
                    print('Player chooses Single Player mode.')
                    pass
                elif pvp_button.hover(coord):
                    mode = 2
                    print('Player chooses PVP mode.')
                    #multi_player
                elif help_button.hover(coord):
                    print('Help menu.')
                    mode = 1
                elif exit_button.hover(coord):
                    print('Player chooses to exit.')
                    pygame.quit()
                    quit()

            #On mouse movement
            if event.type == pygame.MOUSEMOTION:
                #change colour for responsivness
                if single_player_button.hover(coord):
                    single_player_button.color = button_select_color
                elif pvp_button.hover(coord):
                    pvp_button.color = button_select_color
                elif exit_button.hover(coord):
                    exit_button.color = button_select_color
                elif help_button.hover(coord):
                    help_button.color = button_select_color
                else:
                    single_player_button.color = button_color
                    pvp_button.color = button_color
                    exit_button.color = button_color
                    help_button.color = button_color

            print(event)
    
    #instruction screen
    if mode == 1:
        pygame.display.set_caption('How to play.')
        draw_help_screen()
        pygame.display.update()
        clock.tick(60)  # Frames per second.        
        for event in pygame.event.get():  # Creates a list of events that the user does with cursor.

            coord = pygame.mouse.get_pos()  # Grabs the position of the mouse.

            if event.type == pygame.QUIT:
                crashed = True
                pygame.quit()
                quit()
            #back to main menu
            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.hover(coord):
                    mode = 0
                    
            if event.type == pygame.MOUSEMOTION:
                if back_button.hover(coord):
                    back_button.color = button_select_color
                else:
                    back_button.color = button_color
    
    #Player versus Player screen
    if mode == 2:
        pygame.display.set_caption('Versus.')
        draw_board()
        pygame.display.update()
        clock.tick(60)  # Frames per second.        
        for event in pygame.event.get():  # Creates a list of events that the user does with cursor.
            print(event)
            coord = pygame.mouse.get_pos()  # Grabs the position of the mouse.

            if event.type == pygame.QUIT:
                crashed = True
                pygame.quit()
                quit()
            
            #on mouse releae
            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.hover(coord):
                    mode = 0
                click_x = coord[0]
                click_y = coord[1]
                #If mouse is close to grid find a position snapped to the grid
                if 45 < coord[0] < 493 and 45 < coord[1] < 493:
                    if 30 > click_x: 
                        click_x = 30; 
                    click_x = click_x + 15;
                    click_x = click_x - (click_x % 30); 
                    
                    if 30 > click_y: 
                        click_y = 30; 
                    click_y = click_y + 15;
                    click_y = click_y - (click_y % 30);   
                else:
                    click_x = -1
                    click_y = -1
                #append it for printing purposes (temp)
                tile_pos.append((click_x,click_y))
                
                #change it to the index
                click_x = (click_x-60)/30
                click_y = (click_y-60)/30
                print(click_x,click_y)
                
            #on mouse movement
            if event.type == pygame.MOUSEMOTION:
                if back_button.hover(coord):
                    back_button.color = button_select_color
                else:
                    back_button.color = button_color
                #if mouse near grid find a position snapped to the grid
                #This is saved for draw_board
                if 45 < coord[0] < 493 and 45 < coord[1] < 493:
                    hov_x = coord[0]
                    hov_y = coord[1]
                    
                    if 30 > hov_x: 
                        hov_x = 30; 
                    hov_x = hov_x + 15;
                    hov_x = hov_x - (hov_x % 30); 
                    
                    if 30 > hov_y: 
                        hov_y = 30; 
                    hov_y = hov_y + 15;
                    hov_y = hov_y - (hov_y % 30); 
                    
                    hover_pos = (hov_x-13,hov_y-13)
                else:
                    hover_pos = (-1,-1)
                    