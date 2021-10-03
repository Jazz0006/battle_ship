from random import randrange
from random import choice


class Ship:
    """ Class of ship that be deployed on the game board

    Attribute:
        length (int): the length of the ship. 1 < length < length of the board
        direction (int): 0 for horizontal;
                         1 for vertical
        position (list of tuple): the blocks that this ship occupies
        blocks (list of int): 1 -- the block is not hit
                              0 -- the block is hit
    """

    def __init__(self, length):
        self.length = length  # The length of this ship

        self.direction = 0  # 0 for horizontal; 1 for vertical

        # The blocks that this ship occupies
        self.position = [(0, 0)] * length

        # A list to record each block of the ship body is hit or not.
        self.blocks = [1] * length

    @property
    def sunk(self):
        """A ship sinks when all blocks are hit

        1 -- if all its blocks are hit
        0 -- if any of its block is not hit
        """

        return not any(self.blocks)

    def get_hit(self, target):
        ''' Undates the ship if one block of it is hit

        Args:
            target: a tuple of the coordinate on the game board
        '''

        if self.direction == 0:
            # y1 - y0, it is the n-th block of the ship
            pos = target[1] - self.position[0][1]
        else:
            # x1 - x0
            pos = target[0] - self.position[0][0]
        # undate that block to 0, representing it is hit
        self.blocks[pos] = 0


class GameBoard:
    """ Class of the game board with battle ships on the board

    Attributes:
        board_size (int): Edge length of the game board
        board (2D array): Array of symbles of the game board.
                          'O' -- empty space
                          'H' -- ship
                          'X' -- attacked ship
                          '.' -- attacked empty space
        fleet (list of obj: Ship): list of Ship objects deployed on the board
    """

    @property
    def is_game_end(self):
        """bool: Ture if all ships in the fleet are hit """
        return all(my_ship.sunk for my_ship in self.fleet)

    def __init__(self, board_size=5):
        self.board_size = board_size
        self.board = [["O"] * board_size for i in range(board_size)]
        self.fleet = []

    def __repr__(self):
        """ presents the board as a 2-D array"""

        return "\n".join(" ".join(line) for line in self.board)

    def deploy(self, num_ship):
        ''' Randomly deploy ships onto the game board

        Args:
            num_ship: the number of the ships to be deployed.
                      1 < num_ship < board_size

        Returns:
            None
        '''

        for i in range(num_ship, 1, -1):
            # Try to find an empty space to deploy the ship
            is_empty_pos = False
            while not is_empty_pos:
                # get a random direction
                direction = randrange(0, 2)

                # get the blockes after the start position
                if direction == 0:  # The ship is horizontal
                    start_pos_x = randrange(0, self.board_size)
                    start_pos_y = randrange(0, self.board_size - i)
                    pos_to_check = self.board[start_pos_x][start_pos_y:start_pos_y + i]
                else:  # The ship is vertical
                    start_pos_x = randrange(0, self.board_size - i)
                    start_pos_y = randrange(0, self.board_size)
                    pos_to_check = (self.board[j][start_pos_y] for j
                                    in range(start_pos_x, start_pos_x + i))

                # if all the blocks are empty, the ship can be deployed
                is_empty_pos = all(block == 'O' for block in pos_to_check)

            one_ship = Ship(i)
            one_ship.direction = direction
            if direction == 0:
                one_ship.position = [(start_pos_x, y) for y
                                     in range(start_pos_y, start_pos_y + i)]
            else:
                one_ship.position = [(x, start_pos_y) for x
                                     in range(start_pos_x, start_pos_x + i)]

            self.fleet.append(one_ship)

            # Update the game board:
            for pos in one_ship.position:
                self.board[pos[0]][pos[1]] = "H"

    def check_hit(self, target: tuple) -> bool:
        ''' Check an attack is a hit or a miss

        Args:
            target: a tuple of the coordinate on the game board

        Returns:
            True if a ship is on the target;
            False if nothing is on the target.
        '''

        x, y = target[0], target[1]
        if self.board[x][y] == "H":
            return True
        return False

    def update_my_board(self, target: tuple) -> None:
        ''' Update the player's board after receiving an attack on a block

        Args:
            target: a tuple of the coordinate on the game board

        Returns:
            is_hit: True if the attack hit a ship.
        '''

        if self.check_hit(target):
            result_symble = "X"
            is_hit = True
            # Update the ship that got hit.
            for my_ship in self.fleet:
                if target in my_ship.position:
                    my_ship.get_hit(target)
        else:
            result_symble = "."
            is_hit = False
        x, y = target[0], target[1]
        self.board[x][y] = result_symble
        return is_hit

    def update_opponent_board(self, target, hit_symble):
        """Update the enemy's board after receiving attack result

        Args:
            target (tuple): the block to be updated
            hit_symble (str): the symble to write
                              'X' -- hit on a ship
                              '.' -- hit on an empty space
        """
        x, y = target[0], target[1]
        self.board[x][y] = hit_symble


class GamePlay:
    """ The overall control of one side of the game

    Attribute:
        board_size (int): The dimension of the game board
        number_of_ships (int): The number of ships that deployed on the game board

        my_board (obj: GameBoard): The game-board of my fleet
        opponent_board (obj: GameBoard): The game-board of the opponent
        unattacked_blocks (list): Hold remaining blocks that unattacked
        attacked_blocks (list): Hold all the blocks that have been manually attacked
    """

    board_size = 5
    number_of_ships = board_size - 1

    def __init__(self) -> None:
        self.my_board = GameBoard(self.board_size)
        self.opponent_board = GameBoard(self.board_size)
        self.unattacked_blocks = [(x, y) for x in range(self.board_size)
                                  for y in range(self.board_size)]
        self.attacked_blockes = [(-1, -1)]
        # Deploy ships onto my game board
        self.my_board.deploy(self.number_of_ships)

    def generate_hit_target(self):
        ''' Randomly choose one block from all unattacked blocks '''

        tgt = choice(self.unattacked_blocks)
        self.unattacked_blocks.remove(tgt)
        return tgt

    def get_hit_target(self):
        ''' Take user input for the coordinate of the target.

        Args:
            None

        Returns:
            A tuple of the coordinate on the board

        Raises:
            TypeError if the input is not an integer
        '''

        x, y = -1, -1
        while (x, y) in self.attacked_blockes:
            x, y = -1, -1
            while x < 0 or x > self.board_size:
                print(f"Please input the row number of your attacking target:")
                print(f"(0 to {self.board_size - 1})")
                try:
                    x = int(input())
                except ValueError:
                    print(f" Please input an integer between 0 and {self.board_size}")

            while y < 0 or y > self.board_size:
                print(f"Please input the colume number of your attacking target:")
                print(f"(0 to {self.board_size - 1})")
                try:
                    y = int(input())
                except ValueError:
                    print(f" Please input an integer between 0 and {self.board_size}")

            if (x, y) in self.attacked_blockes:
                print(" You have attacked this target,")
                print(" Please select another block.")
        # add the new attack address to the list of attacked blocks
        self.attacked_blockes.append((x, y))
        return (x, y)

    def gen_attack_result(self, target):
        """ Generate the result of one attack

        Args:
            target (tuple): The coordinate of the attack target

        Returns:
            True if the attack hits a ship or
            False if the attack misses all the ships
        """

        hit_result = self.my_board.update_my_board(target)
        return hit_result

    def print_board(self):
        """ Print both enemy's game board and the player's game board """

        print("Enemy's Board: ")
        print(self.opponent_board)
        print("---------------------")
        print("My Board: ")
        print(self.my_board)
