import argparse, sys
from .webserver import WebServer
from .requestprocessor import RequestProcessor

HOST = "localhost"
PORT = 4221

def main():
    print("Logs from your program will appear here!")
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default=None, required=False, type=str)
    args = parser.parse_args()
    server = WebServer(HOST, PORT, file_directory=args.directory)

    server.get("", RequestProcessor.upCheck)
    server.get("echo", RequestProcessor.echo)
    server.get("user-agent", RequestProcessor.returnUserAgent)
    server.get("files", RequestProcessor.getFile)
    server.post("files", RequestProcessor.postFile)
    try:
        server.start()
    finally:
        server.stop()

if __name__ == "__main__":
    sys.exit(main())
