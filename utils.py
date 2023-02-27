
def parse_command(input):
    '''
    Parse the command line input
    return False if the input is not valid
    return tuple of input (str) and arguments (array) otherwise
    '''
    input_split = input.split(' ')
    input = input_split[0]
    arguments = input_split[1:]

    if input not in ['status', 'restart', 'stop', 'start']:
        return False
    
    return (input, arguments)