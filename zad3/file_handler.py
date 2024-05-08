def read_message(filename):  # odczytaj wiadomość z pliku
    with open(filename, 'r') as file:
        message = file.read()
    return message


def write_message(filename, message):  # zapisz wiadomość do pliku
    with open(filename, 'w') as file:
        file.write(message)
