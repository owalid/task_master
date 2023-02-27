import socket
import os

SOCK_FILE = "/tmp/taskmaster.sock"

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.exists(SOCK_FILE):
            os.remove(SOCK_FILE)
        self.server_socket = None
        self.bind()
        self.listen()
        self.accept()
    
    def listen(self):
        '''
        Enable a server to accept connections.
        '''
        self.server.listen()
    
    def bind(self):
        '''
        Bind the socket to address.
        '''
        self.server.bind(SOCK_FILE)

    def accept(self):
        '''
        Accept a connection. The socket must be bound to an address and listening for connections.
        '''
        self.server_socket, _ = self.server.accept()
        self.server_socket.setblocking(False)

    def close(self):
        '''
        Close the socket.
        '''
        if self.server_socket != None:
            self.server_socket.close()

    def receive(self):
        '''
        Receive data from the socket.
        '''
        data = self.server_socket.recv(1024)
        return data.decode()

    def send(self, data):
        '''
        Send data to the socket.
        '''
        self.server_socket.send(data.encode())