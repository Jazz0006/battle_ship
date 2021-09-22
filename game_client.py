import game_class
import socket

SERVER_IP = 127.0.0.1

my_game = game_class.GamePlay()
print("Enemy's Board: ")
print(my_game.opponent_board)
print("---------------------")
print("My Board: ")
print(my_game.my_board)

print("Connecting to the server...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((SERVER_IP, 9587))
    except Exception as e:
        print("-"*71)
        print(f" Error:  Cannot connect to host: {SERVER_IP}")
        print(e)
        print("         Please check if the server app is running.")
        print(f"         And the target IP address {SERVER_IP} is correct.\n\n")
        exit(1)

    # Let player input the attack target
    target_xy = my_game.get_hit_target()

    # Encode the target
    

print("Your turn to attack:")
target = my_game.get_hit_target()

# my_game.generate_hit_target(target)

my_attack = my_game.generate_hit_target()
# my_game.game_board.update_board(target)
# print(my_game.game_board)