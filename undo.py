#Stack class that keeps track of boards every turn,
#so a board from 1 turn ago can be called with undo

class Board_History:
    
    def __init__(self):
        self.boards = []

    def isEmpty(self):
        return self.boards == []

    def push(self, board):
        return self.boards.append(board)

    def pop(self):
        return self.boards.pop()

    def peek(self):
        return self.boards[len(self.boards)-1]

    def size(self):
        return len(self.boards)

#*****
#input:
#   board: 2d list representing the board
#output:
#   board: 2d list representing the board
#
#*****

def undo(board):
    if not Board_History:
        return board #in case undo is called before any moves were played
    Board_History.pop() 
