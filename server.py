import socket
import os, subprocess
from ParsingEnum import ALLOWED_COMMANDS

SOCK_FILE = "/tmp/taskmaster.sock"

class Server:
    def __init__(self, jobs, event_manager_options):
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.exists(SOCK_FILE):
            os.remove(SOCK_FILE)
        self.connection = None
        self.jobs = jobs
        self.event_manager_options = event_manager_options
        self.event_manager_process = None
        self.start_all_jobs()
        self.start_event_manager()
        self.bind()
        self.listen_accept_receive()

    def start_event_manager(self):
        '''
        Start the event manager if option sets to true.
        '''
        try:
            if self.event_manager_options.activated == True:
                pwsd=""
                if os.path.exists("./event_manager/.env") == False:
                    while 1:
                        print("=== Configuration of email sending ===")
                        print("First you need to enable 2FA on your google account.")
                        input("Press any key when it is OK : ")
                        print("Then you need to generate an app password (this will not be your real password).")
                        print("link : https://support.google.com/accounts/answer/185833")
                        pwsd = input("When it's ok, copy and paste the password here : ")
                        break
                    with open("./event_manager/.env", "a") as f:
                        f.writelines("USERMAIL=" + self.event_manager_options.mail + "\n")
                        f.writelines("PASSWORD=" + pwsd + "\n")
                    f.close()
                self.event_manager_process = subprocess.Popen \
                        (["python3", "event_manager/eventmanager.py"],  \
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            print("[ERROR] The event manager could not be launched.")
            print(e)
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
            
            #! NEED TO REMOVE ONLY FOR DEBUG / TEST PURPOSE
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