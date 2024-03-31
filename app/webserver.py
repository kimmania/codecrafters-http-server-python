import socket
import threading
from .request import Request
from .response import Response, ResponseCode

MINIMUN_BUFFER_SIZE = 1024
class WebServer:
    def __init__(self, host, port, file_directory=None, max_buffer: int=MINIMUN_BUFFER_SIZE):
        self.host = host
        self.port = port
        self.file_directory = file_directory
        self.server_socket = socket.create_server((host, port), reuse_port=True)
        self.running = False
        self.thread_pool = []
        self.endpoints = {}
        self.max_buffer = max(max_buffer, MINIMUN_BUFFER_SIZE)

    def start(self):
        print("Starting server...")
        self.running = True
        while self.running:
            conn, addr = self.server_socket.accept()
            t = threading.Thread(target=self._process_request, args=(conn,))
            self.thread_pool.append(t)
            t.start()

    def stop(self):
        print("Shutting down server...")
        self.running = False
        self.server_socket.close()
        for t in self.thread_pool:
            t.join()

    def get(self, path: str, handler: callable = None):
        self.endpoints["GET " + path] = handler

    def post(self, path: str, handler: callable = None):
        self.endpoints["POST " + path] = handler
    
    def _process_request(self, conn: socket.socket):
        # Initialize to an error and update when known
        response = Response(ResponseCode.INTERNAL_SERVER_ERROR) 
        with conn:
            try:
                data = conn.recv(self.max_buffer).decode()
                request = Request(data)
            except ValueError:
                response.setCode(ResponseCode.BAD_REQUEST).send(conn)
                return #exit

            if request.endpoint in self.endpoints:
                response = self.endpoints[request.endpoint](request, self)
            else:
                response.setCode(ResponseCode.NOT_FOUND)

            response.send(conn)

