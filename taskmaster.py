import argparse as ap
import os, sys
from server import Server
from argparse import RawTextHelpFormatter
from parsing_conf import parse_job_conf_file, parse_taskmaster_options_conf_file, parse_event_listener_options_conf_file
from check_rights import check_rights_and_user

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
    parser.add_argument("-c", "--conf", required=True, type=str, help='Path of your configuration file')

    #! THIS OPTIONS IS USED ONLY FOR TESTING PURPOSES
    parser.add_argument("-d", "--deamonize", required=False, action='store_true', default=False, help='Deamonize')

    args = parser.parse_args()

    # Load configuration file
    conf_path = args.conf
    print(conf_path)
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
    check_rights_and_user(jobs, taskmaster_options)

    #! THIS CONDITION IS USED ONLY FOR TESTING PURPOSES
    if args.deamonize:
        daemonize()
    # Start the main program
    server = Server(jobs, event_listener_options)
