import socket, sys, threading
from .requestprocessor import processRequest

 
def main(directory: str | None):
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    host = "127.0.0.1"
    port = 4221

    with socket.create_server((host, port)) as server_socket:
        while True:
            (conn, addr) = server_socket.accept() # wait for client
            print(f"Connection from {addr} has been established.")
            connection = threading.Thread(target=processRequest, args=(conn,directory))
            connection.start()


if __name__ == "__main__":
    args = sys.argv
    print(args)
    for i in range(len(args)):
        if args[i] == "--directory":
            directory = args[i + 1]
            print("directory= " + directory)
            main(directory)
    main(None)