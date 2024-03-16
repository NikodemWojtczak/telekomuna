import numpy as np


def get_h_matrix():
    matrix = np.ones((8, 8))
    np.fill_diagonal(matrix, 0)
    matrix = np.fliplr(matrix)
    unit_matrix = np.eye(8)
    return np.hstack((matrix, unit_matrix))


H = get_h_matrix()


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


def char_to_binary(char):
    return bin(ord(char))[2:].zfill(8)


def binary_to_char(binary):
    ascii_code = int(binary, 2)
    return chr(ascii_code)


def string_to_binary(string):
    result = ""
    for char in string:
        result += char_to_binary(char)
    return result


def binary_to_string(binary):
    result = ""
    while binary:
        result += binary_to_char(binary[:8])
        binary = binary[8:]
    return result


def get_parity_bits(char):
    char_bits_array = list(char_to_binary(char))
    parity_bits = ""
    for i in range(8):
        parity_bit = 0
        for j in range(8):
            parity_bit += H[i][j] * int(char_bits_array[j])
        parity_bit %= 2
        parity_bits += str(int(parity_bit))
    return parity_bits


def encode_char(char):
    return char_to_binary(char) + get_parity_bits(char)


def decode_char(binary):
    return chr(int(binary[:8], 2))


def encode_string(string):
    result = ""
    for char in string:
        result += encode_char(char)
    return result


def decode_string(binary):
    result = ""
    while binary:
        result += decode_char(binary[:16])
        binary = binary[16:]
    return result
