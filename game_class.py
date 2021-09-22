from random import randrange

class ship:
    def __init__(self, length):
        self.length = length
        self.direction = 0 # 0 for horizental; 1 for vertical
        self.position = [(0, 0)] * length
        self.blocks = [1] * length # A list to record each block of the ship body is hit or not.
    
    def get_hit(self, target):
        ''' One block of the ship got hit'''

        if self.direction == 0: # y1 - y0, it is the n-th block of the ship
            pos = target[1] - self.position[0][1]
        else:                   # x1 - x0
            pos = target[0] - self.position[0][0]
        self.blocks[pos] = 0
        #print(self.blocks)

    @property
    def sunk(self):
        # A ship sinks when all blocks are hit
        return not any(self.blocks)

class GameBoard:
    def __init__(self, board_size = 5):
        self.board_size = board_size
        self.board = [["O"] * board_size for i in range(board_size)]
        self.fleet = []

    def __repr__(self):
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
                direction = randrange(0, 2) # 0 for horizental; 1 for vertical
                
                if direction == 0:
                    start_pos_x = randrange(0, self.board_size)
                    start_pos_y = randrange(0, self.board_size - i)
                    pos_to_check = self.board[start_pos_x][start_pos_y:start_pos_y + i]
                else:
                    start_pos_x = randrange(0, self.board_size - i)
                    start_pos_y = randrange(0, self.board_size)
                    pos_to_check = (self.board[j][start_pos_y] for j in range(start_pos_x, start_pos_x + i))

                is_empty_pos = all(block == 'O' for block in pos_to_check)

            one_ship = ship(i)
            one_ship.direction = direction
            if direction == 0:
                one_ship.position = [(start_pos_x, y) for y in range(start_pos_y, start_pos_y + i)]
            else:
                one_ship.position = [(x, start_pos_y) for x in range(start_pos_x, start_pos_x + i)]
            
            #print(f"ship numbe {i}:")
            #print(one_ship.position)
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
        #x, y = *target
        x, y = target[0], target[1]
        if self.board[x][y] == "H":
            return True
        return False

    def update_board(self, target: tuple) -> None:
        ''' Update the game board after receiving an attack on a block
        
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

class GamePlay:

    board_size = 6
    number_of_ships = board_size - 1

    def __init__(self) -> None:
        self.my_board = GameBoard(self.board_size)
        self.opponent_board = GameBoard(self.board_size)
        self.my_board.deploy(self.number_of_ships)

    def generate_hit_target(self):
        ''' Generate a new hit target
        
        Randomly choose a coordinate, if this block was not attacked before,
        return this block.
        '''
        is_valid_target = False
        while not is_valid_target:
            x = randrange(0, self.board_size)
            y = randrange(0, self.board_size)
            target = self.game_board.board[x][y]
            if target == "O" or target == "H":
                is_valid_target = True
        return (x, y)

    def get_hit_target(self):
        ''' Take user input for the coordinate of the target.'''

        print(f"Please input the row number of your attacking target: (0 to {self.board_size - 1})")
        x = int(input())
        print(f"Please input the colume number of your attacking target: (0 to {self.board_size - 1})")
        y = int(input())
        return (x,y)

    def gen_attack_result(self, target):
        hit_result = self.my_board.update_board(target)
        if hit_result:
            print("You hit a target! I will take revenge...")
        else:
            print("Hahaha, you missed.")
        print(self.my_board)


