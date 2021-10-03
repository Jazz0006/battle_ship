import game_class
import socket
import os

SERVER_IP = "172.26.59.193"


def clear_screen():
    if os.name == "posix":
        _ = os.system('clear')
    else:
        _ = os.system('cls')

if __name__ == "__main__":
    clear_screen()
    print(" Welcome to the battle ship game client.")
    print(" You will be playing with the computer.")
    print(" Let's start! \n")
    print(f"Connecting to the server at {SERVER_IP}")
    print(" You can edit SERVER_IP in this file to change the setting.")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_IP, 9587))
        except Exception as err:
            print("-"*71)
            print(f" Error:  Cannot connect to host: {SERVER_IP}")
            print(err)
            print("         Please check if the server app is running.")
            print(f"         And the IP address {SERVER_IP} is correct.\n\n")
            exit(1)

        my_game = game_class.GamePlay()
        print(""" Symbles:
            'O' -- empty space
            'H' -- ship
            'X' -- attacked ship
            '.' -- attacked empty space
            """)

        my_game.print_board()

        is_lost = b'0'

        while True:
            # Let the player input the attack target
            target_xy = my_game.get_hit_target()

            # Encode the target
            byte_2_send = (str(target_xy[0]) + str(target_xy[1])).encode()

            # Send the attacking target in 2 bytes
            s.sendall(byte_2_send)

            # Receive attack result
            rcv_buffer = s.recv(2)
            if not rcv_buffer:
                print(f" Error: Server's connection has lost.")
                print("        This game is ended.")
                break

            clear_screen()
            print(f" This round: you attacked at {target_xy}")

            # First byte is gome over or not
            # Second byte is hit or not
            is_game_over = rcv_buffer[0]
            you_hit = rcv_buffer[1]

            if you_hit == ord(b'Y'):
                print(" You hit the enemy's ship!")
                hit_result = 'X'
            else:
                print(" You missed...")
                hit_result = '.'

            # Update the game board
            my_game.opponent_board.update_opponent_board(target_xy, hit_result)

            if is_game_over == ord(b'E'):
                print(" Congratualation! You won the game!\n\n")
                my_game.print_board()
                break

            # Receive attack
            buffer = s.recv(2)
            if not rcv_buffer:
                print(f" Error: Server's connection has lost.")
                print("        This game is ended.")
                break

            decode_buffer = buffer.decode()
            target_cord = (int(decode_buffer[0]), int(decode_buffer[1]))

            # Check attack result
            attack_result = my_game.my_board.update_my_board(target_cord)
            print(f" \nThe computer attacked you at {target_cord}")
            if attack_result:
                print(" Your ship was hit")
            else:
                print(" You are lucky, the enemy just missed.")

            # Send back the attack result
            if my_game.my_board.is_game_end:
                is_lost = b'E'

            if attack_result:
                is_hit = b'Y'
            else:
                is_hit = b'N'

            buffer_result = is_lost + is_hit
            s.sendall(buffer_result)

            print("\n After this round, the game board is:")
            my_game.print_board()

            if is_lost == b'E':  # Game is over
                print(" Game Over, You lost.\n\n")
                break
