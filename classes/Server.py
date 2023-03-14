import socket
import os, subprocess
from classes.ParsingEnum import ALLOWED_COMMANDS, PROCESS_STATUS
from utils.command import send_result_command

SOCK_FILE = "/tmp/taskmaster.sock"

class Server:
    # __instance is used to store the instance of the class
    __instance = None

    @staticmethod
    def get_instance():
        '''
        Static access method.
        '''
        if Server.__instance == None:
            Server()
        return Server.__instance

    def __init__(self, jobs, event_manager_options):
        if Server.__instance != None:
            return Server.__instance
        else:
            self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            if os.path.exists(SOCK_FILE):
                os.remove(SOCK_FILE)
            self.connection = None
            self.jobs = jobs
            self.event_manager_options = event_manager_options
            self.event_manager_process = None
            Server.__instance = self


    def start_server(self):
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
                if os.path.exists("./event_manager/.env") == False:
                    print("No .env file found.")
                    print("First you need to enable 2FA on your google account.")
                    print("Then you need to generate an app password (this will not be your real password).")
                    print("link : https://support.google.com/accounts/answer/185833")
                    print("When it's done, copy and paste the password inside a .env file at the root directory of eventmanager.py. Put your gmail account too.")
                    print("Check .env_sample for an example.")
                    exit(1)
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
            if job_name == "all" and command in ALLOWED_COMMANDS:
                for job in self.jobs:
                    self.send_command(job.name, command)
                return

            jobs_name = [job.name for job in self.jobs]
            invalid_job_name = job_name not in jobs_name
            invalid_command = command not in ALLOWED_COMMANDS
            if invalid_job_name:
                send_result_command("Invalid job name.", self.connection)
            elif invalid_command:
                send_result_command("Invalid command.", self.connection)
            else:
                self.send_command(job_name, command)
        return

    def listen_accept_receive(self):
        '''
        Accept a connection. The socket must be bound to an address and listening for connections.
        '''
        try:
            self.server.listen()
            self.connection, _ = self.server.accept()
            while True:
                self.connection.setblocking(True)
                data = self.connection.recv(1024)
                self.parse_data_received(data.decode())
                for job in self.jobs:
                    if job.process.poll() is not None:
                        job.last_exit_code = job.process.returncode
        except KeyboardInterrupt:
            print('')
            self.close()
            exit(0)


    def close(self):
        '''
        Close the socket.
        '''
        if self.connection != None:
            self.connection.close()

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
        Start all jobs if "autostart" option is sets to true
        '''
        for job in self.jobs:
            job_state = job.get_state()
            if job.autostart == True and job_state != PROCESS_STATUS.RUNNING.value \
            and job_state != PROCESS_STATUS.STARTED.value and job_state != PROCESS_STATUS.RESTARTED.value:
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
            return job_function(self.connection)
        return "command not found."
