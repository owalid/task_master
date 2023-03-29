import argparse as ap
from subprocess import check_output
import os, sys
import subprocess
import signal
from classes.Server import Server
from argparse import RawTextHelpFormatter
from utils.parsing_conf import parse_job_conf_file, parse_taskmaster_options_conf_file, parse_event_listener_options_conf_file
from utils.check_rights import check_rights_and_user


PID_FILE = "/tmp/taskmaster.pid"

def handle_sigquit(signum, frame):
    server = Server.get_instance()
    server.stop_all_jobs()
    print("SIGKILL received, stopping all jobs.")
    exit(0)

def handle_sighup(signum, frame):
    server = Server.get_instance()
    server.start_all_jobs()
    print("SIGHUP received, restarting all jobs.")

def get_pname(pid):
    p = subprocess.Popen(["ps -o cmd= {}".format(pid)], stdout=subprocess.PIPE, shell=True)
    return p.communicate()[0].decode().strip()

def daemonize():
    '''
        Daemonize the process, it used in the main function
    '''
    try:
        if os.fork() > 0:
            exit(0)
    except OSError as err:
        print(f"Fork error: {err}")
        exit(1)

    os.chdir('/') # change directory to root
    os.setsid() # change session id of process
    os.umask(0) # change permission mask of process

    # get fd of /dev/null
    new_stdin = open("/dev/null", "r")
    new_stdout = open("/dev/null", "w")
    new_stderr = open("/dev/null", "w")

    # duplicate fd of /dev/null to stdin, stdout and stderr
    os.dup2(new_stdin.fileno(), sys.stdin.fileno())
    os.dup2(new_stdout.fileno(), sys.stdout.fileno())
    os.dup2(new_stderr.fileno(), sys.stderr.fileno())

if __name__ == "__main__":
    parser = ap.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("-c", "--conf", required=False, type=str, help='Path of your configuration file')
    parser.add_argument("-k", "--kill", required=False, action='store_true', default=False, help='Kill taskmaster')
    parser.add_argument("-df", "--default",  required=False, action='store_true', default=False, help='Use default value of all the questions asked by the program')

    #! THIS OPTIONS IS USED ONLY FOR TESTING PURPOSES
    parser.add_argument("-d", "--deamonize", required=False, action='store_true', default=False, help='Deamonize')

    args = parser.parse_args()

    print(args)
    if not args.conf and not args.kill:
        parser.print_help()
        exit(1)

    if args.kill:
        # get pid of taskmaster
        with open("/tmp/taskmaster.pid", "r") as f:
            pid = f.read()
        name = get_pname(int(pid))

        # protect against killing other process
        if not name.startswith("python3 taskmaster.py") and not name.startswith("python taskmaster.py") and not name.startswith("taskmaster.py"):
            print("Pid not corresponding to taskmaster")
            exit(1)

        try:
            os.kill(int(pid), signal.SIGQUIT)
            print("Taskmaster killed")
            code = 0
        except:
            print("Taskmaster is not running")
            code = 1
        exit(code)

    # Load configuration files
    conf_path = args.conf
    jobs = parse_job_conf_file(conf_path)
    if jobs == False:
        print("Error while loading the configuration file.")
        exit(1)
    taskmaster_options = parse_taskmaster_options_conf_file(conf_path)
    if taskmaster_options == False:
        print("Error while loading the configuration file.")
        exit(1)
    event_listener_options = parse_event_listener_options_conf_file(conf_path)
    if event_listener_options == False:
        print("Error while loading the configuration file.")
        exit(1)
    check_rights_and_user(jobs, taskmaster_options, accept_default=args.default)
    server = Server(jobs, event_listener_options)
    
    # write pid of taskmaster in /tmp/taskmaster.pid
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    signal.signal(signal.SIGHUP, handle_sighup)
    signal.signal(signal.SIGQUIT, handle_sigquit)

    #! THIS CONDITION IS USED ONLY FOR TESTING PURPOSES
    if args.deamonize:
        daemonize()
    # Start server
    server.start_server()
