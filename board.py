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
                  token: Token) -> None:
        """Places token at spaces[column][row] if that space is not filled."""
        if not self.is_filled(column, row):
            new_token = token       # Allows token to be altered before placing.
            adj_spaces_checked = 0  # Spaces immediately adjacent to the target.

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

            self.spaces[column][row] = new_token
