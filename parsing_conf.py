#parsing_conf.py
import yaml
from Job import Job
from ParsingEnum import ALLOWED_ENTRIES
from ParsingEnum import STOP_SIGNAL
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
            current_job = Job(prg, values[ALLOWED_ENTRIES.CMD.value])
            for key, value in values.items() : 
                if key not in ALLOWED_ENTRIES:
                    print(f"\"{key}\" is not an allowed key.")
                    return False
                if key == ALLOWED_ENTRIES.STOPSIGNAL.value and value not in STOP_SIGNAL:
                    print(f"{key}: the value {value} is not allowed for this entry. See Help Page.")
                    return False
                if key == ALLOWED_ENTRIES.UMASK and (value > 511 or value < 0):
                    print(f"{key} should be at least less or equal to 777 and greater than 0.")
                    return False
                setattr(current_job, key, value)
            list_of_jobs.append(current_job)
    # to test
    for job in list_of_jobs:
        job.print_conf()
    return list_of_jobs