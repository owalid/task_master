#parsing_conf.py
import yaml
from Job import Job
from ParsingEnum import ALLOWED_ENTRIES
from ParsingEnum import STOP_SIGNAL
import pwd

def init_default_job(prg, values):
    have_env_in_conf = ALLOWED_ENTRIES.ENV.value in values.keys()
    env = values[ALLOWED_ENTRIES.ENV.value] if have_env_in_conf else {}
    current_job = Job(prg, values[ALLOWED_ENTRIES.CMD.value], env=env)
    del values[ALLOWED_ENTRIES.CMD.value]
    if have_env_in_conf:
        del values[ALLOWED_ENTRIES.ENV.value]

    return (current_job, values)

def check_if_user_exists(username):
    if not isinstance(username, str) or username.lower() == 'root':
        return False
    try:
        pwd.getpwnam(username)
    except KeyError:
        return False
    return True

def parse_conf_file(conf_path):
    conf_file_loaded = None
    list_of_jobs = []   
    try:
        with open(conf_path, 'r') as conf_file:
            conf_file_loaded = yaml.safe_load(conf_file)
    except:
        print("The configuration file at " + conf_path +  " could not be loaded.")
        return False
    for name_prg, config in conf_file_loaded.items():
        if name_prg != 'programs':
            print("The Yaml file should start with \"programs\"")
            return False       
        for prg, values in config.items():
            current_job, values = init_default_job(prg, values)
            for key, value in values.items() : 
                if key not in ALLOWED_ENTRIES:
                    print(f"\"{key}\" is not an allowed key.")
                    return False
                if key == ALLOWED_ENTRIES.STOPSIGNAL.value and value not in STOP_SIGNAL:
                    print(f"{key}: the value {value} is not allowed for this entry. See Help Page.")
                    return False
                if key == ALLOWED_ENTRIES.UMASK.value and (value > 511 or value < 0):
                    print(f"{key} should be at least less or equal to 777 and greater than 0.")
                    return False
                if key == ALLOWED_ENTRIES.REDIRECTSTDOUT.value and not isinstance(value, bool) \
                or key == ALLOWED_ENTRIES.REDIRECTSTDERR.value and not isinstance(value, bool):
                    print(f"{key} should be a boolean not {value}.")
                    return False
                if key == ALLOWED_ENTRIES.USER.value:
                    if check_if_user_exists(value) == False:
                        print(f"The user {value} does'nt exist or is not permitted. Please put a valid user.")
                        return False
                setattr(current_job, key, value)
            list_of_jobs.append(current_job)
    return list_of_jobs