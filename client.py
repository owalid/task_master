import socket
import os
from server import SOCK_FILE

class Client:
    def __init__(self):
        self.client_socket = None
        try:
            if not os.path.exists(SOCK_FILE):
                print(f"unix://{SOCK_FILE} no such file")
            else:
                self.client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.connect()
        except ConnectionRefusedError:
            print(f"Connection refused: unix://{SOCK_FILE}")
            exit(1)

    def connect(self):
        self.client_socket.connect(SOCK_FILE)

    def send(self, data):
        print(data)
        self.client_socket.send(data.encode())

    def receive(self):
        data = self.client_socket.recv(1024)
        return data.decode()

    def close(self):
        if self.client_socket != None:
            self.client_socket.close()
