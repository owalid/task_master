import argparse as ap
import os
import sys
import subprocess
import signal
from classes.Server import Server
from argparse import RawTextHelpFormatter
from utils.command import send_result_command
from utils.parsing_conf import parse_job_conf_file, parse_taskmaster_options_conf_file, parse_event_listener_options_conf_file
from utils.check_rights import check_rights_and_user
from classes.ParsingEnum import ERRORS

PID_FILE = "/tmp/taskmaster.pid"

def handle_sigquit(signum, frame):
    server = Server.get_instance()
    server.stop_all_jobs()
    print("SIGKILL received, stopping all jobs.")
    exit(0)

def handle_sighup(signum, frame, conf_path):
    server = Server.get_instance()
    new_list_of_jobs = parse_job_conf_file(conf_path)
    if new_list_of_jobs == False:
        send_result_command(server.connection, ERRORS.CONF_FILE_LOADING_ERROR.value)
        return
    hash_array_new_jobs = []
    for new_job in new_list_of_jobs:
        hash_array_new_jobs.append(new_job.hash)
    hash_array_old_jobs = []
    for old_job in server.jobs:
        if old_job.hash not in hash_array_new_jobs:
            old_job.stop()
            server.jobs.remove(old_job)
        else:
            hash_array_old_jobs.append(old_job.hash)
    is_new_jobs_added  = False
    for new_job in new_list_of_jobs:
        if new_job.hash in hash_array_old_jobs:
            continue
        else:
            server.jobs.append(new_job.__copy__())
            is_new_jobs_added = True
    if is_new_jobs_added:
        server.start_all_jobs()
    del new_list_of_jobs
    if is_new_jobs_added:
        send_result_command(server.connection, "SIGHUP received, jobs started or not touched successfully.")
    else:
        send_result_command(server.connection, "SIGHUP received, but nothing changed.")

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
        print(f"{ERRORS.FORK_ERROR.value}{err}")
        exit(1)

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
        if not os.path.exists(PID_FILE):
            print(ERRORS.PID_FILE_NOT_FOUND.value)
            exit(1)
        with open(PID_FILE, "r") as f:
            pid = f.read()
        name = get_pname(int(pid))

        # protect against killing other process
        if not name.startswith("python3 taskmaster.py") and not name.startswith("python taskmaster.py") and not name.startswith("taskmaster.py"):
            print(ERRORS.PID_ERROR.value)
            exit(1)

        try:
            os.kill(int(pid), signal.SIGQUIT)
            print("Taskmaster killed")
            code = 0
        except:
            print(ERRORS.TM_NOT_RUNNING_ERROR.value)
            code = 1
        exit(code)

    # Load configuration files
    conf_path = args.conf
    jobs = parse_job_conf_file(conf_path)
    if jobs == False:
        print(ERRORS.CONF_FILE_LOADING_ERROR.value)
        exit(1)
    taskmaster_options = parse_taskmaster_options_conf_file(conf_path)
    if taskmaster_options == False:
        print(ERRORS.CONF_FILE_LOADING_ERROR.value)
        exit(1)
    event_listener_options = parse_event_listener_options_conf_file(conf_path)
    if event_listener_options == False:
        print(ERRORS.CONF_FILE_LOADING_ERROR.value)
        exit(1)
    check_rights_and_user(jobs, taskmaster_options, accept_default=args.default)
    server = Server(jobs, event_listener_options)

    # signal.signal(signal.SIGHUP, lambda signum, frame:handle_sighup(signum, frame, conf_path))
    signal.signal(signal.SIGQUIT, handle_sigquit)

    #! THIS CONDITION IS USED ONLY FOR TESTING PURPOSES
    if args.deamonize:
        daemonize()
    
    # write pid of taskmaster in /tmp/taskmaster.pid
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # Start server
    server.start_server()
