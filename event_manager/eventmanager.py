from Event import Event
import time, shutil, os, argparse as ap
from argparse import RawTextHelpFormatter

def compute_raw_file_logs():
    computed_logs = ""
    with open("/tmp/.taskmaster_raw_logs_for_em") as raw_log_file:
        raw_logs = raw_log_file.readlines()
        for raw_log in raw_logs:
            pipe_split = raw_log.split('|')
            event = Event()
            for couple in pipe_split:
                pair = couple.split(':')
                setattr(event, pair[0], pair[1])
            computed_logs += event.make_log()
    filepath = '/tmp/logs_'+ str(event.eventtype)+'.log'
    with open(filepath, "w") as file:
        file.write(computed_logs)
    file.close()
    #send_mail(computed_logs)


def main(mail):
    timer = time.perf_counter()
    while 1:
        if time.perf_counter() - timer >= 20:
            print("Counter is 20")
            timer = time.perf_counter()
            if os.path.exists("/tmp/.taskmaster_raw_logs"):
                print("Path exist")
                print("Copy")
                shutil.copy("/tmp/.taskmaster_raw_logs", "/tmp/.taskmaster_raw_logs_for_em")
                print("Remove raw logs")
                os.remove("/tmp/.taskmaster_raw_logs")
                print("Compute raw logs")
                compute_raw_file_logs()
                print("remove raw logs after computing")
                os.remove("/tmp/.taskmaster_raw_logs_for_em")
            else:
                print("Path not existing")

if __name__ == "__main__":
    parser = ap.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("-m", "--mail", required=True, type=str, help="The mail to send logs to.")
    arg = parser.parse_args()
    mail = arg.mail
    main(mail)