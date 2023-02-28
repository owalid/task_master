from ParsingEnum import RESTART_VALUES
from ParsingEnum import STOP_SIGNAL

class Job:
    """Job is a class that contains all the required and optional options to do a job inside taskmaster's main program."""
    
    def __init__(self, name, cmd, numprocs = 1, umask = 18, workingdir = '/tmp', autostart = True,
    autorestart = RESTART_VALUES.UNEXPECTED.value, exitcodes = 0, startretries = 3, starttime = 5, stopsignal = STOP_SIGNAL.TERM.value,
    stoptime = 10, stdout=None, stderr=None, env=None):
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
        if stdout == None:
            self.stdout = '/tmp/' + self.name + '.stdout'
        else :
            self.stdout = stdout
        if stderr == None:
            self.stderr = '/tmp/' + self.name + '.stderr'
        else:
            self.stderr = stderr
        if env == None:
            self.env = {}
        else:
            self.env = env
    
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
        print("stdout : " + self.stdout)
        print("stderr : " + self.stderr)
        print("env : ")
        for key, value in self.env.items():
            print(" ",key , ": ", value)
    
    def status(self):
        print(f"Status of {self.name}")

    def start(self):
        print(f"Start of {self.name}")

    def stop(self):
        print(f"Stop of {self.name}")

    def restart(self):
        print(f"Restart of {self.name}")