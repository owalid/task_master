import argparse as ap
from server import Server
from argparse import RawTextHelpFormatter
from parsing_conf import parse_conf_file
from ParsingEnum import PROCESS_STATUS

if __name__ == "__main__":
    parser = ap.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("-c", "--conf", required=True, type=str, help='Path of your configuration file')
    args = parser.parse_args()

    # Load configuration file
    conf_path = args.conf
    print(conf_path)
    jobs = parse_conf_file(conf_path)
    if jobs == False:
        print("Error while loading the configuration file.")
        exit(1)

    # Start the main program
    server = Server(jobs)
    server.send_command('nginx', 'start')
