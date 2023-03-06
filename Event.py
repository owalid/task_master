from datetime import datetime

class Event:
    def __init__(self, server="taskmaster", processname="", processcmd="", pid=0, eventtype="", eventsubtype="", eventid=0, payload=""):
        self.server=server
        self.processname=processname
        self.processcmd=processcmd
        self.pid=pid
        self.eventtype=eventtype
        self.eventsubtype=eventsubtype
        self.eventdate=datetime.now().ctime()
        self.eventid=eventid
        self.payload= payload
        
    def make_log(self):
        log = "\n===== BEGIN LOG ID : " +  str(self.eventid) + " =====\n"
        log += "Event Date : " + str(self.eventdate) + "\n"
        log += "Process Name: " + self.processname + "\n"
        log += "Command : " + self.processcmd + "\n"
        log += "PID : " + self.pid + "\n"
        log += "Event type : " + self.eventtype + "\n"
        log += "Event subtype : " + self.eventsubtype + "\n"
        log += "Datas : " + self.payload + "\n"
        log += "===== END LOG ID : " + str(self.eventid) + " =====\n"
        return log
        