
# *****
#input: 
#   board: 2d list representing the board
#   last_move: 2 item list representing the last move
#output: 
#   move: 2 item list representing the next move
#
# easy_move takes the board and it's previous move to decide where to place it's next piece.
#           It does this by randomly selecting a square in a direction (including diagonal). 
#           If that square is occupied it tries again after pruning that direction from it's
#           direction_list. If it runs out of directions to try it finds a random empty space.
# *****
def easy_move(board,last_move):
    print("Last:",last_move)
    direction_list = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]] #directions around a square
    
    if last_move == [-1,-1]: ##if check_four_in_five found no four in five set last_move to roughly the middle of the board.  
        last_move = [len(board[0])//2 ,len(board[1])//2]
        
    while True: #do while space is occupied and direction_list has a direction to try.
        rand_num = random.randint(0,len(direction_list)-1)  #randomly chose a direction
        dir = direction_list[rand_num]
        del(direction_list[rand_num])                       #then remove it
        move = [last_move[0]+dir[0],
                last_move[1]+dir[1]]    #set move to last_move+dir
        
        if move[0] < 0:                 #if move would put the tile off the board then put it on edge of board instead.
            move[0] = 0
        if move[1] < 0:
            move[1] = 0
        if move[0] >= len(board[0]):
            move[0] = len(board[0]-1)
        if move[1] >= len(board[1]):
            move[1] = len(board[1]-1)
            
        if board[move[0]][move[1]] == 0 or len(direction_list) == 0:
            break
        
    if len(direction_list) == 0: #if we run out of directions to try
        while True: #do while we have not found an empty space
            x = random.randint(0,len(board[0])-1)     #randomly select an x,y for the move in bounds of the board
            y = random.randint(0,len(board[1])-1)
            move = [x,y]    
            if board[x][y] == 0:
                break;
        
    return move