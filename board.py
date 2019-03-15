from token import Token


class GoBoard:
    """The 19x19 GoBoard on which the game is played, with 15x15 usable spaces,
    and textured by a board_skin which is set to "Brown" by default."""
    def __init__(self, size=15, board_skin="Brown") -> None:
        self.size = size
        self.spaces = [[None]*self.size]*self.size
        self.board_skin = board_skin

    def set_board_skin(self, new_skin: str) -> None:
        """Changes the current board_skin to a new_skin."""
        self.board_skin = new_skin

    def get_token(self, column: int, row: int) -> object:
        """Returns the Token at spaces[column][row] if there is one.  Otherwise
        returns None."""

        if self.is_filled(column, row):      # If spaces[column][row] has a
            return self.spaces[column][row]  # token, return the token.
        else:                                # If spaces[column][row] does not
            return None                      # have a token, return None.

    def is_filled(self, column: int, row: int) -> bool:
        """Return True if the object at spaces[column][row] is a Token.  Returns
        false otherwise."""
        return type(self.spaces[column][row]) == Token

    def set_token(self, column: int, row: int,
                  token: Token) -> bool:
        """Places token at spaces[column][row] if that space is not filled.
        Returns True if token was successfully placed and False otherwise."""
        if not self.is_filled(column, row):
            new_token = self.set_neighbours(column, row, token)
            # The above sets token's neighbours.
            self.update_neighbours(column, row, new_token)
            # The above updates the neighbours list of new_token's neighbours.

            self.spaces[column][row] = new_token  # Places new_token at
                                                  # spaces[column][row].
            return True
        return False

    def set_neighbours(self, column: int, row: int, token: Token) -> Token:
        """Takes token to be placed at spaces[column][row] and sets its
        neighbours to its immediately adjacent tokens.  Returns a new_token
        with an updated list of neighbours."""
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

    def update_neighbours(self, column: int, row: int, token: Token) -> None:
        """Takes token to be placed at spaces[column][row] and updates its
        neighbours' list of neighbours to include token."""
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
