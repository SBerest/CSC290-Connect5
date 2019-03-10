class Token:
    """Tokens used to play a game of Connect 5.  A Token has a player_num
    indicating which player set it, a colour, and an x_coord and y_coord
    indicating its position on a GoBoard.  It also has neighbours immediately
    adjacent to it vertically, horizontally, and diagonally, all initially set
    to None."""
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
