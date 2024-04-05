import socket
import ssl

def main():
    host_addr = '192.168.80.149'
    host_port = 8082
    server_sni_hostname = 'example.com'
    server_cert = 'server.crt'
    client_cert = 'client.crt'
    client_key = 'client.key'

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)
    context.check_hostname = False

    print("Connected to Tic Tac Toe server.")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
    conn.connect((host_addr, host_port))

    player = int(conn.recv(1024).decode())
    print("You are player", player)

    try:
        while True:
            data = conn.recv(1024).decode()
            print(data)

            if "Enter your move" in data:
                move = input("Enter your move (0-8): ")
                if move.isdigit() and 0 <= int(move) <= 8:
                    conn.send(str.encode(move))
                else:
                    print("Invalid input. Please enter a number between 0 and 8.")
            elif "Waiting for player" in data:
                pass  # Do nothing, just wait
            elif "It's a draw!" in data or "You win!" in data or "Player" in data:
                # Game over message received from server, break the loop
                print(data)
                break
            else:
                # Display the game board
                print(data)

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
