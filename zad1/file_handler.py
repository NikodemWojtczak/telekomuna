def read_message(filename):
    """
    Odczytuje napis z wskazanego pliku.
    :param filename: nazwa pliku (string)
    :return: odczytany napis z pliku (string)
    """
    with open(filename, 'r', encoding="iso-8859-1") as file:
        message = file.read()
    return message


def write_message(filename, message):
    """
    Zapisuje wiadomość do wskazanego pliku.
    :param filename: nazwa pliku (string)
    :param message: wiadomość, którą chcemy zapisać w pliku (string)
    """
    with open(filename, 'w', encoding="iso-8859-1") as file:
        file.write(message)
