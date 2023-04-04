#parsing_conf.py
import os
import yaml
from classes.Job import Job
from classes.ParsingEnum import ALLOWED_CATEGORIES, ALLOWED_PROGRAM_ENTRIES, ALLOWED_TM_OPTIONS, ALLOWED_EL_OPTIONS, ERRORS, STOP_SIGNAL, RESTART_VALUES
import pwd
from classes.TaskmasterOptions import TaskmasterOptions
from classes.EventManagerOptions import EventManagerOptions
import re

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
    event_listener_options =  EventManagerOptions()
    try:
        with open(conf_path, 'r') as conf_file:
            conf_file_loaded = yaml.safe_load(conf_file)
    except:
        print(ERRORS.CONF_FILE_LOADING_ERROR.value)
        return False
    for name_cat, config in conf_file_loaded.items():
        if name_cat not in ALLOWED_CATEGORIES:
            print(f"{ERRORS.CONF_FILE_BAD_CATEGORY_ERROR.value}{name_cat}")
            return False
        if name_cat != ALLOWED_CATEGORIES.EVENTLISTENER.value:
            continue
        for option, value in config.items():
            if option not in ALLOWED_EL_OPTIONS:
                print(f"{ERRORS.CONF_FILE_BAD_OPTION_ERROR.value}{option} for category {name_cat}.")
                return False
            if option == ALLOWED_EL_OPTIONS.ACTIVATED.value and not isinstance(value, bool):
                print(f"{ERRORS.CONF_FILE_NOT_A_BOOL_ERROR.value}{option}")
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
        print(ERRORS.CONF_FILE_LOADING_ERROR.value)
        return False
    for name_cat, config in conf_file_loaded.items():
        if name_cat not in ALLOWED_CATEGORIES:
            print(f"{ERRORS.CONF_FILE_BAD_CATEGORY_ERROR.value}{name_cat}")
            return False
        if name_cat != ALLOWED_CATEGORIES.TASKMASTEROPTIONS.value:
            continue
        for option, value in config.items():
            if option not in ALLOWED_TM_OPTIONS:
                print(f"{ERRORS.CONF_FILE_BAD_OPTION_ERROR.value}{option} for category {name_cat}.")
                return False
            if option == ALLOWED_TM_OPTIONS.ROOTWARN.value and not isinstance(value, bool):
                print(ERRORS.CONF_FILE_NOT_A_BOOL_ERROR.value)
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
        print(ERRORS.CONF_FILE_LOADING_ERROR.value)
        return False
    for name_prg, config in conf_file_loaded.items():
        if name_prg not in ALLOWED_CATEGORIES:
            print(f"{ERRORS.CONF_FILE_BAD_CATEGORY_ERROR.value}{name_prg}")
            return False
        if name_prg != ALLOWED_CATEGORIES.PROGRAMS.value:
            continue
        for prg, values in config.items():
            if os.path.exists(values[ALLOWED_PROGRAM_ENTRIES.CMD.value]) == False:
                print(f"{ERRORS.NO_SUCH_FILE_ERROR.value}{values[ALLOWED_PROGRAM_ENTRIES.CMD.value]}")
                return False
            current_job, values = init_default_job(prg, values)
            for key, value in values.items() :
                if key not in ALLOWED_PROGRAM_ENTRIES:
                    print(f"{ERRORS.CONF_FILE_BAD_KEY_ERROR.value}\"{key}\"")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.EXITCODES.value:
                    for val in value:
                        if val < 0 or val > 255:
                            print(f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{val} for {key}")
                            return False
                if key == ALLOWED_PROGRAM_ENTRIES.NUMPROCS.value and (value < 1 or value > 10):
                    print(f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{value} for {key}. Min: 1. Max: 10.")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.STOPSIGNAL.value and value not in STOP_SIGNAL:
                    print(f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{value} for {key}")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.UMASK.value and (value > 511 or value < 0):
                    print(f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{value} for {key}.")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.REDIRECTSTDOUT.value and not isinstance(value, bool) \
                or key == ALLOWED_PROGRAM_ENTRIES.REDIRECTSTDERR.value and not isinstance(value, bool):
                    print(f"{ERRORS.CONF_FILE_NOT_A_BOOL_ERROR.value}{key}")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.USER.value:
                    if check_if_user_exists(value) == False:
                        print(f"{ERRORS.CONF_FILE_NO_SUCH_USER.value}{value}")
                        return False
                if key == ALLOWED_PROGRAM_ENTRIES.AUTOSTART.value and not isinstance(value, bool):
                    print(f"{ERRORS.CONF_FILE_NOT_A_BOOL_ERROR.value}{key}")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.AUTORESTART.value and value not in RESTART_VALUES:
                    print(f"{ERRORS.CONF_FILE_BAD_KEY_ERROR.value}{key}")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.STARTRETRIES.value and (value < 0 or value > 10):
                    print(f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{value} for {key}. Min: 0. Max: 10.")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.STARTTIME.value and (value < 0 or value > 60):
                    print(f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{value} for {key}. Min: 0. Max: 60.")
                    return False
                if key == ALLOWED_PROGRAM_ENTRIES.STOPTIME.value and (value < 0 or value > 60):
                    print(f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{value} for {key}. Min: 0. Max: 60.")
                    return False

                setattr(current_job, key, value)
            current_job.stderr = '' if current_job.redirectstderr == False else current_job.stderr
            current_job.stdout = '' if current_job.redirectstdout == False else current_job.stdout
            if current_job.numprocs > 1:
                original_job = current_job.__copy__()
                for i in range(current_job.numprocs):
                    current_job.name = f"{current_job.name}_{i}"
                    list_of_jobs.append(current_job)
                    current_job = original_job.__copy__()
            else:
                list_of_jobs.append(current_job)
    return False if len(list_of_jobs) == 0 else list_of_jobs
