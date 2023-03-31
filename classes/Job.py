from datetime import datetime
import sys
from utils.command import send_result_command
import socket
import os
import signal
from colorama import Fore, Style
from classes.ParsingEnum import RESTART_VALUES, STOP_SIGNAL, PROCESS_STATUS
import shlex, subprocess, uuid, base64, select

class Job:
    """Job is a class that contains all the required and optional options to do a job inside taskmaster's main program."""

    def __init__(self, name, cmd, user='', numprocs = 1, umask = 18, workingdir = '/tmp', autostart = True,
    autorestart = RESTART_VALUES.UNEXPECTED.value, exitcodes = 0, startretries = 3, starttime = 5, stopsignal = "SIGTERM",
    stoptime = 10, redirectstdout=False, stdout=None, redirectstderr=False, stderr=None, env=None):
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
            self.stdout = '/dev/null'
        else :
            self.stdout = stdout
        self.redirectstderr = redirectstderr
        if self.redirectstderr == True and stderr == None:
            self.stderr = '/tmp/' + self.name + '.stderr'
        elif  self.redirectstderr == False:
            self.stderr = '/dev/null'
        else :
            self.stderr = stderr
        self.state = PROCESS_STATUS.NOTSTARTED.value
        self.old_state = PROCESS_STATUS.UNKNOWN.value
        self.date_of_last_status_change = datetime.now().ctime()
        self.last_exit_code = 0
        self.attachMode = False
        self.stdoutFileForAttachMode = None
        self.stderrFileForAttachMode = None

    def __copy__(self):
        return Job(self.name, self.cmd, self.user, self.numprocs, self.umask, self.workingdir, self.autostart,
        self.autorestart, self.exitcodes, self.startretries, self.starttime, self.stopsignal, self.stoptime,
        self.redirectstdout, self.stdout, self.redirectstderr, self.stderr, self.env)

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

    def get_state(self):
        return self.state

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

    def start(self, connection=None, restart=False):
        if self.state == PROCESS_STATUS.RUNNING.value and restart == False:
            return send_result_command(connection, f"{Fore.BLUE}{Style.BRIGHT}[STATUS]{Style.RESET_ALL} {self.name} is already running.\nPlease use restart command to restart it.\n")

        if self.startretries != -1:
            cmd_split = shlex.split(self.cmd)
            try:
                self.process = subprocess.Popen(cmd_split,
                                env=dict(self.env),
                                stdout=open(self.stdout, 'w') if self.stdout else subprocess.PIPE,
                                stderr=open(self.stderr, 'w') if self.stderr else subprocess.PIPE,
                                cwd=self.workingdir,
                                umask=self.umask
                )
                if connection != None and isinstance(connection, socket.socket):
                    connection.settimeout(self.starttime)
                self.set_status(PROCESS_STATUS.RUNNING.value, connection)
            except:
                _, ex_value, _ = sys.exc_info()
                print(f"Error while starting {self.name}")
                print(ex_value, end="\n\n")
                return self.restart(connection)
        else:
            return self.set_status(PROCESS_STATUS.EXCITED.value, connection)
        self.startretries  = self.original_startretries


    def stop(self, connection=None):
        if connection != None and isinstance(connection, socket.socket):
            connection.settimeout(self.stoptime)


        signal_value = signal.Signals.__dict__.get(self.stopsignal)
        if not signal_value:
            signal_value = signal.SIGKILL
        if self.process != None:
            pid = self.process.pid
            try:
                os.kill(pid, signal_value)
            except ProcessLookupError:
                send_result_command(connection, f"Error: process {self.name} is not running")
                return
        self.set_status(PROCESS_STATUS.STOPPED.value, connection)

    def restart(self, connection=None):
        self.startretries -= 1
        if self.autorestart == False:
            self.set_status(PROCESS_STATUS.EXCITED.value, connection)
        elif self.autorestart == RESTART_VALUES.UNEXPECTED.value:
            if self.last_exit_code not in self.exitcodes:
                #for debugging purpose only
                self.stop(connection=connection)
                self.set_status(PROCESS_STATUS.RESTARTED.value, connection)
                self.start(connection=connection, restart=True)
            else:
                self.set_status(PROCESS_STATUS.EXCITED.value, connection)
        else:
            self.stop(connection=connection)
            self.set_status(PROCESS_STATUS.RESTARTED.value, connection)
            self.start(connection=connection, restart=True)

    def attach(self, connection=None):
        if self.attachMode == False:
            try:
                self.stderrFileForAttachMode = open(self.stderr, 'r') if self.stderr else self.process.stderr
                self.stdoutFileForAttachMode = open(self.stdout, 'r') if self.stdout else self.process.stdout
                self.attachMode = True
                pid = os.fork()
                if pid > 0:
                    if self.stdout:
                        self.stdoutFileForAttachMode.close()
                    if self.stderr:
                        self.stderrFileForAttachMode.close()
                    return
                elif pid == 0:
                    while self.attachMode:
                        r, _, _ = select.select([self.stdoutFileForAttachMode.fileno(), self.stderrFileForAttachMode.fileno()], [], [])
                        for fds in r:
                            if fds == self.stderrFileForAttachMode.fileno():
                                if self.stderr:
                                    datas = self.stderrFileForAttachMode.readline()
                                    send_result_command(connection, datas.decode())
                                else:
                                    datas = (self.stderrFileForAttachMode.readlines()[-20:])
                                    for line in datas:
                                        send_result_command(connection, line)
                            if fds == self.stdoutFileForAttachMode.fileno():
                                if self.stdout:
                                    datas = self.stdoutFileForAttachMode.readline()
                                    send_result_command(connection, datas.decode())
                                else:
                                    datas = (self.stdoutFileForAttachMode.readlines()[-20:])
                                    for line in datas:
                                        send_result_command(connection, line)
            except Exception as e:
                print(f"Error : {e}")
        else:
            data = "Attach Mode is already running."
            send_result_command(connection, data)

    def detach(self, connection=None):
        try:
            if self.stdout:
                self.stdoutFileForAttachMode.close()
            if self.stderr:
                self.stderrFileForAttachMode.close()
            self.attachMode = False
            send_result_command(connection, "Quitting attach mode.")
        except Exception as e:
            print(f"Error : {e}")
