from enum import Enum, EnumMeta
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

class ALLOWED_COMMANDS(BaseEnum):
    START='start'
    STATUS='status'
    STOP='stop'
    RESTART='restart'

class PROCESS_STATUS(BaseEnum):
    NOTSTARTED="Not started"
    STARTED="Started"
    RUNNING="Running"
    RESTARTED="Restarted"
    STOPPED="Stopped"
    EXCITED="Excited"
    UNKNOWN="Unknown"

class ALLOWED_TM_OPTIONS(BaseEnum):
    ROOTWARN='rootwarn'

class ALLOWED_EL_OPTIONS(BaseEnum):
    ACTIVATED='activated'

# These options are to complex to implement for now.
# I let them here if we need them in the future.
# Currently, we allow only one type of log, PROCESS_STATES.
#     SUBSCRIPTIONS='subscriptions'

# class SUBSCRIPTIONS_CAT(BaseEnum):
#     PROCESS_STATES='PROCESS_STATES'
#     PROCESS_LOGS='PROCESS_LOGS'
