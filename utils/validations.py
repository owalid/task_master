from classes.ParsingEnum import ALLOWED_PROGRAM_ENTRIES, ALLOWED_TM_OPTIONS, ALLOWED_EL_OPTIONS, ERRORS, STOP_SIGNAL, RESTART_VALUES
import pwd
import os

def check_if_user_exists(username):
    if not isinstance(username, str) or username.lower() == 'root':
        return False
    try:
        pwd.getpwnam(username)
    except KeyError:
        return False
    return True

def have_duplicates(list):
    checkList = {}
    for item in list:
        if item in checkList:
            return True
        checkList[item] = True
    return False

VALIDATION_DICT = {
    ALLOWED_PROGRAM_ENTRIES.CMD.value: {
        'type_rule_fn': lambda x: isinstance(x, int) and not isinstance(x, bool),
        'main_rules': []
    },
    ALLOWED_PROGRAM_ENTRIES.USER.value: {
        'type_rule_fn': lambda x: isinstance(x, str),
        'main_rules': [
            {
                'rule_fn': lambda x: check_if_user_exists(x),
                'msg_fn': lambda x: f"{ERRORS.CONF_FILE_NO_SUCH_USER.value}{x}"
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.NUMPROCS.value: {
        'type_rule_fn': lambda x: isinstance(x, int) and not isinstance(x, bool),
        'main_rules': [
            {
                'rule_fn': lambda x: x > 1 and x < 10,
                'msg_fn': lambda x: f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{x} for {ALLOWED_PROGRAM_ENTRIES.NUMPROCS.value}. Min: 1. Max: 10."
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.UMASK.value: {
        'type_rule_fn': lambda x: isinstance(x, int) and not isinstance(x, bool),
        'main_rules': [
            {
                'rule_fn': lambda x: x > 0 and x < 511,
                'msg_fn': lambda x: f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{x} for {ALLOWED_PROGRAM_ENTRIES.UMASK.value}. Min: 1. Max: 511."
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.WORKINGDIR.value: {
        'type_rule_fn': lambda x: isinstance(x, str),
        'main_rules': [
            {
                'rule_fn': lambda x: os.path.exists(os.path.dirname(x)) != False,
                'msg_fn': lambda x: f'{ERRORS.NO_SUCH_FILE_ERROR.value}{x}'
            },
            {
                'rule_fn': lambda x: os.path.isdir(x) != False,
                'msg_fn': lambda x: f'{ERRORS.NOT_A_DIR_ERROR.value}{x}'
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.AUTOSTART.value: {
        'type_rule_fn': lambda x: isinstance(x, bool),
        'main_rules': []
    },
    ALLOWED_PROGRAM_ENTRIES.AUTORESTART.value: {
        'type_rule_fn': lambda x: isinstance(x, bool) or isinstance(x, str),
        'main_rules': [
            {
                'rule_fn': lambda x: x in RESTART_VALUES,
                'msg_fn': lambda x: f"{ERRORS.CONF_FILE_BAD_KEY_ERROR.value}{ALLOWED_PROGRAM_ENTRIES.AUTORESTART.value}"
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.EXITCODES.value: {
        'type_rule_fn': lambda x: isinstance(x, list) and len([val for val in x if isinstance(val, int)]) == len(x),
        'main_rules': [
            {
                'rule_fn': lambda x: [len(x) < 255 or len(x) > 1],
                'msg_fn': lambda x: ERRORS.CONF_FILE_TOO_MUCH_EXIT_CODE.value
            },
            {
                'rule_fn': lambda x: not have_duplicates(x),
                'msg_fn': lambda x: f'{ERRORS.CONF_FILE_DUPLICATE_ENTRIES.value}{x}'
            },
            {
                'rule_fn': lambda x: len([val for val in x if val > 0 or val < 255]) == len(x),
                'msg_fn': lambda x: f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{x} for {ALLOWED_PROGRAM_ENTRIES.EXITCODES.value}"
            },
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.STARTRETRIES.value: {
        'type_rule_fn': lambda x: isinstance(x, int) and not isinstance(x, bool),
        'main_rules': [
            {
                'rule_fn': lambda x: x > 0 and x < 10,
                'msg_fn': lambda x: f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{x} for {ALLOWED_PROGRAM_ENTRIES.NUMPROCS.value}. Min: 1. Max: 10."
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.STARTTIME.value: {
        'type_rule_fn': lambda x: isinstance(x, int) and not isinstance(x, bool),
        'main_rules': [
            {
                'rule_fn': lambda x: x > 0 and x < 60,
                'msg_fn': lambda x: f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{x} for {ALLOWED_PROGRAM_ENTRIES.STARTTIME.value}. Min: 0. Max: 60."
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.STOPSIGNAL.value: {
        'type_rule_fn': lambda x: isinstance(x, str),
        'main_rules': [
            {
                'rule_fn': lambda x: x in STOP_SIGNAL,
                'msg_fn': lambda x: f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{x} for {ALLOWED_PROGRAM_ENTRIES.STOPSIGNAL.value}"
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.STOPTIME.value: {
        'type_rule_fn': lambda x: isinstance(x, int) and not isinstance(x, bool),
        'main_rules': [
            {
                'rule_fn': lambda x: x > 0 and x < 60,
                'msg_fn': lambda x: f"{ERRORS.CONF_FILE_BAD_VALUE_ERROR.value}{x} for {ALLOWED_PROGRAM_ENTRIES.STOPTIME.value}. Min: 0. Max: 60."
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.REDIRECTSTDOUT.value: {
        'type_rule_fn': lambda x: isinstance(x, bool),
        'main_rules': []
    },
    ALLOWED_PROGRAM_ENTRIES.STDOUT.value: {
        'type_rule_fn': lambda x: isinstance(x, str),
        'main_rules': [
            {
                'rule_fn': lambda x: x != '/dev/random' and x != '/dev/urandom',
                'msg_fn': lambda x: ERRORS.CONF_FILE_DEV_RANDOM_ERROR.value
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.REDIRECTSTDERR.value: {
        'type_rule_fn': lambda x: isinstance(x, bool),
        'main_rules': []
    },
    ALLOWED_PROGRAM_ENTRIES.STDERR.value: {
        'type_rule_fn': lambda x: isinstance(x, str),
        'main_rules': [
            {
                'rule_fn': lambda x: x != '/dev/random' and x != '/dev/urandom',
                'msg_fn': lambda x: ERRORS.CONF_FILE_DEV_RANDOM_ERROR.value
            }
        ]
    },
    ALLOWED_PROGRAM_ENTRIES.ENV.value: {
        'type_rule_fn': lambda x: isinstance(x, int) and not isinstance(x, bool),
        'main_rules': []
    },
    ALLOWED_TM_OPTIONS.ROOTWARN.value: {
        'type_rule_fn': lambda x: isinstance(x, bool),
        'main_rules': []
    },
    ALLOWED_EL_OPTIONS.ACTIVATED.value: {
        'type_rule_fn': lambda x: isinstance(x, bool),
        'main_rules': []
    },
}