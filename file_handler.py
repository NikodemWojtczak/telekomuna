def read_message(filename):
    with open(filename, 'r') as file:
        message = file.readline()
    return message


def read_binary_message(filename):
    with open(filename, 'r') as file:
        binary_message = file.readline()
    return binary_message


def write_message(filename, message):
    with open(filename, 'w') as file:
        file.write(message)


def write_binary_message(filename, binary_message):
    with open(filename, 'w') as file:
        file.write(binary_message)
