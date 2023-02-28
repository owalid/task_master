from ParsingEnum import RESTART_VALUES
from ParsingEnum import STOP_SIGNAL
from ParsingEnum import PROCESS_STATUS
from datetime import datetime
from colorama import Fore, Style
class Job:
    """Job is a class that contains all the required and optional options to do a job inside taskmaster's main program."""

    

    def __init__(self, name, cmd, numprocs = 1, umask = 18, workingdir = '/tmp', autostart = True,
    autorestart = RESTART_VALUES.UNEXPECTED.value, exitcodes = 0, startretries = 3, starttime = 5, stopsignal = STOP_SIGNAL.TERM.value,
    stoptime = 10, redirectstdout=False, stdout=None, redirectstderr=False, stderr=None, env=None):
        self.name = name
        self.cmd = cmd
        self.numprocs = numprocs
        self.umask = umask
        self.workingdir = workingdir
        self.autostart = autostart
        self.autorestart = autorestart
        self.exitcodes  = exitcodes
        self.startretries = startretries
        self.starttime = starttime
        self.stopsignal = stopsignal
        self.stoptime = stoptime 
        self.redirectstdout = redirectstdout
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
        if env == None:
            self.env = {}
        else:
            self.env = env
        self.state=PROCESS_STATUS.NOTSTARTED.value
        self.dateOfLastStatusChange=datetime.now().ctime()
        self.lastExitCode = 0
    
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
    

    def setStatus(self, newStatus):
        if newStatus not in PROCESS_STATUS:
            raise TypeError("The status could'nt be changed. See ParsingEnum.py/PROCESS_STATUS for available statuses.")
        self.status = newStatus
        self.dateOfLastStatusChange = datetime.now().ctime()

    def getStatus(self):
        if self.status != PROCESS_STATUS.EXCITED.value:
            print(f"{Fore.BLUE}{Style.BRIGHT}[STATUS]{Style.RESET_ALL} {self.name} is currently {Style.BRIGHT}{self.status}{Style.RESET_ALL} since {Style.BRIGHT}{self.dateOfLastStatusChange}{Style.RESET_ALL}.")
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}[STATUS]{Style.RESET_ALL} {self.name} is currently {Style.BRIGHT}{self.status}{Style.RESET_ALL} with code {self.lastExitCode} since {Style.BRIGHT}{self.dateOfLastStatusChange}{Style.RESET_ALL}.")

    def start(self):
        print(f"Start of {self.name}")

    def stop(self):
        print(f"Stop of {self.name}")

    def restart(self):
        print(f"Restart of {self.name}")