import socket
import os
from server import SOCK_FILE

class Client:
    def __init__(self):
        self.client_socket = None
        if not os.path.exists(SOCK_FILE):
            print("unix:///tmp/server.sock no such file")
        else:
            self.client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.connect()

    def connect(self):
        self.client_socket.connect(SOCK_FILE)

    def send(self, data):
        self.client_socket.send(data.encode())

    def receive(self):
        data = self.client_socket.recv(1024)
        return data.decode()

    def close(self):
        if self.client_socket != None:
            self.client_socket.close()
