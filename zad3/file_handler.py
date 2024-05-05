def read_message(filename):
    with open(filename, 'r') as file:
        message = file.read()
    return message


def write_message(filename, message):
    with open(filename, 'w') as file:
        file.write(message)
