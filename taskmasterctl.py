from classes.Client import Client
from utils.command import parse_command

def clean_exit(client):
    client.close()
    print("Bye")
    exit(0)

def display_help():
    print('''commands:
=====================================
quit    exit    stop    start    status
=====================================''')
if __name__ == "__main__":
    client = Client()

    while True:
        try:
            cmd = input("taskmaster> ")

            # Parse help, exit and quit command
            if cmd == 'help':
                display_help()
                continue
            elif cmd == 'quit' or cmd == 'exit':
                clean_exit(client)

            # Parse commands
            (cmd_parsed, arguments) = parse_command(cmd)

            if cmd_parsed == 'kill':
                res = input("Are you sure you want to kill all processes and taskmaster? (Y/n)")
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
                print(f"*** Unknown syntax: {cmd}")
                continue
            elif not arguments:
                print("Missing arguments.")
                print("<command> <job_name or 'all'>")
                continue
            elif client.client_socket == None: # Try to connect to server if not connected
                client = Client()
            if client.client_socket != None: # If connected send command to server
                # todo: process arguments according to command and server
                client.send(f"{cmd_parsed} {arguments}")
                print(client.receive())
        except KeyboardInterrupt:
            print('')
            clean_exit(client)
        except EOFError:
            print('')
            clean_exit(client)
