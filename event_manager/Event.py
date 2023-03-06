from datetime import datetime
import base64
class Event:
    def __init__(self, server="taskmaster", eventid="", date="", processname="", processcmd="", eventtype="PROCESS_STATES",
                 fromstate="", tostate="", lastexitcode=0):
        self.server=server
        self.eventid=eventid
        self.date = date
        self.processname=processname
        self.processcmd=processcmd
        self.eventtype=eventtype
        self.fromstate=fromstate
        self.tostate=tostate
        self.lastexitcode=lastexitcode

    def make_log(self):
        log = "\n===== BEGIN LOG ID : " +  str(self.eventid) + " =====\n"
        log += "Event Date : " + base64.b64decode(self.date.encode()).decode() + "\n"
        log += "Process Name: " + self.processname + "\n"
        log += "Command : " + self.processcmd + "\n"
        log += "Event type : " + self.eventtype + "\n"
        log += "From State : " + self.fromstate + "\n"
        log += "To State : " + self.tostate + "\n"
        log += "Last exit code : " + str(self.lastexitcode) + "\n"
        log += "===== END LOG ID : " + str(self.eventid) + " =====\n"
        return log
        