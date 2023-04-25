from enum import Enum, EnumMeta
from colorama import *
import signal

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

class BaseEnum(Enum, metaclass=MetaEnum):
    pass

def extend_join_enums(inherited_enum):
    def wrapper(added_enum):
        joined = {}
        for items in inherited_enum:
            for item in items:
                joined[item.name] = item.value
        for item in added_enum:
            joined[item.name] = item.value
        return BaseEnum(added_enum.__name__, joined)
    return wrapper

class ALLOWED_CATEGORIES(BaseEnum):
    PROGRAMS='programs'
    TASKMASTEROPTIONS='taskmasteroptions'
    EVENTLISTENER='eventlistener'

class RESTART_VALUES(BaseEnum):
    UNEXPECTED='unexpected'
    TRUE=True
    FALSE=False

STOP_SIGNAL = [name for name in signal.Signals.__dict__.keys() if name.startswith('SIG')]

class ALLOWED_PROGRAM_ENTRIES(BaseEnum):
    CMD='cmd'
    USER='user'
    NUMPROCS='numprocs'
    UMASK='umask'
    WORKINGDIR='workingdir'
    AUTOSTART='autostart'
    AUTORESTART='autorestart'
    EXITCODES='exitcodes'
    STARTRETRIES='startretries'
    STARTTIME='starttime'
    STOPSIGNAL='stopsignal'
    STOPTIME='stoptime'
    REDIRECTSTDOUT='redirectstdout'
    STDOUT='stdout'
    REDIRECTSTDERR='redirectstderr'
    STDERR='stderr'
    ENV='env'


class ALLOWED_COMMANDS_WITH_PARAMS(BaseEnum):
    START='start'
    STATUS='status'
    STOP='stop'
    RESTART='restart'
    ATTACH='attach'
    DETACH='detach'

class ALLOWED_COMMANDS_WITHOUT_PARAMS(BaseEnum):
    KILL='kill'
    LIST='list'
    RELOAD='reload'

@extend_join_enums([ALLOWED_COMMANDS_WITHOUT_PARAMS, ALLOWED_COMMANDS_WITH_PARAMS])
class ALLOWED_COMMANDS(BaseEnum):
    pass

class PROCESS_STATUS(BaseEnum):
    NOTSTARTED="Not started"
    STARTED="Started"
    RESTARTED="Restarted"
    STOPPED="Stopped"
    RELOAD="Reload"
    EXITED="Exited"
    ATTACHED="Attached"
    DETACHED="Detached"
    UNKNOWN="Unknown"

class ALLOWED_TM_OPTIONS(BaseEnum):
    ROOTWARN='rootwarn'

class ALLOWED_EL_OPTIONS(BaseEnum):
    ACTIVATED='activated'

class ERRORS(BaseEnum):
    GENERIC_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Error: '
    GENERIC_HARD_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Something went wrong. The program will exit.'
    FORK_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Fork Error: '
    PID_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Pid not corresponding to taskmaster.'
    TM_NOT_RUNNING_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Taskmaster is not running.'
    UNKNOW_SYNTAX_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Unknown Syntax: '
    MISSING_ARGUMENT_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Missing arguments.'
    NO_SUCH_FILE_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} No such file or directory: '
    NOT_A_DIR_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Not a directory: '
    CONNECTION_REFUSED_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Connection refused: '
    CONNECTION_RESET_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Connection reset by peer.'
    BROKEN_PIPE_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Broken pipe.'
    LOG_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The log could not be wrote: '
    PROCESS_FAILED_TO_START_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The following process could not be started: '
    ATTACHED_MODE_ALREADY_RUNNING_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Attach Mode is already running.'
    EVEN_MANAGER_FAILED_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The Event Manager could not be launched: '
    EVENT_MANAGER_FAILED_MAIL_CONNECTION_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} We could not connect to gmail with: '
    EVENT_MANAGER_FAILED_SENDING_MAIL_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} We could not send the mail: '
    ENV_NOT_FOUND_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} .env file not found.'
    ENV_ARG_EMPTY_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} An argument in .env file is empty'
    CONF_FILE_LOADING_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Error while loading the configuration file.'
    CONF_FILE_BAD_CATEGORY_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The following category does not exist: '
    CONF_FILE_BAD_OPTION_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The following option is not allowed: '
    CONF_FILE_NOT_A_BOOL_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The following option should be a boolean: '
    CONF_FILE_BAD_KEY_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The following key is not allowed: '
    CONF_FILE_BAD_VALUE_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The following value is not allowed: '
    CONF_FILE_NO_SUCH_USER=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The following user does not exist: '
    CONF_FILE_DEV_RANDOM_ERROR=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Write to /dev/random or /dev/urandom is a bad idea.'
    CONF_FILE_DUPLICATE_ENTRIES=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Duplicate entries for: '
    CONF_FILE_TOO_MUCH_EXIT_CODE=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Wrong number of entries for exitcodes. Min: 1. Max 255.'
    CONF_FILE_BAD_TYPE=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} Bad type for: '
    NEW_BAD_CONF_FILE=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The new configuration file is not good. Passed configuration will be preserved.'
    PID_FILE_NOT_FOUND=f'{Back.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL} The pid file could not be found.'


# These options are to complex to implement for now.
# I let them here if we need them in the future.
# Currently, we allow only one type of log, PROCESS_STATES.
#     SUBSCRIPTIONS='subscriptions'

# class SUBSCRIPTIONS_CAT(BaseEnum):
#     PROCESS_STATES='PROCESS_STATES'
#     PROCESS_LOGS='PROCESS_LOGS'
