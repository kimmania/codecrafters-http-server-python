import socket

RESPONSE_200_OK = "HTTP/1.1 200 OK\r\n\r\n"

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    (conn, addr) = server_socket.accept() # wait for client
    
    with conn:
        print(f'addr: {addr}')
        data = conn.recv(1024)
        conn.send(RESPONSE_200_OK.encode())

if __name__ == "__main__":
    main()
