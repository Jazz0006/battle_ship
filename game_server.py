import game_class
import socket
import threading
import traceback

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.conn = clientSocket
        self.addr = clientAddress
        print ("New connection added: ", clientAddress)
        self.my_game = game_class.GamePlay()
        self.my_game.print_board()
        #self.lock = threading.Lock()

    def run(self):
        try:
            print(" Info:   Connected with:", self.addr)

            is_lost = b'0'

            while True:
                # Accept attack
                print(" Wait for opponent's attack...")
                #self.lock.acquire()
                buffer = self.conn.recv(2)
                print(f" The buffer received from {self.addr}: {buffer}")              
                decode_buffer = buffer.decode()
                target_cord = (int(decode_buffer[0]), int(decode_buffer[1]))

                # Check attack result
                print(f" Under attack at {target_cord}")
                attack_result = self.my_game.gen_attack_result(target_cord)
                print(" Info: Attacke result: ", attack_result)
                # Print the game board
                #self.my_game.print_board()

                # Send back the attack result
                if self.my_game.my_board.is_game_end:
                    is_lost = b'E'

                if attack_result:
                    is_hit = b'Y'
                else:
                    is_hit = b'N'

                self.conn.sendall(is_lost + is_hit)
                print(f" Info: Sending result to {self.addr}: {is_lost + is_hit}")
                #self.lock.release()

                if is_lost == b'E': # Game is over
                    print(" Game Over, You lost.\n\n")
                    self.conn.close()
                    break

                # My Turn to Attack
                my_target = self.my_game.generate_hit_target()

                # Encode the target
                byte_2_send = (str(my_target[0]) + str(my_target[1])).encode()

                #self.lock.acquire()
                # Send the attacking target in 2 bytes
                self.conn.sendall(byte_2_send)
                print(f" Info: I attacked at {my_target}")

                # Receive attack result
                print(" Result of my attack...")
                rcv_buffer = self.conn.recv(2)
                #self.lock.release()
                print(rcv_buffer)
                
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
                self.my_game.opponent_board.update_opponent_board(my_target, hit_result)
                #self.my_game.print_board()
                print("------End of one round-------\n\n")
                if is_game_over == ord(b'E'):
                    print(" Congratualation! You won the game!\n\n")
                    break

        except Exception as err:
            print(" Error: Connection lost with the other player.")
            print("        Please connect again. \n\n")
            traceback.print_exc()



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

        while True:            
            conn, addr = s.accept()
            newthread = ClientThread(addr, conn)
            newthread.start()

    except KeyboardInterrupt:
        print(" \nInfo:   Stopped accepting connection.")
        print(" Info:   See you next time\n\n")
        exit(1)
