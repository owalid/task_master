from client import Client
from utils import parse_command

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

            if cmd_parsed == False: # invalid command
                print(f"*** Unknown syntax: {cmd}")
                continue
            elif client.client_socket == None: # Try to connect to server if not connected
                client = Client()
            if client.client_socket != None: # If connected send command to server
                # todo: process arguments according to command and server
                client.send(cmd_parsed)
                print(client.receive())
        except KeyboardInterrupt:
            print('')
            clean_exit(client)
        except EOFError:
            print('')
            clean_exit(client)