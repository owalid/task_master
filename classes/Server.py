import socket
import os, subprocess
from classes.ParsingEnum import ALLOWED_COMMANDS, ERRORS, PROCESS_STATUS, RESTART_VALUES
from utils.command import send_result_command

SOCK_FILE = "/tmp/taskmaster.sock"
SIZE_OF_RECEIVE = 1024

class Server:
    # __instance is used to store the instance of the class
    __instance = None

    @staticmethod
    def get_instance():
        '''
            Static access method. used to make singleton.
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
        '''
        Start the server. Bind the socket to address and listen for connections.
        return: None
        '''
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
            print(f'{ERRORS.EVEN_MANAGER_FAILED_ERROR.value}{e}')

    def bind(self):
        '''
        Bind the socket to address.
        return: None
        '''
        self.server.bind(SOCK_FILE)

    def list_jobs(self):
        '''
        List all jobs.
        return: None
        '''
        jobs_name = [job.name for job in self.jobs]
        jobs_name = "\n".join(jobs_name)
        send_result_command(self.connection, jobs_name)

    def parse_data_received(self, data):
        '''
        Parse the data received from the socket.
        return: None
        '''
        if data:
            data_splitted = data.split(" ")

            # if we receive only kill
            if (data_splitted[0] == "kill" or data_splitted[0] == "list") and len(data_splitted) < 2:
                data_splitted.append("")

            if len(data_splitted) < 2:
                send_result_command(self.connection, "Invalid command.")
                return

            command, job_name = data_splitted[0], data_splitted[1]
            if command == "kill":
                self.stop_all_jobs()
                print('')
                self.close()
                exit(0)
            elif command == "list":
                print("list")
                self.list_jobs()
                return
            if job_name == "all" and command in ALLOWED_COMMANDS:
                for job in self.jobs:
                    self.send_command(job.name, command)
                return
            jobs_name = [job.name for job in self.jobs]
            invalid_job_name = job_name not in jobs_name
            invalid_command = command not in ALLOWED_COMMANDS
            if invalid_job_name:
                send_result_command(self.connection, "Invalid job name.")
            elif invalid_command:
                send_result_command(self.connection, "Invalid command.")
            else:
                self.send_command(job_name, command)
        return

    def listen_accept_receive(self):
        '''
        Accept a connection. The socket must be bound to an address and listening for connections.
        return: None
        '''
        try:
            while True:
                self.server.listen()
                self.connection, _ = self.server.accept()
                while True:
                    self.connection.setblocking(True)
                    res = b''
                    while True:
                        try:
                            data = self.connection.recv(SIZE_OF_RECEIVE)
                            res += data
                            if len(data.decode()) < SIZE_OF_RECEIVE or data == b'':
                                break
                        except:
                            break
                    if not res:
                        break
                    for job in self.jobs:
                        if job.process:
                            if job.process.poll() is not None and job.get_state() != PROCESS_STATUS.EXITED.value:
                                job.last_exit_code = job.process.returncode
                                job.set_status(PROCESS_STATUS.EXITED.value)
                                if (job.autorestart == True or job.autorestart == RESTART_VALUES.UNEXPECTED.value) and job.startretries > 0:
                                    job.restart()
                    self.parse_data_received(res.decode())

                    # Check for all processes if they are still running
        except KeyboardInterrupt:
            print('')
            self.close()
            exit(0)


    def close(self):
        '''
        Close the socket.
        return: None
        '''
        if self.connection != None:
            self.connection.close()

    # Job management

    @staticmethod
    def get_job_from_name(jobs, job_name):
        '''
        Return the job object from its name.
        return: Job
        '''
        for job in jobs:
            if job.name == job_name:
                return job
        return None

    def start_all_jobs(self):
        '''
        Start all jobs if "autostart" option is sets to true
        return: None
        '''
        for job in self.jobs:
            job_state = job.get_state()
            if job.autostart == True and job_state != PROCESS_STATUS.STARTED.value \
            and job_state != PROCESS_STATUS.RESTARTED.value and job.to_resume == False:
                job.start()
            if job.to_resume == True:
                job.resume()

    def stop_all_jobs(self):
        '''
        Stop all jobs
        return: None
        '''
        for job in self.jobs:
            job_state = job.get_state()
            if job_state != PROCESS_STATUS.STOPPED.value:
                job.stop()

    def send_command(self, job_name, cmd_name):
        '''
        Send an command to the job dynamically.
        return: None
        '''
        job = self.get_job_from_name(self.jobs, job_name)

        if job == None:
            return send_result_command(self.connection, "Job not found.")
        if hasattr(job, cmd_name) and callable(job_function := getattr(job, cmd_name)):
            # get the function corresponding to the command from the job object
            # Example: if cmd_name == "status", then job_function = job.status
            return job_function(self.connection)
        return send_result_command(self.connection, "command not found.")
