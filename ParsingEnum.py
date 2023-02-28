from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True    


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


class RESTART_VALUES(BaseEnum):
    UNEXPECTED='unexpected'
    TRUE='true'
    FALSE='false'

class STOP_SIGNAL(BaseEnum):
    TERM='TERM'
    HUP='HUP'
    INT='INT'
    QUIT='QUIT'
    KILL='KILL'
    USR1='USR1'
    USR2='USR2'

class ALLOWED_ENTRIES(BaseEnum):
    CMD='cmd'
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
    STDOUT='stdout'
    STDERR='stderr'
    ENV='env'
