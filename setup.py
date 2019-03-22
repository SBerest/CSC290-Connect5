import cx_Freeze
import os
import pygame, pygame.draw

os.environ['TCL_LIBRARY'] = r'D:\Anaconda\pkgs\python-3.7.0-hea74fb7_0\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Simon Berest\AppData\Local\Programs\Python\Python37-32\tcl\tk8.6'

executables = [cx_Freeze.Executable("connect_five.py")]
cx_Freeze.setup(
    options={"build_exe":{"packages":["pygame"],"include_files":["gomoku.ico","ai.py","board.py","button.py","player.py","undo.py","background_blur.jpg","background_image.jpg","Black.png","Black_crown.png","Black_trans.png","gameboard.png","instructions.png","sidebar.png","sidebar_ai.png","title.png","White.png","White_crown.png","White_trans.png","button_click.mp3","invalid.mp3","place_0.mp3","place_1.mp3","place_2.mp3"]}},
    description = "Connect Five for CSC290",
    icon="gomoku.ico",
    executables = executables
    )