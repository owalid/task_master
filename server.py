import socket
import os
from ParsingEnum import ALLOWED_COMMANDS

SOCK_FILE = "/tmp/taskmaster.sock"

class Server:
    def __init__(self, jobs):
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.exists(SOCK_FILE):
            os.remove(SOCK_FILE)
        self.connection = None
        self.jobs = jobs
        self.start_all_jobs()
        self.bind()
        self.listen_accept_receive()
        
    
    def bind(self):
        '''
        Bind the socket to address.
        '''
        self.server.bind(SOCK_FILE)

    def parse_data_received(self, data):
        '''
        Parse the data received from the socket.
        '''
        if data:

            data_splitted = data.split(" ")
            if len(data_splitted) < 2:
                self.send("Invalid command.")
                return
            command, job_name = data_splitted[0], data_splitted[1]
            
            print(f"command: {command}, job_name: {job_name}")
            res = ''
            if job_name == "all" and command in ALLOWED_COMMANDS:
                for job in self.jobs:
                    res = self.send_command(job.name, command)
                    self.send(res)
                return
            
            jobs_name = [job.name for job in self.jobs]
            invalid_job_name = job_name not in jobs_name
            invalid_command = command not in ALLOWED_COMMANDS
            if invalid_job_name:
                self.send("Invalid job name.")
            elif invalid_command:
                self.send("Invalid command.")
            else:
                res = self.send_command(job_name, command)
                self.send(res)
        return

    def listen_accept_receive(self):
        '''
        Accept a connection. The socket must be bound to an address and listening for connections.
        '''
        self.server.listen()
        self.connection, _ = self.server.accept()
        while True:
            self.connection.setblocking(True)
            data = self.connection.recv(1024)
            self.parse_data_received(data.decode())


    def close(self):
        '''
        Close the socket.
        '''
        if self.connection != None:
            self.connection.close()

    def send(self, data):
        '''
        Send data to the socket.
        '''
        self.connection.send(data.encode())
    
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
    
    def start_all_jobs(self):
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