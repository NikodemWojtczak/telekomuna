import numpy as np


def get_h_matrix():
    matrix = np.ones((8, 8))
    np.fill_diagonal(matrix, 0)
    matrix = np.fliplr(matrix)
    unit_matrix = np.eye(8)
    return np.hstack((matrix, unit_matrix))


H = get_h_matrix()


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
    char_bits = char_to_binary(char)
    parity_bits = ""
    for i in range(8):
        parity_bit = 0
        for j in range(8):
            parity_bit += H[i][j] * int(char_bits[j])
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


def verify_char(binary_char):
    R = np.array(list(binary_char)).astype(int)
    HR = np.dot(H, R)
    HR %= 2
    position = -1
    for j in range(16):
        match = True
        for i in range(8):
            if H[i][j] != HR[i]:
                match = False
                break
        if match:
            position = j
            break
    return position


def correct_char(binary_char, position):
    binary_char = list(binary_char)
    if binary_char[position] == '0':
        binary_char[position] = '1'
    else:
        binary_char[position] = '0'
    binary_char = ''.join(binary_char)
    return binary_char


def verify_string(binary_string):
    positions = []
    iteration = 0
    while binary_string:
        binary_char = binary_string[:16]
        verification = verify_char(binary_char)
        position = (iteration * 16) + verification
        if verification != -1:
            positions.append(position)
        binary_string = binary_string[16:]
        iteration += 1
    return positions


def correct_string(binary_string, positions):
    while len(positions) > 0:
        index = len(positions) - 1
        word_position = int(positions[index] / 16)
        start_index = word_position * 16
        end_index = start_index + 16
        corrected_char = correct_char(binary_string[start_index:end_index], positions[index] % 16)
        binary_string = binary_string[:start_index] + corrected_char + binary_string[end_index:]
        positions.pop()
    return binary_string

