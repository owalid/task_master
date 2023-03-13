from datetime import datetime
from utils.command import send_result_command
import socket
import signal
from colorama import Fore, Style
from classes.ParsingEnum import RESTART_VALUES, STOP_SIGNAL, PROCESS_STATUS
import shlex, subprocess, uuid, base64

class Job:
    """Job is a class that contains all the required and optional options to do a job inside taskmaster's main program."""

    def __init__(self, name, cmd, user='', numprocs = 1, umask = 18, workingdir = '/tmp', autostart = True,
    autorestart = RESTART_VALUES.UNEXPECTED.value, exitcodes = 0, startretries = 3, starttime = 5, stopsignal = "SIGTERM",
    stoptime = 10, redirectstdout=False, stdout="/dev/null", redirectstderr=False, stderr="/dev/null", env=None):
        self.name = name
        self.cmd = cmd
        self.user = user
        self.numprocs = numprocs
        self.umask = umask
        self.workingdir = workingdir
        self.autostart = autostart
        self.autorestart = autorestart
        self.exitcodes  = exitcodes
        self.startretries = startretries
        self.original_startretries = startretries
        self.starttime = starttime
        self.stopsignal = stopsignal
        self.stoptime = stoptime
        self.redirectstdout = redirectstdout

        self.env = {}
        self.process = None

        for key, value in env.items():
            self.env[key] = str(value)

        if self.redirectstdout == True and stdout == None:
            self.stdout = '/tmp/' + self.name + '.stdout'
        elif self.redirectstdout == False:
            self.stdout = ''
        else :
            self.stdout = stdout
        self.redirectstderr = redirectstderr
        if self.redirectstderr == True and stderr == None:
            self.stderr = '/tmp/' + self.name + '.stderr'
        elif  self.redirectstderr == False:
            self.stderr = ''
        else :
            self.stderr = stderr

        self.state = PROCESS_STATUS.NOTSTARTED.value
        self.old_state = PROCESS_STATUS.UNKNOWN.value
        self.date_of_last_status_change = datetime.now().ctime()
        self.last_exit_code = 0

    def print_conf(self):
        print("Name : "  + self.name)
        print("Command : " + self.cmd)
        print("Number of proc " + str(self.numprocs))
        print("Umask : " + str(self.umask))
        print("Working Directory : " + self.workingdir)
        print("Autostart : " + str(self.autostart))
        print("Autorestart : " + str(self.autorestart))
        print("Exit codes : " + str(self.exitcodes))
        print("Start retries : " + str(self.startretries))
        print("Start time : " + str(self.starttime))
        print("Stop signal : " + self.stopsignal)
        print("Stop time : " + str(self.stoptime))
        print(f"redirectstdout: {self.redirectstdout}")
        print("stdout : " + self.stdout)
        print(f"redirectstderr: {self.redirectstderr}")
        print("stderr : " + self.stderr)
        print("env : ")
        for key, value in self.env.items():
            print(" ",key , ": ", value)


    def set_status(self, new_status, connection=None):
        if new_status not in PROCESS_STATUS:
            raise TypeError("The status could'nt be changed. See ParsingEnum.py/PROCESS_STATUS for available statuses.")
        self.old_state = self.state
        self.state = new_status
        self.date_of_last_status_change = datetime.now().ctime()
        self.make_log()
        self.status(connection)

    def status(self, connection=None):
        result = ''
        if self.state != PROCESS_STATUS.EXCITED.value:
            result = f"{Fore.BLUE}{Style.BRIGHT}[STATUS]{Style.RESET_ALL} {self.name} is currently {Style.BRIGHT}{self.state}{Style.RESET_ALL} since {Style.BRIGHT}{self.date_of_last_status_change}{Style.RESET_ALL}.\n"
        else:
            result = f"{Fore.BLUE}{Style.BRIGHT}[STATUS]{Style.RESET_ALL} {self.name} is currently {Style.BRIGHT}{self.state}{Style.RESET_ALL} with code {self.last_exit_code} since {Style.BRIGHT}{self.date_of_last_status_change}{Style.RESET_ALL}.\n"

        send_result_command(connection, result)

    def make_log(self):
        log = "server:Taskmaster|"
        log += "eventid:" + str(uuid.uuid1()) + "|"
        log += "date:" + base64.b64encode(self.date_of_last_status_change.encode()).decode() + "|"
        log += "processname:" + self.name + "|"
        log += "processcmd:" + self.cmd + "|"
        log += "eventtype:PROCESS_STATES|"
        log += "fromstate:" + self.old_state.upper() + "|"
        log += "tostate:" + self.state.upper() + "|"
        log += "lastexitcode:" + str(self.last_exit_code) + "\n"
        try:
            with open("/tmp/.taskmaster_raw_logs", "a") as file_log:
                file_log.write(log)
            file_log.close()
            with open("./logs/taskmaster_raw_logs.log", "a") as raw_log:
                raw_log.write(log)
            raw_log.close()
        except Exception as e:
            print(f"The logs could'nt be wrote : {e}")

    def start(self, connection=None):
        if self.startretries != -1:
            cmd_split = shlex.split(self.cmd)
            try:
                print(f"CMD = {self.cmd}")
                with open(self.stdout, 'w') as f_out:
                    with open(self.stderr, 'w') as f_err:
                        try:
                            self.process = subprocess.Popen(cmd_split,
                                            env=dict(self.env),
                                            stdout=open(self.stdout, 'w'),
                                            stderr=open(self.stderr, 'w'),
                                            cwd=self.workingdir,
                                            umask=self.umask
                            )
                            if connection != None and isinstance(connection, socket.socket):
                                connection.settimeout(self.starttime)
                            self.set_status(PROCESS_STATUS.RUNNING.value, connection)
                        except Exception as e:
                            print(e)
                            return self.restart(connection)
            except OSError as e:
                print(e)
                return self.restart(connection)
        else:
            return self.set_status(PROCESS_STATUS.EXCITED.value, connection)
        # self.startretries  = self.original_startretries


    def stop(self, connection=None):
        if connection != None and isinstance(connection, socket.socket):
            connection.settimeout(self.stoptime)

        signal_value = signal.Signals.__dict__.get(self.stopsignal)

        if signal_value:
            self.process.send_signal(signal_value)
        self.process.kill()
        self.set_status(PROCESS_STATUS.STOPPED.value, connection)

    def restart(self, connection=None):
        self.startretries -= 1
        if self.autorestart == False:
            print("autorestart == false")
            self.set_status(PROCESS_STATUS.EXCITED.value, connection)
        elif self.autorestart == RESTART_VALUES.UNEXPECTED.value:
            normal_exit_code = True
            for exitcode in self.exitcodes:
                if self.last_exit_code != exitcode:
                    #for debugging purpose only
                    print(f"The exit code is not expected : {str(self.last_exit_code)}")
                    self.stop()
                    self.set_status(PROCESS_STATUS.RESTARTED.value, connection)
                    self.start()
                    normal_exit_code = False
            if normal_exit_code == True:
                self.set_status(PROCESS_STATUS.STOPPED.value, connection)
        else:
            print("autorestart == true")
            self.stop()
            self.set_status(PROCESS_STATUS.RESTARTED.value, connection)
            self.start()

