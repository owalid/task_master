from classes.ParsingEnum import ALLOWED_COMMANDS
import socket

def parse_command(input):
    '''
    Parse the command line input
    return (False,False) if the input is not valid
    return (sts, array). input (str) and arguments (array) otherwise
    '''
    input_split = input.split(' ')
    input = input_split[0]
    arguments = None
    if len(input_split) > 1:
        arguments = input_split[1]

    if input not in ALLOWED_COMMANDS:
        return (False, False)
    
    return (input, arguments)


def send_result_command(connection, data):
    '''
    Send data to the socket.
    return: None
    '''
    if data and isinstance(data, str) and connection and isinstance(connection, socket.socket):
        connection.send(data.encode())
        