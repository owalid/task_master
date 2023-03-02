#parsing_conf.py
import yaml
from Job import Job
from ParsingEnum import ALLOWED_CATEGORIES, ALLOWED_PROGRAM_ENTRIES, ALLOWED_TM_OPTIONS, ALLOWED_EL_OPTIONS,SUBSCRIPTIONS_CAT, STOP_SIGNAL
import pwd
from TaskmasterOptions import TaskmasterOptions
from EventListenerOptions import EventListenerOptions

def init_default_job(prg, values):
    have_env_in_conf = ALLOWED_PROGRAM_ENTRIES.ENV.value in values.keys()
    env = values[ALLOWED_PROGRAM_ENTRIES.ENV.value] if have_env_in_conf else {}
    current_job = Job(prg, values[ALLOWED_PROGRAM_ENTRIES.CMD.value], env=env)
    del values[ALLOWED_PROGRAM_ENTRIES.CMD.value]
    if have_env_in_conf:
        del values[ALLOWED_PROGRAM_ENTRIES.ENV.value]

    return (current_job, values)

def check_if_user_exists(username):
    if not isinstance(username, str) or username.lower() == 'root':
        return False
    try:
        pwd.getpwnam(username)
    except KeyError:
        return False
    return True

def parse_event_listener_options_conf_file(conf_path):
    conf_file_loaded = None
    event_listener_options =  EventListenerOptions() 
    try:
        with open(conf_path, 'r') as conf_file:
            conf_file_loaded = yaml.safe_load(conf_file)
    except:
        print("The configuration file at " + conf_path +  " could not be loaded.")
        return False
    for name_cat, config in conf_file_loaded.items():
        if name_cat not in ALLOWED_CATEGORIES:
            print(f"{name_cat} is not an allowed category for the configuration file.")
            return False
        if name_cat != ALLOWED_CATEGORIES.EVENTLISTENER.value:
            continue
        for option, value in config.items():
            if option not in ALLOWED_EL_OPTIONS:
                print(f"{option} is not an allowed option for {name_cat}.")
                return False
            if option == ALLOWED_EL_OPTIONS.ACTIVATED.value and not isinstance(value, bool):
                print(f"{option} should be a boolean not {value}")
                return False
            if option == ALLOWED_EL_OPTIONS.SUBSCRIPTIONS.value and len([val for val in value if val not in SUBSCRIPTIONS_CAT]):
                print(f"{option} can't be {value}.")
                return False
            setattr(event_listener_options, option, value)
    return event_listener_options

def parse_taskmaster_options_conf_file(conf_path):
    conf_file_loaded = None
    taskmaster_options =  TaskmasterOptions() 
    try:
        with open(conf_path, 'r') as conf_file:
            conf_file_loaded = yaml.safe_load(conf_file)
    except:
        print("The configuration file at " + conf_path +  " could not be loaded.")
        return False
    for name_cat, config in conf_file_loaded.items():
        if name_cat not in ALLOWED_CATEGORIES:
            print(f"{name_cat} is not an allowed category for the configuration file.")
            return False
        if name_cat != ALLOWED_CATEGORIES.TASKMASTEROPTIONS.value:
            continue
        for option, value in config.items():
            if option not in ALLOWED_TM_OPTIONS:
                print(f"{option} is not an allowed entry for {name_cat}.")
                return False
            if option == ALLOWED_TM_OPTIONS.ROOTWARN.value and not isinstance(value, bool):
                print(f"{option} should be a boolean not {value}")
                return False
            setattr(taskmaster_options, option, value)
    return taskmaster_options


def parse_job_conf_file(conf_path):
    conf_file_loaded = None
    list_of_jobs = []   
    try:
        with open(conf_path, 'r') as conf_file:
            conf_file_loaded = yaml.safe_load(conf_file)
    except:
        print("The configuration file at " + conf_path +  " could not be loaded.")
        return False
    for name_prg, config in conf_file_loaded.items():
        if name_prg not in ALLOWED_CATEGORIES:
            print(f"{name_prg} is not an allowed category for the configuration file.")
            return False
        if name_prg != ALLOWED_CATEGORIES.PROGRAMS.value:
            continue
        for prg, values in config.items():
            current_job, values = init_default_job(prg, values)
            for key, value in values.items() : 
                if key not in ALLOWED_PROGRAM_ENTRIES:
                    print(f"\"{key}\" is not an allowed key.")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.STOPSIGNAL.value and value not in STOP_SIGNAL:
                    print(f"{key}: the value {value} is not allowed for this entry. See Help Page.")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.UMASK.value and (value > 511 or value < 0):
                    print(f"{key} should be at least less or equal to 777 and greater than 0.")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.REDIRECTSTDOUT.value and not isinstance(value, bool) \
                or key == ALLOWED_PROGRAM_ENTRIES.REDIRECTSTDERR.value and not isinstance(value, bool):
                    print(f"{key} should be a boolean not {value}.")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.USER.value:
                    if check_if_user_exists(value) == False:
                        print(f"The user {value} does'nt exist or is not permitted. Please put a valid user.")
                        return False
                setattr(current_job, key, value)
            list_of_jobs.append(current_job)
    return False if len(list_of_jobs) == 0 else list_of_jobs