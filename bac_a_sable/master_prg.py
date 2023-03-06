import subprocess

timer=30
handshakedone=False
while timer:
    process = subprocess.Popen(["python3", "event.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error=0
    if handshakedone == False:
        print("Handshake")
        hand="AUREADY\n"
        process.stdin.write(hand.encode())
        process.stdin.flush()
        shake = process.stdout.readline().decode().strip()
        match shake:
            case "READY":
                print("Ready")
                handshakedone = True
            case "BUSY":
                error += 1
                continue
            case _:
                error += 1
                continue
    if handshakedone == True:
        print("Dans handshake true")
        log="toto et titi sont dans un bateau...$"
        payload="BEGIN\n"
        process.stdin.write(payload.encode())
        process.stdin.flush()
        res = process.stdout.readline().decode().strip()
        print("RES " + res)
        payload="server:taskmaster|processname:cat|processcmd:cat -e toto.txt|pid:32178|eventtype:PROCESS_LOGS|eventsubtype:PROCESS_LOGS_STDOUT|eventid:13587410|payload:"+ log +"\n"
        process.stdin.write(payload.encode())
        process.stdin.flush()
        res = process.stdout.readline().decode().strip()
        payload="END\n"
        process.stdin.write(payload.encode())
        process.stdin.flush()
        res = process.stdout.readline().decode().strip()
        print("res end = " + res)
        if res == "OK":
            print("Prout")
        elif res == "ERROR":
            print("There is an error. The log could not be created")
    process.stdin.close()
    process.stdout.close()
    timer -= 1