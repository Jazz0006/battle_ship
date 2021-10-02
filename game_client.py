import game_class
import socket
import time

SERVER_IP = "172.26.59.193"

my_game = game_class.GamePlay()
my_game.print_board()

print("Connecting to the server...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((SERVER_IP, 9587))
    except Exception as err:
        print("-"*71)
        print(f" Error:  Cannot connect to host: {SERVER_IP}")
        print(err)
        print("         Please check if the server app is running.")
        print(f"         And the target IP address {SERVER_IP} is correct.\n\n")
        exit(1)

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
        # First byte is gome over or not
        # Second byte is hit or not
        is_game_over = rcv_buffer[0]
        
        you_hit = rcv_buffer[1]

        if you_hit == ord(b'Y'):
            print(" You hit enemy's ship!")
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
        #print(" Wait for opponent's attack...")
        buffer = s.recv(2)                
        decode_buffer = buffer.decode()
        target_cord = (int(decode_buffer[0]), int(decode_buffer[1]))

        time.sleep(1)

        # Check attack result
        attack_result = my_game.my_board.update_my_board(target_cord)
        print(f" Under attack at {target_cord}")
        if attack_result:
            print("Your ship was hit")
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
        print("enemy's result: ", buffer_result)
        s.sendall(buffer_result)

        my_game.print_board()

        if is_lost == b'E': # Game is over
            print(" Game Over, You lost.\n\n")
            break
    