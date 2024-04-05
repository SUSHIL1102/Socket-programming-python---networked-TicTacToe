import socket
import threading
import ssl

def handle_client(conn, player):
    global game_board

    conn.send(str(player).encode())

    while not is_winner(player) and not is_board_full():
        try:
            if player == 1:
                conn.send(str.encode("Your move, player 1. Enter your move (0-8): "))
            else:
                conn.send(str.encode("Your move, player 2. Enter your move (0-8): "))

            data = conn.recv(1024).decode()
            if not data:
                break
            if data == "QUIT":
                print("Player " + str(player) + " disconnected.")
                break

            
            move = int(data)
            if is_valid_move(move):
                update_board(move, player)
                board_state = display_board()
                conn.send(str.encode(board_state))
                if is_winner(player):
                    conn.send(str.encode("You win!, GAME OVER!!!!!\n"))
                    break
                elif is_board_full():
                    conn.send(str.encode("It's a draw!\n"))
                    break
                toggle_player()  # Toggle player after a valid move
            else:
                conn.send(str.encode("Invalid move. Try again.\n"))
        except Exception as e:
            print("Error: ", e)
            break

    conn.close()

def display_board():
    board_string = "Board:\n"
    board_string += game_board[0] + " | " + game_board[1] + " | " + game_board[2] + "\n"
    board_string += "--+---+--\n"
    board_string += game_board[3] + " | " + game_board[4] + " | " + game_board[5] + "\n"
    board_string += "--+---+--\n"
    board_string += game_board[6] + " | " + game_board[7] + " | " + game_board[8] + "\n\n"
    return board_string

def is_valid_move(move):
    return move >= 0 and move < 9 and game_board[move] == ' '

def update_board(move, player):
    global game_board
    game_board[move] = 'X' if player == 1 else 'O'

def toggle_player():
    global current_player
    current_player = 1 if current_player == 2 else 2

def is_winner(player):
    global game_board
    winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    symbol = 'X' if player == 1 else 'O'
    for combo in winning_combinations:
        if game_board[combo[0]] == game_board[combo[1]] == game_board[combo[2]] == symbol:
            return True
    return False

def is_board_full():
    global game_board
    return ' ' not in game_board

listen_addr = '10.30.203.8'
listen_port = 8082
server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)
context.check_hostname = False

current_player = 1
game_board = [' '] * 9

bindsocket = socket.socket()
bindsocket.bind((listen_addr, listen_port))
bindsocket.listen(2)

print("Waiting for connections...")

try:
    while True:
        player = 1
        clients = []
        while len(clients) < 2:
            newsocket, fromaddr = bindsocket.accept()
            print("Connected to:", fromaddr)
            conn = context.wrap_socket(newsocket, server_side=True)
            #print("SSL established. Peer: {}".format(conn.getpeercert()))
            clients.append((conn, player))
            threading.Thread(target=handle_client, args=(conn, player)).start()
            player += 1
finally:
    conn.close()
