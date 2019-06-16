import attr
import numpy as np
from attr.validators import instance_of
import re


@attr.s
class Ship(object):
    """ parent class to all game pieces
    attributes: name, level, num_hits2kill, shape and num_hits."""
    name = attr.ib(validator=instance_of(str))
    level = np.random.choice(3)
    num_hits2kill = 1
    Shape = np.array([1])
    num_hits = 0

    def __reshape__(self):
        self.Shape = np.select([self.Shape == 1], [self.name])
        return self

    def kill(self, board):
        print(f"killed {self.name}")
        for row in range(board.shape[1]):
            for col in range(board.shape[2]):
                if board[self.level, row, col] == self.name:
                    board[self.level, row, col] = 0
        return board

    def hit(self, board, coordinates):
        self.num_hits += 1
        if self.num_hits2kill <= self.num_hits:
            return self.kill(board)
        board[coordinates[0], coordinates[1], coordinates[2]] = 0
        return board


@attr.s
class Submarine(Ship):
    level = 0
    Shape = np.array([1, 1, 1])


@attr.s
class Destroyer(Ship):
    level = 1
    num_hits2kill = 4
    Shape = np.array([1, 1, 1, 1])


@attr.s
class Jet(Ship):
    level = 2
    Shape = np.array([[0, 1, 0, 0], [1, 1, 1, 1], [0, 1, 0, 0]])


@attr.s
class Game(object):
    """ this class defines the boards and the conditions to winning.
    inner methods: create_board, create_ships, place_ship, show, hit and game_over"""

    board_shape = attr.ib(default=(4, 4, 3), validator=instance_of(tuple))
    num_submarine = attr.ib(default=1, validator=instance_of(int))
    num_destroyer = attr.ib(default=1, validator=instance_of(int))
    num_jet = attr.ib(default=1, validator=instance_of(int))

    def create_ships(self):
        general = Ship('general')
        general = general.__reshape__()
        submarine = []
        destroyer = []
        jet = []
        for create_submarine in range(self.num_submarine):
            name = "submarine" + str(create_submarine)
            sub = Submarine(name)
            sub.__reshape__()
            submarine.append(sub)
        for create_destroyer in range(self.num_destroyer):
            name = "destroyer" + str(create_destroyer)
            des = Destroyer(name)
            des.__reshape__()
            destroyer.append(des)
        for create_jet in range(self.num_jet):
            name = "jet" + str(create_jet)
            jjet = Jet(name)
            jjet.__reshape__()
            jet.append(jjet)
        self.types = [submarine, destroyer, jet, [general]]
        self.status = {"submarine": self.num_submarine, "destroyer": self.num_destroyer, "jet": self.num_jet, "general": 1}
        return self

    def place_ship(self, ship_vessel):
        direction = np.random.choice(2)
        ship_shape = ship_vessel.Shape
        if direction:
            ship_shape = np.transpose(ship_shape)
        ship_size = np.shape(ship_shape)
        if len(ship_size) == 1 and direction == 0:
            ship_size = [1, ship_size[0]]
        elif len(ship_size) == 1 and direction == 1:
            ship_size = [ship_size[0], 1]
        clear = False
        while not clear:
            count = 0
            start_point = [np.random.choice(self.board_shape[1]-ship_size[0]+1),
                           np.random.choice(self.board_shape[2]-ship_size[1]+1)]
            dim0 = np.linspace(start_point[0], (start_point[0] + ship_size[0] - 1), num=ship_size[0], dtype=int)
            dim1 = np.linspace(start_point[1], (start_point[1] + ship_size[1] - 1), num=ship_size[1], dtype=int)
            try:
                for row in dim0:
                    for column in dim1:
                        if not self.board[ship_vessel.level, row, column] == 0:
                            raise IndexError
                for board_row in dim0:
                    for board_column in dim1:
                        if len(dim0) == 1:
                            self.board[ship_vessel.level, board_row, board_column] = \
                                ship_shape[board_column - start_point[1]]
                        elif len(dim1) == 1:
                            self.board[ship_vessel.level, board_row, board_column] = \
                                ship_shape[board_row - start_point[0]]
                        else:
                            self.board[ship_vessel.level, board_row, board_column] = \
                                ship_shape[board_row - start_point[0], board_column - start_point[1]]
                clear = True
            except IndexError:
                count += 1
                if count < sum(np.shape(self.board)):
                    continue
                else:
                    raise IndexError
        return self.board[ship_vessel.level, :, :]

    def create_board(self):
        self.create_ships()
        self.board = np.zeros(self.board_shape, dtype=object)
        for vessel in self.types:
            for ship_vessel in vessel:
                    ship_vessel.location = self.place_ship(ship_vessel)
        return self

    def show(self):
        print(self.board)

    def hit(self, coordinates: list):
        if self.board[coordinates[0], coordinates[1], coordinates[2]] != 0 and \
                self.board[coordinates[0], coordinates[1], coordinates[2]] != '0':
            print(f"hit {self.board[coordinates[0], coordinates[1], coordinates[2]]}")
            for category in self.types:
                for vessel in category:
                    did_hit = self.board[coordinates[0], coordinates[1], coordinates[2]] == vessel.name
                    if did_hit:
                        self.board = vessel.hit(self.board, coordinates)
                        return
        else:
            print("miss")

    def game_over(self):
        """the first win condition is if the general is hit.
        the second win condition is if all vessel besides the general have been taken down"""
        if not ["general"] in self.board:
            return True
        for check_vessels in self.types[::3]:
            for ship in check_vessels:
                if ship.name in self.board:
                    return False
        return True


def run_game():
    """ This is the method that runs the game and sub classes.
    The method asks for user input and acts on it.
    if the user input isn't recognized, the user will be asked to try again.
    currently the game is set to board size (4, 4, 3), and one of each game piece. this can be changed in this function.
    however, it should be noticed that the number of game pieces are possible given the board size."""
    board_size = (3, 4, 4)
    assert board_size[0] == 3
    num_subs = 1
    num_des = 1
    num_jets = 1
    player1 = Game(board_size, num_subs, num_des, num_jets).create_board()
    player2 = Game(board_size, num_subs, num_des, num_jets).create_board()
    print("Welcome to another game of Submarines! \n\n"
          "The shape of the board is (4, 4, 3). *notice that the coordinates referred to are inclusive-inclusive\n"
          "There is one submarine, one destroyer, one jet and one general on each players board. \n"
          "You can type 'show' to examine your board or 'quit' to exit the game prematurely. \n"
          "The pieces were set randomly. \n"
          "Win conditions: hitting the general or killing all game pieces besides the general"
          "Let's begin! \n")
    count = 1
    play = True
    while play:
        if (count % 2) == 0:
            n = 2
        else:
            n = 1
        input_string = input(f"player{n}, what coordinate are you targeting (X, Y, Z)? \n")
        numbers = re.findall(r'\d+', input_string)
        if str.lower(input_string) == "show":
            if n == 1:
                player1.show()
                continue
            player2.show()
            continue
        elif str.lower(input_string) == "quit":
            print("quitting")
            break
        elif len(numbers) == 3:
            try:
                if n == 1:
                    player2.hit([int(numbers[2])-1, int(numbers[1])-1, int(numbers[0])-1])
                else:
                    player1.hit([int(numbers[2])-1, int(numbers[1])-1, int(numbers[0])-1])
            except IndexError:
                print("the value you typed is out of bounds")
                continue
        else:
            print("typed wrong value. please try again.\n")
            continue
        # check if the game is over
        if player1.game_over():
            print("player 2 has won the game!")
            play = False
            continue
        elif player2.game_over():
            print("player 1 has won the game!")
            play = False
            continue
        count += 1


if __name__ == "__main__":
    run_game()

