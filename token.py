class Token:
    """Tokens to play the game with."""
    def __init__(self, player_num: int, colour: str, x_coord: int, y_coord: int,
                 north=None, south=None, east=None, west=None, n_east=None,
                 s_east=None, n_west=None, s_west=None):
        self.player_num = player_num
        self.colour = colour

        self.x = x_coord
        self.y = y_coord

        self.neighbours = {}

        self.n_token = north
        self.ne_token = n_east
        self.e_token = east
        self.se_token = s_east
        self.s_token = south
        self.sw_token = s_west
        self.w_token = west
        self.nw_token = n_west
