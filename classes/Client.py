import socket
import os
from classes.ParsingEnum import ERRORS
from classes.Server import SOCK_FILE

class Client:
    def __init__(self):
        self.client_socket = None
        try:
            if not os.path.exists(SOCK_FILE):
                print(f"{ERRORS.NO_SUCH_FILE_ERROR.value}unix://{SOCK_FILE}")
            else:
                self.client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.client_socket.settimeout(1)
                self.connect()
        except ConnectionRefusedError:
            print(f"{ERRORS.CONNECTION_REFUSED_ERROR.value}unix://{SOCK_FILE}")
            exit(1)

    def connect(self):
        '''
        Connect to the server according to the socket file.
        return: None
        '''
        self.client_socket.connect(SOCK_FILE)

    def send(self, data):
        '''
        Send data to the server.
        return: None
        '''
        print(data)
        try:
            self.client_socket.send(data.encode())
        except ConnectionResetError:
            print(ERRORS.CONNECTION_RESET_ERROR.value)
            exit(1)
        except BrokenPipeError:
            print(ERRORS.BROKEN_PIPE_ERROR.value)
            exit(1)

    def receive(self):
        '''
        Receive data from the server.
        return: None
        '''
        try:
            data = self.client_socket.recv(1024)
            return data.decode()
        except ConnectionResetError:
            print(ERRORS.CONNECTION_RESET_ERROR.value)
            exit(1)
        except socket.timeout:
            return

    def close(self):
        '''
        Close the socket.
        return: None
        '''
        if self.client_socket != None:
            self.client_socket.close()
