from datetime import datetime
from colorama import Fore, Style
from ParsingEnum import RESTART_VALUES, STOP_SIGNAL, PROCESS_STATUS
import shlex, subprocess

class Job:
    """Job is a class that contains all the required and optional options to do a job inside taskmaster's main program."""

    def __init__(self, name, cmd, user='', numprocs = 1, umask = 18, workingdir = '/tmp', autostart = True,
    autorestart = RESTART_VALUES.UNEXPECTED.value, exitcodes = 0, startretries = 3, starttime = 5, stopsignal = STOP_SIGNAL.TERM.value,
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
    

    def set_status(self, new_status):
        if new_status not in PROCESS_STATUS:
            raise TypeError("The status could'nt be changed. See ParsingEnum.py/PROCESS_STATUS for available statuses.")
        self.state = new_status
        self.date_of_last_status_change = datetime.now().ctime()

    def status(self):
        if self.state != PROCESS_STATUS.EXCITED.value:
            return f"{Fore.BLUE}{Style.BRIGHT}[STATUS]{Style.RESET_ALL} {self.name} is currently {Style.BRIGHT}{self.state}{Style.RESET_ALL} since {Style.BRIGHT}{self.date_of_last_status_change}{Style.RESET_ALL}."
        else:
            return f"{Fore.BLUE}{Style.BRIGHT}[STATUS]{Style.RESET_ALL} {self.name} is currently {Style.BRIGHT}{self.state}{Style.RESET_ALL} with code {self.lastExitCode} since {Style.BRIGHT}{self.date_of_last_status_change}{Style.RESET_ALL}."

    def start(self):
        if self.startretries != -1:
            cmd_split = shlex.split(self.cmd)
            try:
                with open(self.stdout, 'w') as f_out:
                    with open(self.stderr, 'w') as f_err:
                        try:
                            self.process = subprocess.Popen(cmd_split,
                                            env=dict(self.env),
                                            stdout=f_out,
                                            stderr=f_err,
                                            cwd=self.workingdir,
                                            umask=self.umask
                            )
                            self.set_status(PROCESS_STATUS.RUNNING.value)
                        except Exception as e:
                            print(e)
                            self.set_status(PROCESS_STATUS.STOPPED.value)
                            self.startretries -= 1
                            self.set_status(PROCESS_STATUS.RESTARTED.value)
                            self.start()
            except OSError as e:
                print(e)
                self.set_status(PROCESS_STATUS.STOPPED.value)
                self.startretries -= 1
                self.set_status(PROCESS_STATUS.RESTARTED.value)
                self.start()
        else:
            self.set_status(PROCESS_STATUS.EXCITED.value)
        self.startretries  = self.original_startretries          
        return self.status()


    def stop(self):
        self.process.kill()
        self.set_status(PROCESS_STATUS.STOPPED.value)
        return self.status()

    def restart(self):
        self.stop()
        self.set_status(PROCESS_STATUS.RESTARTED.value)
        self.start()
        return self.status()
