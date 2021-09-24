import game_class
import socket

my_game = game_class.GamePlay()
my_game.print_board()

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

            is_lost = b'0'

            while True:
                # Accept attack
                print(" Wait for opponent's attack...")
                buffer = conn.recv(2)                
                decode_buffer = buffer.decode()
                target_cord = (int(decode_buffer[0]), int(decode_buffer[1]))

                # Check attack result
                attack_result = my_game.my_board.update_my_board(target_cord)
                print(f" Under attack at {target_cord}")
                if attack_result:
                    print("Your ship was hit.\n")
                else:
                    print(" You are lucky, the enemy just missed.\n")

                my_game.print_board()

                # Send back the attack result
                if my_game.my_board.is_game_end:
                    is_lost = b'E'

                if attack_result:
                    is_hit = b'Y'
                else:
                    is_hit = b'N'

                conn.sendall(is_lost + is_hit)

                if is_lost == b'E': # Game is over
                    print(" Game Over, You lost.\n\n")
                    break

                # My Turn to Attack
                my_target = my_game.generate_hit_target()

                # Encode the target
                byte_2_send = (str(my_target[0]) + str(my_target[1])).encode()

                # Send the attacking target in 2 bytes
                conn.sendall(byte_2_send)
                print(f" I attacked at {my_target}")

                # Receive attack result
                print(" Waiting for the result of my attack...")
                rcv_buffer = conn.recv(2)
                print(rcv_buffer)
                ####rcv_decoded = rcv_buffer.decode()
                ####print(type(rcv_decoded))
                # First byte is gome over or not
                # Second byte is hit or not
                is_game_over = rcv_buffer[0]
                you_hit = rcv_buffer[1]
                #print("The first byte I received: ", is_game_over)
                #print("The second byte I received: ", you_hit)

                if you_hit == ord(b'Y'):
                    print(" You hit enemy's ship!")
                    hit_result = 'X'
                else:
                    print(" You missed...")
                    hit_result = '.'

                # Show the attack result
                my_game.opponent_board.update_opponent_board(my_target, hit_result)
                my_game.print_board()

                if is_game_over == ord(b'E'):
                    print(" Congratualation! You won the game!\n\n")
                    break

    except Exception as err:
        print(" Error: Connection lost with the other player.")
        print("        Please connect again. \n\n")
        print(err)

    


#print("Your turn to attack:")
#target = my_game.get_hit_target()

# my_game.generate_hit_target(target)

#my_attack = my_game.generate_hit_target()
# my_game.game_board.update_board(target)
# print(my_game.game_board)