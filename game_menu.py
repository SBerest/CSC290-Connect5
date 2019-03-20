import pygame, pygame.draw
import sys
from board import GoBoard
from board import Token
from button import button
import player
import undo
import random #for random.randint
import AI
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
instructions_image = pygame.image.load("assets/instructions.png")
game_picture = pygame.image.load("assets/gameboard.png")
black_tile = pygame.image.load("assets/Black.png")
white_tile = pygame.image.load("assets/White.png")
black_ghost = pygame.image.load("assets/Black_trans.png")
white_ghost = pygame.image.load("assets/White_trans.png")
sidebar = pygame.image.load("assets/sidebar.png")

def title_display(text):
    """
    Setting up the title for the game menu.

    @param text: title of the game
    @return: None
    """
    font = pygame.font.SysFont('Haettenschweiler', 125)
    title = font.render(text, True, title_color)
    game_menu.blit(title, (150,25))

mode = 0
win = 0
back = 0
hover_pos = (-1,-1)
start_pvp = 0
ai = None
board = GoBoard()
turn = 0
last_black = None
last_white = None


def init_pvp():
    #Initiates the pvp objects
    global board
    global turn
    global start_pvp
    board = GoBoard(15)
    print("init_pvp")
    start_pvp = 1
    turn = 0
    
def reset_pvp():
    #resets the pvp objects
    global board
    global turn
    global start_pvp
    board = GoBoard(15)
    print("init_pvp")
    start_pvp = 1
    turn = 0
    

def kill_pvp():
    #Kills the pvp objects
    global board
    global turn
    global start_pvp
    global win
    win = 0
    start_pvp = 0
    print("kill_pvp")
    board = None
    turn = 0
    
def init_pva(difficulty):
    #Initiates the pva objects
    global board
    global turn
    global ai
    global start_pva
    ai = AI(difficulty)  
    print("init_pva")
    board = GoBoard()
    turn = 0
    
def kill_pva():
    global board
    global turn
    global ai
    global start_pva
    global win
    win = 0
    #Kills the pva objects
    ai = None
    print("kill_pva")
    board = None
    turn = 0
    
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
    global board
    global last_black
    global last_white
    game_menu.fill((255,255,255))
    game_menu.blit(background_blur,[0,0])
    back_button.draw(game_menu, (0, 0, 0))
    reset_button.draw(game_menu, (0, 0, 0))
    undo_button.draw(game_menu, (0, 0, 0))
    play_help_button.draw(game_menu, (0, 0, 0))
    myfont = pygame.font.SysFont('Time New Roman', 50)
    coord_font = pygame.font.SysFont('Tw Cen MT Condensed Extra Bold', 65)
    
    if turn == 0:
        game_menu.blit(black_tile,[540,134])
    else:
        game_menu.blit(white_tile,[540,194])
    
    
    #If the mouse is near the grid draw the preview of where it's placed
    if hover_pos != (-1,-1):
        if turn == 0:
            game_menu.blit(black_ghost,(hover_pos))
        else:
            game_menu.blit(white_ghost,(hover_pos))
    
    if ai == None:
        game_menu.blit(sidebar,[0,0])
    
    #Draw all tiles already placed
    if board != None:
        for tile in board.tokens_placed:
            if tile.colour == 'white':
                game_menu.blit(white_tile,((tile.x*30)+46,(tile.y*30)+46))
            elif tile.colour == 'black':
                game_menu.blit(black_tile,((tile.x*30)+46,(tile.y*30)+46))
                
    if win == 1:
        pygame.draw.rect(game_menu, (0, 0, 0), (60, 500, 200, 80), 0)
        textsurface = myfont.render("P1 Victory", False, (255,255, 255))
        game_menu.blit(textsurface,(75,520))
    
    if win == 2:
        pygame.draw.rect(game_menu, (255, 255, 255), (280, 500, 200, 80), 0)
        pygame.draw.rect(game_menu, (0, 0, 0), (280, 500, 200, 80), 2)
        textsurface = myfont.render("P2 Victory", False, (0,0,0))
        game_menu.blit(textsurface,(295,520))

    if win == 3:    
        pygame.draw.rect(game_menu, (255, 255, 255), (280, 500, 200, 80), 0)
        pygame.draw.rect(game_menu, (0, 0, 0), (280, 500, 200, 80), 2)
        textsurface = myfont.render("AI Victory", False, (0,0,0))
        game_menu.blit(textsurface,(297,520))

    #If black tiles are placed print out the coordinates of the last one
    if last_black != None:
        coordinates = str(last_black.x)+","+str(last_black.y)
        textsurface = coord_font.render(coordinates, False, (161, 148, 122))
        outline = coord_font.render(coordinates, False, (0, 0, 0))
        game_menu.blit(outline,(639,124))
        game_menu.blit(outline,(639,125))
        game_menu.blit(outline,(639,126))
        game_menu.blit(outline,(640,124))
        game_menu.blit(outline,(640,125))
        game_menu.blit(outline,(640,126))
        game_menu.blit(outline,(641,124))
        game_menu.blit(outline,(641,125))
        game_menu.blit(outline,(641,126))
        game_menu.blit(textsurface,(640,125))
        
    #If white tiles are placed print out the coordinates of the last one
    if last_white != None:
        coordinates = str(last_white.x)+","+str(last_white.y)
        textsurface = coord_font.render(coordinates, False, (161, 148, 122))
        outline = coord_font.render(coordinates, False, (0, 0, 0))
        game_menu.blit(outline,(639,184))
        game_menu.blit(outline,(639,185))
        game_menu.blit(outline,(639,186))
        game_menu.blit(outline,(640,184))
        game_menu.blit(outline,(640,185))
        game_menu.blit(outline,(640,186))
        game_menu.blit(outline,(641,184))
        game_menu.blit(outline,(641,185))
        game_menu.blit(outline,(641,186))
        game_menu.blit(textsurface,(640,185))
    
    
is_crashed = False
single_player_button = button(button_color, 300, 200, 200, 75, 'Single Player')
pvp_button = button(button_color, 300, 300, 200, 75, 'PVP Mode')
exit_button = button(button_color, 300, 500, 200, 75, 'Exit')
help_button = button(button_color, 300, 400, 200, 75, 'Instructions')

reset_button = button(button_color, 575, 300, 150, 35, 'Reset')
undo_button = button(button_color, 575, 350, 150, 35, 'Undo')
play_help_button = button(button_color, 575, 400, 150, 35, 'Instructions')
back_button = button(button_color, 575, 450, 150, 35, 'Back')

def get_colour():
    if turn == 0:
        return "black"
    else:
        return "white"
        
def change_turn():
    global turn
    if turn == 0:
        turn = 1
    else:
        turn = 0

def check_win():
    #Horizontal checking\
    board_list = board.get_board_list()
    global win
    for x in range(len(board_list[0])):
        sequence = []
        for y in range(len(board_list[1])):
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 0:
                if count[1] == 5:
                    win = 1
                    return True
                elif count[2] == 5:
                    win = 2
                    return True
                
    #Vertical checking
    for y in range(len(board_list[1])):
        sequence = []
        for x in range(len(board_list[0])):
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 0:
                if count[1] == 5:
                    win = 1
                    return True
                elif count[2] == 5:
                    win = 2
                    return True
                
    
    #diagonals like /, from top right to bottom left along top
    for y_start in range(4, len(board_list[1])):
        sequence = []
        x = 0
        y = y_start
        while y >= 0:
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 0:
                if count[1] == 5:
                    win = 1
                    return True
                elif count[2] == 5:
                    win = 2
                    return True
            x+=1
            y-=1
            
    ###diagonals / , from top right to bottom left along right
    for x_start in range(1,len(board_list[0])-4):
        sequence = []
        x = x_start
        y = len(board_list[1])-1
        while x <= len(board_list[0])-1:
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 0:
                if count[1] == 5:
                    win = 1
                    return True
                elif count[2] == 5:
                    win = 2
                    return True
            x+=1
            y-=1
        
    ###diagonals \, from bottom right to top left along bottom
    for y_start in range(4, len(board_list[1])):
        sequence = []
        x = len(board_list[0])-1
        y = y_start
        while y >= 0:
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 0:
                if count[1] == 5:
                    win = 1
                    return True
                elif count[2] == 5:
                    win = 2
                    return True
            x-=1
            y-=1
            
    ###diagonals \, from bottom right to top left along right
    for x_start in range(len(board_list[0])-2,3,-1):
        sequence = []
        x = x_start
        y = len(board_list[1])-1
        while x >= 0:
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 0:
                if count[1] == 5:
                    win = 1
                    return True
                elif count[2] == 5:
                    win = 2
                    return True
            x-=1
            y-=1
    return [-1,-1]

        
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
                    back = 0
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
                    pvp_button.color = button_color
                    exit_button.color = button_color
                    help_button.color = button_color
                elif pvp_button.hover(coord):
                    pvp_button.color = button_select_color
                    single_player_button.color = button_color
                    exit_button.color = button_color
                    help_button.color = button_color
                elif exit_button.hover(coord):
                    exit_button.color = button_select_color
                    single_player_button.color = button_color
                    pvp_button.color = button_color
                    help_button.color = button_color
                elif help_button.hover(coord):
                    help_button.color = button_select_color
                    single_player_button.color = button_color
                    pvp_button.color = button_color
                    exit_button.color = button_color
                else:
                    single_player_button.color = button_color
                    pvp_button.color = button_color
                    exit_button.color = button_color
                    help_button.color = button_color

    
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
                    mode = back
                    
            if event.type == pygame.MOUSEMOTION:
                if back_button.hover(coord):
                    back_button.color = button_select_color
                else:
                    back_button.color = button_color
    
    #Player versus Player screen
    if mode == 2:
        if start_pvp == 0:
            print("init")
            init_pvp()
        start_pvp = 1
        pygame.display.set_caption('Versus.')
        draw_board()
        pygame.display.update()
        clock.tick(60)  # Frames per second.        
        for event in pygame.event.get():  # Creates a list of events that the user does with cursor.
            coord = pygame.mouse.get_pos()  # Grabs the position of the mouse.

            if event.type == pygame.QUIT:
                crashed = True
                pygame.quit()
                quit()
            
            #on mouse releae
            if event.type == pygame.MOUSEBUTTONUP:
                if undo_button.hover(coord):
                    print("Undo")
                elif play_help_button.hover(coord):
                    back = 2
                    mode = 1
                elif back_button.hover(coord):
                    start_pvp = 0
                    kill_pvp()
                    mode = 0
                elif reset_button.hover(coord):
                    reset_pvp()
                click_x = coord[0]
                click_y = coord[1]

                #If mouse is close to grid find a position snapped to the grid
                if 45 < coord[0] < 493 and 45 < coord[1] < 493 and win == 0:
                    if 30 > click_x: 
                        click_x = 30; 
                    click_x = click_x + 15;
                    click_x = click_x - (click_x % 30); 
                    
                    if 30 > click_y: 
                        click_y = 30; 
                    click_y = click_y + 15;
                    click_y = click_y - (click_y % 30);
                    
                    #play 
                    
                    #change it to the index
                    click_x = (click_x-60)//30
                    click_y = (click_y-60)//30
                else:
                    click_x = -1
                    click_y = -1
                    
                if click_x != -1 and click_y != -1:
                    if board.set_token(click_x,click_y,turn+1,get_colour()):
                        if turn == 0:
                            last_black = board.tokens_placed[len(board.tokens_placed)-1]
                            print(last_black.x,last_black.y)
                        else:
                            last_white = board.tokens_placed[len(board.tokens_placed)-1]
                        draw_board()
                        check_win()
                        change_turn()
                        rand_int = random.randint(0,2)
                        pygame.mixer.music.load('sounds/place_'+str(rand_int)+'.mp3')
                        pygame.mixer.music.set_volume(1.0)
                        pygame.mixer.music.play(0)
                    else:
                        pygame.mixer.music.load('sounds/invalid.mp3')
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(0)
                
            #on mouse movement
            if event.type == pygame.MOUSEMOTION:
                if back_button.hover(coord):
                    back_button.color = button_select_color
                    play_help_button.color = button_color
                    undo_button.color = button_color
                    reset_button.color = button_color
                elif undo_button.hover(coord):
                    undo_button.color = button_select_color
                    back_button.color = button_color
                    play_help_button.color = button_color
                    reset_button.color = button_color
                elif play_help_button.hover(coord):
                    play_help_button.color = button_select_color
                    back_button.color = button_color
                    undo_button.color = button_color
                    reset_button.color = button_color
                elif reset_button.hover(coord):
                    reset_button.color = button_select_color
                    back_button.color = button_color
                    play_help_button.color = button_color
                    undo_button.color = button_color
                else:
                    back_button.color = button_color
                    play_help_button.color = button_color
                    undo_button.color = button_color
                    reset_button.color = button_color
                    
                #if mouse near grid find a position snapped to the grid
                #This is saved for draw_board
                if 45 < coord[0] < 493 and 45 < coord[1] < 493 and win == 0:
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
                    
