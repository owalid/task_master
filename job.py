class Job:
    """Job is a class that contain all the required and optionnal option to do a job inside task_master main program."""
    
    def __init__(self, name, cmd, numprocs = 1, umask = '022', workingdir = '/tmp', autostart = True,
    autorestart = "unexpected", exitcodes = [0, 1], startretries = 3, starttime = 5, stopsignal = 'TERM',
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
