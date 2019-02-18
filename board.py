from token import Token


class GoBoard:
    """The 19x19 Board on which the game is played, with 15x15 usable spaces."""
    def __init__(self):
        self.size = 15
        self.spaces = [[None]*self.size]*self.size

    def get_piece(self, spaces: list, column: int, row: int) -> Token:
        return spaces[column][row]

    def is_filled(self, spaces: list, column: int, row: int) -> bool:
        """Return True if spaces[column][row] contains a Token."""

        return type(spaces[column][row]) == Token

    def set_piece(self, spaces: list, column: int, row: int,
                  token: Token) -> None:
        if not self.is_filled(spaces, column, row):
            new_token = token

            new_token.n_token = self.get_piece(spaces, column, row - 1)
            new_token.ne_token = self.get_piece(spaces, column + 1, row - 1)
            new_token.e_token = self.get_piece(spaces, column + 1, row)
            new_token.se_token = self.get_piece(spaces, column + 1, row + 1)
            new_token.s_token = self.get_piece(spaces, column, row + 1)
            new_token.sw_token = self.get_piece(spaces, column - 1, row + 1)
            new_token.w_token = self.get_piece(spaces, column - 1, row)
            new_token.nw_token = self.get_piece(spaces, column - 1, row - 1)

            spaces[column][row] = new_token

