import socket
import os

SOCK_FILE = "/tmp/taskmaster.sock"

class Server:
    def __init__(self, jobs):
        try:
            self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            if os.path.exists(SOCK_FILE):
                os.remove(SOCK_FILE)
            self.server_socket = None
            self.jobs = jobs
            self.bind()
            self.listen()
        except ConnectionRefusedError:
            print("Connection refused")
            exit(1)
        except KeyboardInterrupt:
            print("Bye")
            exit(0)
    
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
    
    # Job management
    
    @staticmethod
    def get_job_from_name(jobs, job_name):
        '''
        Return the job object from its name.
        '''
        for job in jobs:
            if job.name == job_name:
                return job
        return None
    
    def start_all(self):
        '''
        Start all jobs.
        '''
        for job in self.jobs:
            job.start()
    
    def send_command(self, job_name, cmd_name):
        '''
        Send an command to the job.
        '''
        job = self.get_job_from_name(self.jobs, job_name)
        if job == None:
            return "Job not found."
        if hasattr(job, cmd_name) and callable(job_function := getattr(job, cmd_name)):
            # get the function corresponding to the command from the job object
            # Example: if cmd_name == "status", then job_function = job.status
            return job_function()
        return "command not found."