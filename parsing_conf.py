#parsing_conf.py
import yaml
import job
def parse_conf_file(conf_path):
    conf_file_loaded = None
    list_of_jobs = []
    name  = ''
    cmd = ''
    try:
        with open(conf_path, 'r') as conf_file:
            conf_file_loaded = yaml.safe_load(conf_file)
    except:
        print("The configuration file at " + conf_path +  " could not be loaded.")
        return False
    allowed_entries = ['cmd', 'numprocs', 'umask', 'workingdir', 'autostart',
    'autorestart', 'exitcodes', 'startretries', 'starttime', 'stopsignal',
    'stoptime', 'stdout', 'stderr', 'env']

    for name_prg, config in conf_file_loaded.items():
        if name_prg != 'program':
            print("The Yaml file should start with \"programs:\"")
            return False
        for cmd, values in config.items():
            print("\n ==== program_name : " + cmd + "====\n")
            for key, values in values.items() : 
                if key not in allowed_entries:
                    return False
                print(key)
                print(values)
                print("\n")
    return conf_file_loaded