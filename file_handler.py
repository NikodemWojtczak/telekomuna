def read_message(filename):
    """
    Odczytuje napis z wskazanego pliku.
    :param filename: nazwa pliku (string)
    :return: odczytany napis z pliku (string)
    """
    with open(filename, 'r') as file:
        message = file.readline()
    return message


def write_message(filename, message):
    """
    Zapisuje wiadomość do wskazanego pliku.
    :param filename: nazwa pliku (string)
    :param message: wiadomość, którą chcemy zapisać w pliku (string)
    """
    with open(filename, 'w') as file:
        file.write(message)
