import game_class
import socket

my_game = game_class.GamePlay()
print("Enemy's Board: ")
print(my_game.opponent_board)
print("---------------------")
print("My Board: ")
print(my_game.my_board)

print("Waiting for player to connect...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind(('', 9587))
    except Exception as e:
        print(" Error:  Cannot create a socket")
        print(e)
        print(" Please check your network setting.")
        exit(1)

    try:
        s.listen()
        conn, addr = s.accept()
    except KeyboardInterrupt:
        print(" \nInfo:   Stopped accepting connection.")
        print(" Info:   See you next time\n\n")
        exit(1)

    try:
        with conn:
            print(" Info:   Connected with:", addr)

            # Accept attack
            

    except:
        print(" Error: Connection lost with the other player.")
        print("        Please connect again. \n\n")


print("Your turn to attack:")
target = my_game.get_hit_target()

# my_game.generate_hit_target(target)

my_attack = my_game.generate_hit_target()
# my_game.game_board.update_board(target)
# print(my_game.game_board)