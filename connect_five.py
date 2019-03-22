import pygame, pygame.draw
import sys

#import the objects used
from board import GoBoard
from board import Token
from button import Button
from undo import Board_History
from ai import AI

import random #for random.randint
from pygame.locals import *

pygame.init()

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
background_image = pygame.image.load('background_image.jpg')
background_blur = pygame.image.load('background_blur.jpg')
instructions_image = pygame.image.load('instructions.png')
game_picture = pygame.image.load('gameboard.png')
black_tile = pygame.image.load('Black.png')
white_tile = pygame.image.load('White.png')
black_crown = pygame.image.load('Black_crown.png')
white_crown = pygame.image.load('White_crown.png')
black_ghost = pygame.image.load('Black_trans.png')
white_ghost = pygame.image.load('White_trans.png')
sidebar = pygame.image.load('sidebar.png')
sidebar_ai = pygame.image.load('sidebar_ai.png')

def title_display(text):
    '''
    Setting up the title for the game menu.

    @param text: title of the game
    @return: None
    '''
    font = pygame.font.SysFont("Crimson-Roman.ttf", 125)
    title = font.render(text, True, title_color)
    game_menu.blit(title, (150,25))
    
#Global Variables
mode = 0            #The different displays
win = 0             #who won
back = 0            #which display to back button goes to
hover_pos = (-1,-1) #For the example display
start_pvp = 0       #Did pvp start
start_pva = 0       #Did pvai start
difficulty = 0      #what difficulty ai
turn = 0            #whos turn is it
timer = 0           #delay for AI
board = GoBoard()   #The board the game is played on
win_sequence = []   #The sequence of the winning tiles
Ai = None           #The Ai object
board_history = None#The board history object
last_black = None   #Location of the latest black tile
last_white = None   #Location of the latest white tile
is_crashed = False  #Did the program crash

def init_pvp():
    #Initiates the pvp objects and variables
    global board
    global board_history
    global start_pva
    global start_pvp
    global turn
    global win
    global win_sequence
    
    board = GoBoard(15)
    board_history = Board_History()
    start_pva = 0
    start_pvp = 1
    turn = 0
    win = 0
    win_sequence = []
    
def reset_pvp():
    #resets the pvp objects and variables
    global board
    global board_history
    global last_black
    global last_white
    global start_pvp
    global turn
    global win
    global win_sequence
    
    board = GoBoard(15)
    board_history = Board_History()
    last_black = None
    last_white = None
    start_pvp = 1
    turn = 0
    win = 0
    win_sequence = []
    

def kill_pvp():
    #sets the pvp objects and variables to 0/none
    global board
    global last_black
    global last_white
    global start_pvp
    global turn
    global win
    
    board = None
    last_black = None
    last_white = None
    start_pvp = 0
    turn = 0
    win = 0
    
def init_pva(difficulty):
    #Initiates the pva objects and variables
    global Ai
    global board
    global board_history
    global turn
    global start_pva
    global start_pvp
    global timer
    global win
    global win_sequence
    
    board = GoBoard()
    board_history = Board_History()
    start_pva = 1
    start_pvp = 0
    Ai = AI(difficulty)  
    timer = 0
    turn = 0
    win = 0
    win_sequence = []
    
def reset_pva():
    #resets the pva objects and variables
    global Ai
    global board
    global board_history
    global last_black
    global last_white
    global start_pvp
    global timer
    global turn
    global win
    global win_sequence
    
    Ai = AI(difficulty)  
    board = GoBoard()
    board_history = Board_History()
    last_black = None
    last_white = None
    start_pva = 1
    timer = 0
    turn = 0
    win = 0
    win_sequence = []
    
def kill_pva():
    #sets the pva objects and the variables to 0/None
    global Ai
    global board
    global difficulty
    global last_black
    global last_white
    global start_pva
    global timer
    global turn
    global win

    Ai = None
    board = None
    difficulty = 0
    last_black = None
    last_white = None
    start_pva = 0
    timer = 0
    win = 0
    turn = 0
    
def undo():
    '''
    Gets a previous board taken from the board history object.
    '''
    global board
    global last_black
    global last_white
    global turn
    global win
    
    #Change turns if there is a board to switch to (not the empty board)
    if(len(board.tokens_placed) > 0):
        change_turn()
        
    board = board_history.undo(board,1)
    
    #resets last_black and last_white
    if(len(board.tokens_placed) > 1):
        if turn == 0:
            last_white = board.tokens_placed[len(board.tokens_placed)-1]
            last_black = board.tokens_placed[len(board.tokens_placed)-2]
                
        else:
            last_black = board.tokens_placed[len(board.tokens_placed)-1]
            last_white = board.tokens_placed[len(board.tokens_placed)-2]
    else:
        if turn == 0:
            last_white = None
            last_black = None
        else:
            last_white = None
            last_black = board.tokens_placed[0]
            
def undo_ai():
    '''
    Gets the board 2 turns ago so that it's the players turn again
    '''
    global board
    global last_black
    global last_white
    global turn
    global win
        
    #Undos the players previous move
    board = board_history.undo(board,2)
    
    #resets last_black and last_white
    if(len(board.tokens_placed) > 1):
        if turn == 0:
            last_white = board.tokens_placed[len(board.tokens_placed)-1]
            last_black = board.tokens_placed[len(board.tokens_placed)-2]
                
        else:
            last_black = board.tokens_placed[len(board.tokens_placed)-1]
            last_white = board.tokens_placed[len(board.tokens_placed)-2]
    else:
        if turn == 0:
            last_white = None
            last_black = None
        else:
            last_white = None
            last_black = board.tokens_placed[0]
            
            
def draw_main_menu():
    '''
    Used within the game loop, the buttons, title, and images will constantly be redrawn until the loop exits.
    '''
    game_menu.fill((255, 255, 255))
    game_menu.blit(background_image, [0, 0])
    game_menu.blit(game_picture, [0,200])
    game_menu.blit(game_picture, [485, 200])
    title_display('Connect Five')
    
    single_player_button.draw(game_menu, (0, 0, 0))
    easy_button.draw(game_menu,(0,0,0))
    med_button.draw(game_menu,(0,0,0))
    hard_button.draw(game_menu,(0,0,0))
    
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
    global win_sequence
    
    game_menu.fill((255,255,255))
    game_menu.blit(background_blur,[0,0])
    
    reset_button.draw(game_menu, (0, 0, 0))
    play_help_button.draw(game_menu, (0, 0, 0))
    undo_button.draw(game_menu, (0, 0, 0))
    back_button.draw(game_menu, (0, 0, 0))
    
    #Turn indicator
    if win == 0:
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
    
    #choose which sidebar to use
    if Ai == None:
        game_menu.blit(sidebar,[0,0])
    else:
        game_menu.blit(sidebar_ai,[0,0])
    
    #Draw all tiles already placed
    if board != None:
        for tile in board.tokens_placed:
            if tile.colour == 'white':
                game_menu.blit(white_tile,((tile.x*30)+46,(tile.y*30)+46))
            elif tile.colour == 'black':
                game_menu.blit(black_tile,((tile.x*30)+46,(tile.y*30)+46))  
    
    myfont = pygame.font.SysFont('Crimson-Roman.ttf', 50)
    if win == 1:
        game_menu.blit(black_crown,[540,134])
        if win_sequence != []:
            for tile in win_sequence:
                game_menu.blit(black_crown,((tile[0]*30)+46,(tile[1]*30)+46))  
        pygame.draw.rect(game_menu, (0, 0, 0), (60, 500, 200, 80), 0)
        textsurface = myfont.render('P1 Victory', False, (255,255, 255))
        game_menu.blit(textsurface,(75,520))
    
    if win == 2 and Ai == None:
        game_menu.blit(white_crown,[540,194])
        if win_sequence != []:
            for tile in win_sequence:
                game_menu.blit(white_crown,((tile[0]*30)+46,(tile[1]*30)+46))  
        pygame.draw.rect(game_menu, (255, 255, 255), (280, 500, 200, 80), 0)
        pygame.draw.rect(game_menu, (0, 0, 0), (280, 500, 200, 80), 2)
        textsurface = myfont.render('P2 Victory', False, (0,0,0))
        game_menu.blit(textsurface,(295,520))

    elif win == 2 and Ai != None:    
        game_menu.blit(white_crown,[540,194])
        if win_sequence != []:
            for tile in win_sequence:
                game_menu.blit(white_crown,((tile[0]*30)+46,(tile[1]*30)+46))  
        pygame.draw.rect(game_menu, (255, 255, 255), (280, 500, 200, 80), 0)
        pygame.draw.rect(game_menu, (0, 0, 0), (280, 500, 200, 80), 2)
        textsurface = myfont.render('AI Victory', False, (0,0,0))
        game_menu.blit(textsurface,(297,520))

    coord_font = pygame.font.SysFont('Crimson-Roman.ttf', 65)
    #If black tiles are placed print out the coordinates of the latest one
    if last_black != None:
        coordinates = str(last_black.x)+','+str(last_black.y)
        textsurface = coord_font.render(coordinates, False, (161, 148, 122))
        outline = coord_font.render(coordinates, False, (0, 0, 0))
        
        #creates a black outline around textsurface
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
        
    #If white tiles are placed print out the coordinates of the latest one
    if last_white != None:
        coordinates = str(last_white.x)+','+str(last_white.y)
        textsurface = coord_font.render(coordinates, False, (161, 148, 122))
        outline = coord_font.render(coordinates, False, (0, 0, 0))
        
        #creates a black outline around textsurface
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
    
#initializing buttons on main menu  
single_player_button = Button(button_color, 300, 200, 200, 33, 'Single Player')
easy_button = Button(button_color, 300, 233, 66, 32, 'Easy')
med_button = Button(button_color, 366, 233, 67, 32, 'Medium')
hard_button = Button(button_color, 434, 233, 66, 32, 'Hard')
pvp_button = Button(button_color, 300, 300, 200, 75, 'PVP Mode')
exit_button = Button(button_color, 300, 500, 200, 75, 'Exit')
help_button = Button(button_color, 300, 400, 200, 75, 'Instructions')

#initializing buttons during play
reset_button = Button(button_color, 575, 300, 150, 35, 'Reset')
undo_button = Button(button_color, 575, 350, 150, 35, 'Undo')
play_help_button = Button(button_color, 575, 400, 150, 35, 'Instructions')
back_button = Button(button_color, 575, 450, 150, 35, 'Back')

def get_colour():
    '''
        returns black if turn == 0, white otherwise
    '''
    if turn == 0:
        return 'black'
    else:
        return 'white'
        
def change_turn():
    """
        switches the turn between 1 and 0 when called
    """
    global turn
    if turn == 0:
        turn = 1
    else:
        turn = 0

def check_win():
    """
        checks if in a given set of 5 tiles there are 5 of a single
        players token. It does this by iterating over the horizontals, 
        the verticals and both diagonals. As it checks the squares it
        saves a sequence of the 5 most recent squares, reseting when
        it goes to a new line. Then it checks if the sequence is all 1s
        or all 2s.
    """
    global win
    global win_sequence
    board_list = board.get_board_list()
    
    #Horizontal checking
    for x in range(len(board_list[0])):
        sequence = []
        for y in range(len(board_list[1])):
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            if sequence == [1,1,1,1,1]:
                win_sequence = [[x,y],[x,y-1],[x,y-2],[x,y-3],[x,y-4]]
                win = 1
                return True
            elif sequence == [2,2,2,2,2]:
                win_sequence = [[x,y],[x,y-1],[x,y-2],[x,y-3],[x,y-4]]
                win = 2
                return True
                
    #Vertical checking
    for y in range(len(board_list[1])):
        sequence = []
        for x in range(len(board_list[0])):
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            if sequence == [1,1,1,1,1]:
                win_sequence = [[x,y],[x-1,y],[x-2,y],[x-3,y],[x-4,y]]
                win = 1
                return True
            elif sequence == [2,2,2,2,2]:
                win_sequence = [[x,y],[x-1,y],[x-2,y],[x-3,y],[x-4,y]]
                win = 2
                return True
                
    
    #[/] Diagonal Checks along top of board
    for y_start in range(4, len(board_list[1])):
        sequence = []
        x = 0
        y = y_start
        while y >= 0:
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            if sequence == [1,1,1,1,1]:
                win_sequence = [[x,y],[x-1,y+1],[x-2,y+2],[x-3,y+3],[x-4,y+4]]
                win = 1
                return True
            elif sequence == [2,2,2,2,2]:
                win_sequence = [[x,y],[x-1,y+1],[x-2,y+2],[x-3,y+3],[x-4,y+4]]
                win = 2
                return True
            x+=1
            y-=1
            
    #[/] Diagonal Checks along right of board
    for x_start in range(1,len(board_list[0])-4):
        sequence = []
        x = x_start
        y = len(board_list[1])-1
        while x <= len(board_list[0])-1:
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            if sequence == [1,1,1,1,1]:
                win_sequence = [[x,y],[x-1,y+1],[x-2,y+2],[x-3,y+3],[x-4,y+4]]
                win = 1
                return True
            elif sequence == [2,2,2,2,2]:
                win_sequence = [[x,y],[x-1,y+1],[x-2,y+2],[x-3,y+3],[x-4,y+4]]
                win = 2
                return True
            x+=1
            y-=1
        
    #[\] Diagonal Checks along bottom of board
    for y_start in range(4, len(board_list[1])):
        sequence = []
        x = len(board_list[0])-1
        y = y_start
        while y >= 0:
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            if sequence == [1,1,1,1,1]:
                win_sequence = [[x,y],[x+1,y+1],[x+2,y+2],[x+3,y+3],[x+4,y+4]]
                win = 1
                return True
            elif sequence == [2,2,2,2,2]:
                win_sequence = [[x,y],[x+1,y+1],[x+2,y+2],[x+3,y+3],[x+4,y+4]]
                win = 2
                return True
            x-=1
            y-=1
            
    #[\] Diagonal Checks along right of board
    for x_start in range(len(board_list[0])-2,3,-1):
        sequence = []
        x = x_start
        y = len(board_list[1])-1
        while x >= 0:
            sequence.append(board_list[x][y])
            if len(sequence) == 6:
                sequence.pop(0)
            if sequence == [1,1,1,1,1]:
                win_sequence = [[x,y],[x+1,y+1],[x+2,y+2],[x+3,y+3],[x+4,y+4]]
                win = 1
                return True
            elif sequence == [2,2,2,2,2]:
                win_sequence = [[x,y],[x+1,y+1],[x+2,y+2],[x+3,y+3],[x+4,y+4]]
                win = 2
                return True
            x-=1
            y-=1
            
    return [-1,-1]

def main_menu():
    '''
    Main Menu game logic
    This runs the main_menu drawer as well as the logic for all the buttons.
    '''
    global difficulty
    global mode
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
                pygame.mixer.music.load('invalid.mp3')
                pygame.mixer.music.play(0)
            elif easy_button.hover(coord):
                mode = 3
                difficulty = 0
            elif med_button.hover(coord):
                mode = 3
                difficulty = 1
            elif hard_button.hover(coord):
                mode = 3
                difficulty = 2
            elif pvp_button.hover(coord):
                mode = 2
            elif help_button.hover(coord):
                back = 0
                mode = 1
            elif exit_button.hover(coord):
                pygame.quit()
                quit()

        #On mouse movement
        if event.type == pygame.MOUSEMOTION:
            #change colour for responsivness
            if pvp_button.hover(coord):
                pvp_button.color = button_select_color
                exit_button.color = button_color
                help_button.color = button_color
            elif exit_button.hover(coord):
                exit_button.color = button_select_color
                pvp_button.color = button_color
                help_button.color = button_color
            elif help_button.hover(coord):
                help_button.color = button_select_color
                pvp_button.color = button_color
                exit_button.color = button_color
            elif easy_button.hover(coord):
                easy_button.color = button_select_color
                pvp_button.color = button_color
                exit_button.color = button_color
                help_button.color = button_color
                med_button.color = button_color
                hard_button.color = button_color
            elif med_button.hover(coord):
                med_button.color = button_select_color
                pvp_button.color = button_color
                exit_button.color = button_color
                help_button.color = button_color
                easy_button.color = button_color
                hard_button.color = button_color
            elif hard_button.hover(coord):
                hard_button.color = button_select_color
                pvp_button.color = button_color
                exit_button.color = button_color
                help_button.color = button_color
                easy_button.color = button_color
                med_button.color = button_color
            else:
                pvp_button.color = button_color
                exit_button.color = button_color
                help_button.color = button_color
                easy_button.color = button_color
                med_button.color = button_color
                hard_button.color = button_color

def instructions():
    '''
    Instructions screen logic
    This runs the instruction drawer as well as the logic for all the the back button.    
    '''
    global mode
    
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

def p_verse_p():
    """
    Game logic for the pvp mode, also the logic for the buttons
    and board for displaying.
    """
    global back
    global board
    global hover_pos
    global last_black
    global last_white
    global mode
    global start_pvp
    global win
    
    if start_pvp == 0:
        init_pvp()
    start_pvp = 1
    pygame.display.set_caption('Versus a Friend.')
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
                if win == 0:
                    undo()
                    draw_board()
            elif play_help_button.hover(coord):
                back = 2
                mode = 1
            elif back_button.hover(coord):
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
                if board == None:
                    board = GoBoard()
                if board.set_token(click_x,click_y,turn+1,get_colour(),board_history):
                    if turn == 0:
                        last_black = board.tokens_placed[len(board.tokens_placed)-1]
                    else:
                        last_white = board.tokens_placed[len(board.tokens_placed)-1]
                    check_win()
                    change_turn()
                    draw_board()
                    rand_int = random.randint(0,2)
                    pygame.mixer.music.load('place_'+str(rand_int)+'.mp3')
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play(0)
                else:
                    pygame.mixer.music.load('invalid.mp3')
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

def p_verse_ai():
    """
    Game logic for the pvp mode, also the logic for the buttons
    and board for displaying.
    """
    global back
    global board
    global hover_pos
    global last_black
    global last_white
    global mode
    global start_pva
    global timer
    global turn
    global win
    

    if start_pva == 0:
        init_pva(difficulty)
    start_pva = 1
    pygame.display.set_caption('Versus Ai.')
    draw_board()
    pygame.display.update()
    clock.tick(60)  # Frames per second.
    if turn == 1 and win == 0:
        timer+=1
        if timer > 15:
            timer = 0
            move = Ai.move(board)
            board.set_token(move[0],move[1],turn+1,get_colour(),board_history)
            last_white = board.tokens_placed[len(board.tokens_placed)-1]
            check_win()
            change_turn()
            draw_board()
            rand_int = random.randint(0,2)
            pygame.mixer.music.load('place_'+str(rand_int)+'.mp3')
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(0)
            
    for event in pygame.event.get():  # Creates a list of events that the user does with cursor.
        coord = pygame.mouse.get_pos()  # Grabs the position of the mouse.

        if event.type == pygame.QUIT:
            crashed = True
            pygame.quit()
            quit()
        
        #on mouse releae
        if event.type == pygame.MOUSEBUTTONUP:
            if undo_button.hover(coord):
                if win == 0:
                    undo_ai()
                    draw_board()
            elif play_help_button.hover(coord):
                back = 3
                mode = 1
            elif back_button.hover(coord):
                start_pva = 0
                kill_pva()
                mode = 0
            elif reset_button.hover(coord):
                reset_pvp()
            click_x = coord[0]
            click_y = coord[1]
            if turn == 0:
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
                    if board.set_token(click_x,click_y,turn+1,get_colour(),board_history):
                        if turn == 0:
                            last_black = board.tokens_placed[len(board.tokens_placed)-1]
                        else:
                            last_white = board.tokens_placed[len(board.tokens_placed)-1]
                        check_win()
                        change_turn()
                        draw_board()
                        rand_int = random.randint(0,2)
                        pygame.mixer.music.load('place_'+str(rand_int)+'.mp3')
                        pygame.mixer.music.set_volume(1.0)
                        pygame.mixer.music.play(0)
                    else:
                        pygame.mixer.music.load('invalid.mp3')
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
            if 45 < coord[0] < 493 and 45 < coord[1] < 493 and win == 0 and turn == 0:
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
        
                
                
#The game logic
while not is_crashed:
    #Main Menu
    if mode == 0: 
        main_menu()
    #instruction screen
    if mode == 1:
        instructions()
    #Player versus Player screen
    if mode == 2:
        p_verse_p()
    #versus ai mode
    if mode == 3:
        p_verse_ai()
