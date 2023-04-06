from classes.Client import Client
from utils.command import parse_command
from classes.ParsingEnum import ALLOWED_COMMANDS, ALLOWED_COMMANDS_WITH_PARAMS, ALLOWED_COMMANDS_WITHOUT_PARAMS, ERRORS
import signal
import sys

LISTED_JOBS = []

def signal_handler(signal, frame):
    global detachMode
    detachMode = True

def clean_exit(client):
    client.close()
    print("Bye")
    exit(0)

def update_listed_jobs():
    global LISTED_JOBS
    client = Client.get_instance()
    client.send(f"list")
    listed_jobs = client.receive()
    LISTED_JOBS = listed_jobs.split('\n')
    LISTED_JOBS.append("all")

def completer(text, state):
    # Get current input to know if we are completing a command
    current_input = readline.get_line_buffer()
    if current_input:
        current_input = readline.get_line_buffer().split(" ")[0]
    if current_input in ALLOWED_COMMANDS_WITHOUT_PARAMS: # No autocompletion for commands without params
        return None
    if current_input in ALLOWED_COMMANDS_WITH_PARAMS: # Try to complete a jobname
        options = [job for job in LISTED_JOBS if job.startswith(text)]
    else: # Try to complete a command
        options = [cmd.value for cmd in ALLOWED_COMMANDS if cmd.value.startswith(text)]

    if state < len(options):
        return options[state]
    else:
        return None

def display_help():
    print('''commands:
=============================================
quit      exit      stop     start    status
restart   attach    detach   list     kill
=============================================''')
if __name__ == "__main__":
    client = Client()
    import readline # this is for the history and autocompletion of the commands
    readline.parse_and_bind("tab:complete")
    readline.set_completer(completer)
    while True:
        try:
            update_listed_jobs() # Update the list of jobs
            cmd = input('taskmaster> ')
            # Parse help, exit and quit command
            if cmd == 'help':
                display_help()
                continue
            elif cmd == 'quit' or cmd == 'exit':
                clean_exit(client)

            # Parse commands
            (cmd_parsed, arguments) = parse_command(cmd)

            if cmd_parsed == 'kill':
                res = input("Are you sure you want to kill all processes and taskmaster? (Y/n) ")
                res = res.lower()

                if res == 'y' or res == 'yes' or res == '':
                    print("Killing all processes and taskmaster...")
                    client.send(f"kill")
                    print("Bye")
                    exit(0)
            if cmd_parsed == 'list':
                client.send(f"list")
                print(client.receive())
                continue

            if cmd_parsed == False: # invalid command
                print(f"{ERRORS.UNKNOW_SYNTAX_ERROR.value}{cmd}")
                continue
            elif not arguments:
                print(ERRORS.MISSING_ARGUMENT_ERROR.value)
                print("<command> <job_name or 'all'>")
                continue
            elif client.client_socket == None: # Try to connect to server if not connected
                client = Client()
            if client.client_socket != None: # If connected send command to server
                # todo: process arguments according to command and server
                if cmd_parsed ==  ALLOWED_COMMANDS.ATTACH.value:
                    client.send(f"{cmd_parsed} {arguments}")
                    signal.signal(signal.SIGINT, signal_handler)
                    detachMode = False
                    print("Press Ctrl + c to quit attach mode")
                    while True:
                        data = client.receive()
                        if (data is not None):
                            print(data)
                        if detachMode == True:
                            break
                    client.send(f"{ALLOWED_COMMANDS.DETACH.value} {arguments}")
                    print(client.receive())
                elif cmd_parsed == ALLOWED_COMMANDS.RESTART.value:
                    client.send(f"{cmd_parsed} {arguments}")
                    print(client.receive())
                else:
                    client.send(f"{cmd_parsed} {arguments}")
                    print(client.receive())
        except KeyboardInterrupt:
            print('')
            clean_exit(client)
        except EOFError:
            print('')
            clean_exit(client)
