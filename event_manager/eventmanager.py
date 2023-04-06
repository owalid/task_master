from Event import Event
import time, datetime, shutil, os,  yagmail, dotenv, sys
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from classes.ParsingEnum import ERRORS

def send_mail(filepath):
    env = dotenv.dotenv_values()
    if env == None:

        print(ERRORS.ENV_NOT_FOUND_ERROR.value)
        return
    try:
        mail = env.get("USERMAIL")
        pswd = env.get("PASSWORD")
        if mail == None or pswd == None:
            print(ERRORS.ENV_ARG_EMPTY_ERROR.value)
            return
        yag = yagmail.SMTP(mail, pswd)
        print("Connection ok with google server.")
    except Exception as e:
        print(f"{ERRORS.EVENT_MANAGER_FAILED_MAIL_CONNECTION_ERROR.value}{mail} {e}")
        return
    try:
        yag.send(
            to=mail,
            subject="Hourly report from taskmaster application " + str(datetime.datetime.now()),
            contents="Find your hourly report from your taskmaster application on the file attached bellow.",
            attachments=[filepath]
            )
        print("File sent\n")
    except Exception as e:
        print(f'{ERRORS.EVENT_MANAGER_FAILED_SENDING_MAIL_ERROR.value}{e}')

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
    filepath = '/tmp/logs_'+ str(event.eventtype) + '_' + str(datetime.datetime.now()).translate(str.maketrans({' ':'_'}))   + '.log'
    try:
        with open(filepath, "w") as log:
            log.write(computed_logs)
        log.close()
        with open(sys.path[0] + "/../logs/taskmaster_computed_logs.log", "a") as computed_file:
            computed_file.write(computed_logs)
        computed_file.close()
    except Exception as e:
        print(f'{ERRORS.GENERIC_ERROR.value}{e}')
    return filepath

def main():
    env = dotenv.dotenv_values()
    cycle = int(env.get("CYCLE"))
    if  not isinstance(cycle, int):
        exit(1)
    if cycle == None:
        cycle = 600
    if cycle < 20 or cycle > 31536000:
        exit(1)
    timer = time.perf_counter()
    while 1:
        if time.perf_counter() - timer >= cycle:
            print("Counter OK")
            timer = time.perf_counter()
            if os.path.exists("/tmp/.taskmaster_raw_logs"):
                print("Path exists")
                shutil.copy("/tmp/.taskmaster_raw_logs", "/tmp/.taskmaster_raw_logs_for_em")
                os.remove("/tmp/.taskmaster_raw_logs")
                logpath = compute_raw_file_logs()
                send_mail(logpath)
                os.remove("/tmp/.taskmaster_raw_logs_for_em")
            else:
                print("No logs.")

if __name__ == "__main__":
    main()
