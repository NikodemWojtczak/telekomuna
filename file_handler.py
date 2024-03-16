def print_binary_string(binary_string):  # do czytelnego zapisu w pliku
    result = ""
    while binary_string:
        result += binary_string[:8]
        binary_string = binary_string[8:]
        if len(binary_string) >= 8:
            result += " "
    return result


def get_binary_from_string(string):  # odczytanie ciagu bitow z pliku (bedzie ze spacjami - trzeba je usunac)
    return string.replace(" ", "")


def read_message(filename):
    with open(filename, 'r') as file:
        message = file.readline()
    return message


def read_binary_message(filename):
    with open(filename, 'r') as file:
        binary_message = get_binary_from_string(file.readline())
    return binary_message


def write_message(filename, message):
    with open(filename, 'w') as file:
        file.write(message)


def write_binary_message(filename, binary_message):
    with open(filename, 'w') as file:
        file.write(print_binary_string(binary_message))


