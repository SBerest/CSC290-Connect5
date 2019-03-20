#Stack class that keeps track of boards every turn,
#so a board from 1 turn ago can be called with undo
import copy 
from board import GoBoard
class Board_History:
    
    def __init__(self):
        empty_board = GoBoard()
        self.boards = [empty_board]

    def isEmpty(self):
        return self.boards == []

    def push(self, board):
        print("Push")
        return self.boards.append(copy.deepcopy(board))

    def pop(self):
        if len(self.boards) > 1:
            print(len(self.boards))
            return self.boards.pop()
        else:
            print("Only empty board left")
            return GoBoard()
    def peek(self):
        return self.boards[len(self.boards)-1]

    def size(self):
        return len(self.boards)

    #*****
    #input:
    #   board: 2d list representing the board
    #   times: the amount of times to undo (expected inputs are 1 and 2)
    #output:
    #   board: 2d list representing the board
    #
    #*****
    def undo(self,board,times):
        print("undo:",len(self.boards))
        if len(self.boards) == 0:
            return board #in case undo is called before any moves were played
        for i in range(times-1):
            print("pop")
            if len(self.boards) == 1:
                return self.pop() 
            self.pop() 
        print("pop")
        return self.pop()
