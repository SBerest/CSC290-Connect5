
class Token:
    '''Tokens used to play a game of Connect 5.  A Token has a player_num
    indicating which player set it, a colour, and an x_coord and y_coord
    indicating its position on a GoBoard.  It also has neighbours immediately
    adjacent to it vertically, horizontally, and diagonally, all initially set
    to None.'''
    def __init__(self, player_num: int, colour: str, x_coord: int, y_coord: int,
                 north=None, south=None, east=None, west=None, n_east=None,
                 s_east=None, n_west=None, s_west=None):
        self.player_num = player_num
        self.colour = colour
 
        self.x = x_coord
        self.y = y_coord

        self.neighbours = [s_west, south, s_east,  # List of self's immediately
                           west, east, n_west,     # adjacent neighbours.
                           north, n_east]

                           
class GoBoard:
    '''The 15x15 GoBoard on which the game is played, textured by a board_skin
    which is set to 'Brown' by default. The board keeps a list of all tokens
    that have been placed.'''
    def __init__(self, size=15, board_skin='Brown') -> None:
        self.tokens_placed = []
        self.size = size
        self.spaces = [None]*size
        for i in range(size):
            self.spaces[i] = [None]*size
        self.board_skin = board_skin

    def set_board_skin(self, new_skin: str) -> None:
        '''Changes the current board_skin to a new_skin.
        :rtype: None'''
        self.board_skin = new_skin

    def get_token(self, column: int, row: int) -> Token or None:
        '''Returns the Token at spaces[column][row] if there is one.  Otherwise
        returns None.
        :rtype: Token or None'''

        if self.is_filled(column, row):      # If spaces[column][row] has a
            return self.spaces[column][row]  # token, return the token.
        else:                                # If spaces[column][row] does not
            return None                      # have a token, return None.

    def is_filled(self, column: int, row: int) -> bool:
        '''Return True if the object at spaces[column][row] is a Token.  Returns
        false otherwise.
        :rtype: bool'''
        return type(self.spaces[column][row]) == Token

    def set_token(self, column: int, row: int, player_num: id, colour, board_history) -> bool:
        '''Places token at spaces[column][row] if that space is not filled.
        Returns True if token was successfully placed and False otherwise.
        :rtype: bool'''
        if not self.is_filled(column, row):
            board_history.push(self)
            token = Token(player_num, colour, column, row)
            #new_token = self.set_neighbours(column, row, token)
            # The above sets token's neighbours.
            #self.update_neighbours(column, row, new_token)
            # The above updates the neighbours list of new_token's neighbours.
            self.spaces[column][row] = token  # Places new_token at
                                                  # spaces[column][row].
            self.tokens_placed.append(token)  # Updates the list of tokens
                                                  # placed.
            return True
        return False

    def remove_token(self, token: Token) -> bool:
        '''Removes token from its space on the GoBoard.
        :rtype: bool'''
        if self.get_token(token.x, token.y) == token:
            self.update_neighbours(token.x, token.y, None)
            # The above updates the neighbours list of new_token's neighbours.

            self.spaces[token.x][token.y] = None  # Removes token from
                                                  # spaces[token.x][token.y].
            self.tokens_placed.pop(-1)            # Updates the list of tokens
                                                  # placed.
            return True
        return False
    def get_last_move(self):
        '''returns the last move of white as a list of ints
        '''
        token = self.tokens_placed[len(self.tokens_placed)-2]
        return [token.x,token.y]
    
    
    def get_board_list(self):
        '''Gives the board in list form to be easy read.
        @return: board
        '''
        board = [[0 for x in range(15)] for y in range(15)]
        for x in range(self.size):
            for y in range (self.size):
                if self.is_filled(x, y):
                    token = self.get_token(x, y)
                    board[x][y] = token.player_num
                else:
                    board[x][y] = 0
        return board

        
    def set_neighbours(self, column: int, row: int, token: Token) -> Token:
        '''Takes token to be placed at spaces[column][row] and sets its
        neighbours to its immediately adjacent tokens.  Returns a new_token
        with an updated list of neighbours.
        :rtype: Token'''
        new_token = token  # Allows token to be altered before placing.
        adj_spaces_checked = 0  # Spaces adjacent to the target checked.

        # The following nested for loop checks the spaces adjacent to
        # spaces[column][row] for neighbours.
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                # Code iterates only if the space checked is not where token
                # will be placed.
                if not ((x_offset == 0) or (y_offset == 0)):
                    new_token.neighbours[adj_spaces_checked] = \
                        self.get_token(column + x_offset, row + y_offset)
                    adj_spaces_checked += 1
                    # Adds the token at
                    # spaces[column + x_offset][row + y_offset] to token's
                    # list of neighbours and increases the
                    # adj_spaces_checked accordingly on each iteration.
        return new_token

    def update_neighbours(self, column: int, row: int, token: Token or None) \
            -> None:
        '''Takes token to be placed at spaces[column][row] and updates its
        neighbours' list of neighbours to include token.  Alternatively takes
        None as an argument and removes a Token from it's neighbours' list of
        neighbours.
        :rtype: None'''
        adj_spaces_checked = 0  # Spaces adjacent to the target checked.

        # The following nested for loop iterates through token's neighbours.
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                # Code iterates only if the space checked is not where token
                # will be placed.
                if not ((x_offset == 0) or (y_offset == 0)):
                    # Code iterates only if the space checked is filled.
                    if self.is_filled(column + x_offset, row + y_offset):
                        token.neighbours[adj_spaces_checked]. \
                            neighbours[8 - adj_spaces_checked] = token
                        # Adds token to the list of neighbours of the token at
                        # spaces[column + x_offset][row + y_offset].
                    adj_spaces_checked += 1
                    # Adjusts adj_spaces_checked accordingly on each iteration.

