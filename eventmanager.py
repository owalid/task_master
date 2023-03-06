from Event import Event
import sys

def compute_payload(payload):
    pipe_split = payload.split('|')
    event = Event()
    for couple in pipe_split:
        pair = couple.split(':')
        setattr(event, pair[0], pair[1])
    to_write = event.make_log()
    filepath = '/tmp/logs_'+ str(event.eventsubtype)+'.log'
    with open(filepath, "a") as file:
        file.write(to_write)
    file.close()

while 1:
    value = input()
    match value:
        case "AUREADY":
            print("READY\n")
        case "BEGIN":
            print("Computing = true\n")
            to_write = input()
            compute_payload(to_write)
            end = input()
            if end == "END":
                print("OK\n")
            else:
                print("ERROR\n")
        case _:
            continue
    