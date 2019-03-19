import random #for random.randint

# Main simply sets up a 15x15 array representing the board.
# it initializes last_move_1/2 to 7/7 which is roughly the middle of the board.
# Easy move tries to place the piece touching it's previous piece
# main is just for testing purposes.
def test():
    
    width = 15 #setting up the board
    height = 15
    board = [[0 for x in range(width)] for y in range(height)] 
    
    last_move_1 = [-1,-1] #initializing variables
    last_move_2 = [-1,-1]
    
    board[1][1] = 1
    board[1][2] = 1
    board[1][3] = 1
    
    
    #15 times print the board
    for n in range(15):
        for direction in board:
            for square in direction:
                print(square,end = " ")
            print()
        #make an ai do an easy move then print it
        last_move_1 = hard_move(board,last_move_1)
        print("p1",last_move_1)
        board[last_move_1[0]][last_move_1[1]]= 1
        
        #make an ai do an easy move then print it
        last_move_2 = hard_move(board,last_move_2)
        print("p2",last_move_2)
        board[last_move_2[0]][last_move_2[1]]= 2
    
    #print the board one more time
    for direction in board:
        for square in direction:
            print(square,end = " ")
        print()

      
def hard_move(board,last_move):
    '''
        hard_move takes the board and it's previous move to first check if it can win or stop the opponent from winning
        then it checks for an "open three" (ex 00xxx00). If it can't do either it just does an easy move.
        @param:  
            board:      2d list of ints representing the board
            last_move:  len 2 list representing where the ai player their previous move
        @return:
            move:       len 2 list representing coordinates to play next
            
    '''  
    move = check_four_in_five(board)
    if move == [-1,-1]:
        move = check_open_three(board)
        if move == [-1,-1]:
            move = easy_move(board,last_move)
    return move
    
        

def med_move(board,last_move):
    '''
       Medium move checks if, in a given set of 5 squares there are four of a single player's tile
       then return the position of the the empty square that is not that player's.
       Otherwise return easy_move's output.
       
     @param: 
       board: 2d int list representing the board
       last_move: 2 int list representing the last move      
    @return:  
       move: 2 item list representing the next move      
    '''   
    move = check_four_in_five(board)
    if move == [-1,-1]:
        move = easy_move(board,last_move)
    return move
        

def easy_move(board,last_move):        
    '''
     easy_move takes the board and it's previous move to decide where to place it's next piece.
               It does this by looking in random adjacent squares. If it finds an empty square
               it places the tile there, if it is surrounded by tiles it finds a random empty 
               square to place it's tile.
     @param: 
       board: 2d int list representing the board
       last_move: 2 int list representing the last move
     @return: 
       move: 2 item list representing the next move
    '''
    print("Last:",last_move)
    direction_list = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]] #directions around a square
    
    if last_move == [-1,-1]:  
        last_move = [len(board[0])//2 ,len(board[1])//2] #set last move to roughly the middle of the board
        
    while True: #do while space is we wanted to use is occupied and direction_list has a direction to try.
    
        rand_num = random.randint(0,len(direction_list)-1)  #randomly chose a direction
        dir = direction_list[rand_num]
        del(direction_list[rand_num])                       #then remove it
        move = [last_move[0]+dir[0],
                last_move[1]+dir[1]]    
                
        #if move would put the tile off the board then put it on edge of board instead.
        if move[0] < 0:                 
            move[0] = 0
        if move[1] < 0:
            move[1] = 0
        if move[0] >= len(board[0]):
            move[0] = len(board[0])-1
        if move[1] >= len(board[1]):
            move[1] = len(board[1])-1
            
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
    
def check_four_in_five(board):
    '''
    check_four_in_five returns the position of an empty square in a set of 4 of one player's tile and
    one empty square. (ex 11101) returns the position of 0
    
    more in depth: as it iterates across the directions it creates a sequence of the five most recent
    squares. Saving the location of the most recent empty tile. When it finds a sequence with 1 zero and
    four of a single player's tiles it returns tht position.
    
    @param: 
        board: 2d list of ints representing the board
    @return:
        move: the position of the 0.
    '''
    #Horizontal checking
    for x in range(len(board[0])):
        move = [-1,-1]
        sequence = []
        for y in range(len(board[1])):
            sequence.append(board[x][y])
            if board[x][y] == 0:
                move = [x,y]
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 1 and (count[1] == 4 or count[2] == 4):
                return move
                
    #Vertical checking
    for y in range(len(board[1])):
        move = [-1,-1]
        sequence = []
        for x in range(len(board[0])):
            sequence.append(board[x][y])
            if board[x][y] == 0:
                move = [x,y]
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 1 and (count[1] == 4 or count[2] == 4):
                return move
                
    
    #diagonals like /, from top right to bottom left along top
    for y_start in range(4, len(board[1])):
        move = [-1,-1]
        sequence = []
        x = 0
        y = y_start
        while y >= 0:
            sequence.append(board[x][y])
            if board[x][y] == 0:
                move = [x,y]
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 1 and (count[1] == 4 or count[2] == 4):
                return move
            x+=1
            y-=1
            
    ###diagonals / , from top right to bottom left along right
    for x_start in range(1,len(board[0])-4):
        move = [-1,-1]
        sequence = []
        x = x_start
        y = len(board[1])-1
        while x <= len(board[0])-1:
            sequence.append(board[x][y])
            if board[x][y] == 0:
                move = [x,y]
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 1 and (count[1] == 4 or count[2] == 4):
                return move
            x+=1
            y-=1
        
    ###diagonals \, from bottom right to top left along bottom
    for y_start in range(4, len(board[1])):
        move = [-1,-1]
        sequence = []
        x = len(board[0])-1
        y = y_start
        while y >= 0:
            sequence.append(board[x][y])
            if board[x][y] == 0:
                move = [x,y]
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 1 and (count[1] == 4 or count[2] == 4):
                return move
            x-=1
            y-=1
            
    ###diagonals \, from bottom right to top left along right
    for x_start in range(len(board[0])-2,3,-1):
        move = [-1,-1]
        sequence = []
        x = x_start
        y = len(board[1])-1
        while x >= 0:
            sequence.append(board[x][y])
            if board[x][y] == 0:
                move = [x,y]
            if len(sequence) == 6:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 1 and (count[1] == 4 or count[2] == 4):
                return move
            x-=1
            y-=1
    return [-1,-1]

    
def check_open_three(board):
    '''
    check_open_three returns the position of an empty square in a set of 3 empty squares and 
    3 of a single players squares where one empty square is in the middle 4 squares. (ex 010110) 
    and returns the position of the middle 0.
    
    more in depth: as it iterates across the directions it creates a sequence of the six most recent
    squares. Saving the location of the most recent empty before and the empty square before that. 
    When it finds a sequence with 3 zeros and 3 of a single player's tiles it returns the position of the 0
    in the centre of the formation.
    
    @param: 
        board: 2d list of ints representing the board
    @return:
        move: the location of the middle 0.
    '''
    
    for x in range(len(board[0])):
        zero_one = [-1,-1]
        zero_two = [-1,-1]
        sequence = []
        for y in range(len(board[1])):
            sequence.append(board[x][y])
            if board[x][y] == 0:
                zero_one = zero_two
                zero_two = [x,y]
            if len(sequence) == 7:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 3 and (count[1] == 3 or count[2] == 3):
                if sequence[0] == 0 and sequence[5] == 0:
                    return zero_one
                
    #Vertical
    for y in range(len(board[1])):
        zero_one = [-1,-1]
        zero_two = [-1,-1]
        sequence = []
        for x in range(len(board[0])):
            sequence.append(board[x][y])
            if board[x][y] == 0:
                zero_one = zero_two
                zero_two = [x,y]
            if len(sequence) == 7:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 3 and (count[1] == 3 or count[2] == 3):
                if sequence[0] == 0 and sequence[5] == 0:
                    return zero_one
                
    
    #diagonals like /, from top right to bottom left along top
    for y_start in range(4, len(board[1])):
        zero_one = [-1,-1]
        zero_two = [-1,-1]
        sequence = []
        x = 0
        y = y_start
        while y >= 0:
            sequence.append(board[x][y])
            if board[x][y] == 0:
                zero_one = zero_two
                zero_two = [x,y]
            if len(sequence) == 7:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 3 and (count[1] == 3 or count[2] == 3):
                if sequence[0] == 0 and sequence[5] == 0:
                    return zero_one
            x+=1
            y-=1
            
    ###diagonals / , from top right to bottom left along right
    for x_start in range(1,len(board[0])-4):
        zero_one = [-1,-1]
        zero_two = [-1,-1]
        sequence = []
        x = x_start
        y = len(board[1])-1
        while x <= len(board[0])-1:
            sequence.append(board[x][y])
            if board[x][y] == 0:
                zero_one = zero_two
                zero_two = [x,y]
            if len(sequence) == 7:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 3 and (count[1] == 3 or count[2] == 3):
                if sequence[0] == 0 and sequence[5] == 0:
                    return zero_one
            x+=1
            y-=1
        
    ###diagonals \, from bottom right to top left along bottom
    for y_start in range(4, len(board[1])):
        zero_one = [-1,-1]
        zero_two = [-1,-1]
        sequence = []
        x = len(board[0])-1
        y = y_start
        while y >= 0:
            sequence.append(board[x][y])
            if board[x][y] == 0:
                zero_one = zero_two
                zero_two = [x,y]
            if len(sequence) == 7:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 3 and (count[1] == 3 or count[2] == 3):
                if sequence[0] == 0 and sequence[5] == 0:
                    return zero_one
            x-=1
            y-=1
            
    ###diagonals \, from bottom right to top left along right
    for x_start in range(len(board[0])-2,3,-1):
        zero_one = [-1,-1]
        zero_two = [-1,-1]
        sequence = []
        x = x_start
        y = len(board[1])-1
        while x >= 0:
            sequence.append(board[x][y])
            if board[x][y] == 0:
                zero_one = zero_two
                zero_two = [x,y]
            if len(sequence) == 7:
                sequence.pop(0)
            count = [0,0,0]
            for tile in sequence:
                count[tile]+=1
            if count[0] == 3 and (count[1] == 3 or count[2] == 3):
                if sequence[0] == 0 and sequence[5] == 0:
                    return zero_one
            x-=1
            y-=1
    return [-1,-1]


def ai_move(board, difficulty):
    '''
    Given a difficulty and a board return that level of ai move.
    
    @param:
        board: a Board object
        difficulty: an int representing the difficulty
    @return:
        move: a move given as a list 
    '''
    last_move = board.get_last_move()
    int_board = board.get_int_list()
    
    if difficulty == 0:
        return easy_move(int_board,last_move)
    elif difficulty == 1:
        return med_move(int_board,last_move)
    elif difficulty == 2:
        return hard_move(int_board,last_move)