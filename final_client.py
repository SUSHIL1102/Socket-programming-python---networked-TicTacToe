import socket
import ssl 

def main():
    host_addr = '10.30.203.8'
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
    #print("SSL established. Peer: {}".format(conn.getpeercert()))

    player = int(conn.recv(1024).decode())
    print("You are player", player)

    while True:
        try:
            data = conn.recv(1024).decode()
            if "Enter your move" in data:
                move = input(data)
                conn.send(str.encode(move))
            elif "Waiting for player" in data:
                pass  # Do nothing, just wait
            else:
                print(data)
                break  # Game over

           
            board_state = conn.recv(1024).decode()
            print(board_state)
        except Exception as e:
            print("Error: ", e)
            break

    conn.close()

if __name__ == "__main__":
    main()