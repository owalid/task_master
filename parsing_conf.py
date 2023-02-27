#parsing_conf.py
import yaml
from job import Job
def parse_conf_file(conf_path):
    conf_file_loaded = None
    list_of_jobs = []
    
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
        if name_prg != 'programs':
            print("The Yaml file should start with \"programs\"")
            return False       
        for prg, values in config.items():
            print("\n ==== program_name : " + prg + "====\n")
            dict_job = {'name': None, 'cmd' : None, 'numprocs':None, 'umask':None, 'workingdir':None, 'autostart':None,
            'autorestart':None, 'exitcodes':None, 'startretries':None, 'starttime':None, 'stopsignal':None,
            'stoptime':None, 'stdout':None, 'stderr':None, 'env':None }
            dict_job['name'] = prg
            for key, value in values.items() : 
                if key not in allowed_entries:
                    return False
                dict_job[key] = value
                print(key)
                print ("values :")
                print(value)
                print("\n")
            if dict_job['cmd'] == None or dict_job['name'] == None:
                print("You should at least give a name and a command to execute.")
                return False
            list_of_jobs.append(Job(dict_job['name'], 
                                    dict_job['cmd'],
                                    dict_job['numprocs'],
                                    dict_job['umask'],
                                    dict_job['workingdir'],
                                    dict_job['autostart'],
                                    dict_job['autorestart'],
                                    dict_job['exitcodes'],
                                    dict_job['startretries'],
                                    dict_job['starttime'],
                                    dict_job['stopsignal'],
                                    dict_job['stoptime'],
                                    dict_job['stdout'],
                                    dict_job['stderr'],
                                    dict_job['env']))
    # to test
    # for job in list_of_jobs:
    #     job.print_conf()
    return list_of_jobs