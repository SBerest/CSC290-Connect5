# Player Class that contains the essentials of a player in
# connect five
class Player:

    def __init__(self, name):
        self.name = name    #Name of player
        self.turns = 0      #Number of turns by player

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_turns(self):
        return self.turns

    def set_turns(self, turns):
        self.turns = turns

# Creating the 2 players
player1 = Player("Player1")
player2 = Player("Player2")

# Declaring variables for game over and total turns taking
# throughout game
game_over = False
total_turns = 0


# Logic for switching between the players and keep track
# of turns
while not game_over:

    if total_turns%2 == 0:  # Player 1
        print("It is " + player1.get_name() + "'s turn")
        player1.set_turns(player1.get_turns() + 1)
        print("Number of turns for Player1: {}".format(player1.get_turns()))
    else:   # Player 2
        print("It is " + player2.get_name() + "'s turn")
        player2.set_turns(player2.get_turns() + 1)
        print("Number of turns for Player2: {}".format(player1.get_turns()))

    total_turns +=1
    print("Total turns: {}".format(total_turns))
