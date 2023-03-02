import argparse as ap
from server import Server
from argparse import RawTextHelpFormatter
from parsing_conf import parse_job_conf_file, parse_taskmaster_options_conf_file
from check_rights import check_rights_and_user
import os
if __name__ == "__main__":
    parser = ap.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("-c", "--conf", required=True, type=str, help='Path of your configuration file')
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
    # event_listener = parse_event_listener_conf_file(conf_path)
    check_rights_and_user(jobs, taskmaster_options)
    # Start the main program
    server = Server(jobs)
    server.send_command('nginx', 'start')
    server.send_command('nginx', 'get_status')
    server.send_command('nginx', 'stop')
    server.send_command('nginx', 'get_status')
    server.send_command('nginx', 'restart')
    server.send_command('nginx', 'get_status')
    server.send_command('nginx', 'stop')
    server.send_command('nginx', 'get_status')
