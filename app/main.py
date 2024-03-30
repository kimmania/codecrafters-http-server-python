import socket, threading
from .requestprocessor import processRequest

 
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    host = "127.0.0.1"
    port = 4221

    #server_socket = socket.create_server((host, port), reuse_port=False)
    with socket.create_server((host, port)) as server_socket:
        while True:
            (conn, addr) = server_socket.accept() # wait for client
            print(f"Connection from {addr} has been established.")
            connection = threading.Thread(target=processRequest, args=(conn,))
            connection.start()


if __name__ == "__main__":
    main()
