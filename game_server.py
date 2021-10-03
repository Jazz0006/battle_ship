import game_class
import socket
import threading


class ClientThread(threading.Thread):
    """ A thread for each client connection

    Attribute:
        conn: the socket connection
        addr: client IP address and port
        my_game: a instance of GamePlay class

    """
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.conn = clientSocket
        self.addr = clientAddress
        print(" Info: A new player just connected from: ", clientAddress)
        self.my_game = game_class.GamePlay()
        print(" A new game board has been setup: \n")
        self.my_game.print_board()

    def run(self):
        """ Main function of the game

        Until all ships of either side are hit:
        1. Receive client's attack
        2. Return attack result
        3. Generate a random target to attack
        4. Send the attacking target
        5. Receive the attacking result

        """

        try:
            is_lost = b'0'

            while True:
                # Accept attack
                print(" Info: Waiting for opponent's attack...")
                buffer = self.conn.recv(2)
                if not buffer:
                    print(f" Error: Client's connection from {self.addr} has lost.")
                    print("        This game is ended.")
                    break

                decode_buffer = buffer.decode()
                target_cord = (int(decode_buffer[0]), int(decode_buffer[1]))

                # Check attack result
                print(f" Info: Under attack at {target_cord}")
                attack_result = self.my_game.gen_attack_result(target_cord)
                print(" Info: Attacke result: ", attack_result)

                # Send back the attack result
                if self.my_game.my_board.is_game_end:
                    is_lost = b'E'

                if attack_result:
                    is_hit = b'Y'
                else:
                    is_hit = b'N'

                self.conn.sendall(is_lost + is_hit)
                print(f" Info: Sending result to {self.addr}: {is_lost + is_hit}")

                if is_lost == b'E':  # Game is over
                    print(" Game Over, You lost.\n\n")
                    self.conn.close()
                    break

                # My Turn to Attack
                my_target = self.my_game.generate_hit_target()

                # Encode the target
                byte_2_send = (str(my_target[0]) + str(my_target[1])).encode()

                # Send the attacking target in 2 bytes
                self.conn.sendall(byte_2_send)
                print(f" Info: I attacked at {my_target}")

                # Receive attack result
                rcv_buffer = self.conn.recv(2)
                if not rcv_buffer:
                    print(f" Error: Client's connection from {self.addr} has lost.")
                    print("        This game is ended.")
                    break

                # First byte is gome over or not
                # Second byte is hit or not
                is_game_over = rcv_buffer[0]
                you_hit = rcv_buffer[1]

                if you_hit == ord(b'Y'):
                    print(" Info: You hit the enemy's ship!")
                    hit_result = 'X'
                else:
                    print(" Info: You missed...")
                    hit_result = '.'

                # Update board
                self.my_game.opponent_board.update_opponent_board(my_target, hit_result)
                print("------End of one round-------\n\n")

                if is_game_over == ord(b'E'):
                    print(" Congratualation! You won the game!\n\n")
                    break

        except Exception as err:
            print(" Error: Connection lost with the other player.")
            print("        Please connect again. \n\n")


# Main thread to receive connection:
if __name__ == "__main__":
    print(" Welcome to the battle ship game server.")
    print(" Now waiting for client to connect.")
    print("\n If you want to stop the server, plaese press Ctrl+C\n")

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

            while True:
                conn, addr = s.accept()
                newthread = ClientThread(addr, conn)
                newthread.start()

        except KeyboardInterrupt:
            print(" \nInfo:   Stopped accepting connection.")
            print(" Info:   See you next time\n\n")
            exit(1)
