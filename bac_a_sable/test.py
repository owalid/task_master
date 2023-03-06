from Event import Event

def compute_payload(payload):
    pipe_split = payload.split('|')
    event = Event()
    for couple in pipe_split:
        pair = couple.split(':')
        print(couple)
        print(pair)
        setattr(event, pair[0], pair[1])
    to_write = event.make_log()
    filepath = '/tmp/logs_'+ str(event.eventsubtype)+'.log'
    print(event.make_log())
    with open(filepath, "w") as file:
        file.write(to_write)
    file.close()

payload="server:taskmaster|processname:cat|processcmd:cat -e toto.txt|pid:32178|eventtype:PROCESS_LOGS|eventsubtype:PROCESS_LOGS_STDOUT|date:10/22/2023-13h52.00|eventid:13587410|payload:toto et titi sont dans un bateau...$\n"
compute_payload(payload)