from Event import Event
import time, datetime, shutil, os,  yagmail, dotenv, sys


def send_mail(filepath):
    env = dotenv.dotenv_values()
    if env == None:
        print("No .env file. Misconfiguration ?")
        return
    try:
        mail = env.get("USERMAIL")
        pswd = env.get("PASSWORD")
        if mail == None or pswd == None:
            print("An argument is empty in .env. Misconfiguration ?")
            return 
        yag = yagmail.SMTP(mail, pswd)
        print("Connection ok with google server.")
    except Exception as e:
        print(f"Could not connect to mail {mail} " + e)
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
        print(f'Could not send the mail. ' + e)

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
        print(e)
    return filepath

def main():
    timer = time.perf_counter()
    while 1:
        if time.perf_counter() - timer >= 20:
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