import numpy as np


H = np.array([[1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
              [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
              [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
              [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
"""
Macierz służąca do korygowania błędów.
Aby była ona zdolna do wykrywania błędów pojedynczych, musi:\n
* nie posiadać kolumn zerowych\n
* nie posiadać kolumn identycznych\n
Aby była ona zdolna do wykrywania błędów podwójnych, musi dodatkowo:\n
* nie posiadać kolumny, która jest sumą dwóch pozostałych kolumn\n
Macierz ta spełnia wszystkie wymienione warunki, przez co może korygować zarówno błędy pojedyncze jak i podwójne.
"""


def is_binary_valid(binary_string):
    """
    Sprawdza, czy zakodowana wiadomość przedstawiona za pomocą ciągu bitów jest sformatowana poprawnie, tj.
    czy długość wiadomości jest większa od 0, czy długość wiadomości jest wielokrotnością 16, czy w wiadomości
    nie znajdują się znaki niedozwolone (inne niż 0 i 1).
    :param binary_string: napis będący zakodowaną wiadomością w postaci binarnej (string)
    :return: True gdy w wiadomości nie ma błędów, False gdy w wiadomości są błędy (boolean)
    """
    if not all(char in '01' for char in binary_string):
        return False
    if len(binary_string) % 16 != 0:
        return False
    if len(binary_string) == 0:
        return False
    return True


def char_to_binary(char):
    """
    Konwertuje znak do postaci bitowej z uzupełnieniem do 8 bitów.
    :param char: pojedynczy znak do zakodowania (char)
    :return: Napis będący binarną, 8-bitową reprezentacją znaku (string)
    """
    return bin(ord(char))[2:].zfill(8)


def binary_to_char(binary):
    """
    Konwertuje 8-bitowy ciąg do pojedynczego znaku.
    :param binary: napis będący 8-bitowym ciągiem (string)
    :return: Znak, którego binarną reprezentacją jest wskazany ciąg bitów (char)
    """
    ascii_code = int(binary, 2)
    return chr(ascii_code)


def string_to_binary(string):
    """
    Konwertuje napis do postaci binarnej.
    :param string: napis do zakodowania (string)
    :return: Napis będący ciągiem bitów reprezentującym wskazany napis w postaci binarnej (string)
    """
    result = ""
    for char in string:
        result += char_to_binary(char)
    return result


def binary_to_string(binary):
    """
    Konwertuje ciąg bitów do napisu.
    :param binary: napis będący ciągiem bitów do przekonwertowania (string)
    :return: Napis, którego binarną reprezentacją jest wskazany ciąg bitów (string)
    """
    result = ""
    while binary:
        result += binary_to_char(binary[:8])
        binary = binary[8:]
    return result


def get_parity_bits(char):
    """
    Zwraca dla podanego znaku napis będący ciągiem 8 bitów parzystości. Aby uzyskać bit parzystości liczona jest 
    suma modulo 2 iloczynów bitów wiadomości z jednego wiersza macierzy H przez bity reprezentacji binarnej znaku na 
    odpowiadających sobie pozycjach. Czynność tą powtarza się dla każdego wiersza macierzy H.
    :param char: znak, dla którego mają zostać obliczone bity parzystości (char)
    :return: Napis będący ciągiem 8-bitów parzystości dla wskazanego znaku (string)
    """
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
    """
    Koduje znak, czyli zamienia go na reprezentację binarną i dołącza do niego bity parzystości.
    :param char: znak do zakodowania (char)
    :return: Napis będący 16-bitowym ciągiem reprezentującym zakodowany znak (string)
    """
    return char_to_binary(char) + get_parity_bits(char)


def decode_char(binary):
    """
    Dekoduje znak, czyli pozbywa się bitów parzystości z podanego ciągu bitów.
    :param binary: napis będący 16-bitowym ciągiem reprezentującym zakodowany znak
    :return: Zdekodowany znak (char)
    """
    return chr(int(binary[:8], 2))


def encode_string(string):
    """
    Koduje napis, czyli dopisuje bity parzystości do wszystkich znaków napisu.
    :param string: napis do zakodowania (string)
    :return: Ciąg bitów reprezentujących zakodowane znaki napisu (string)
    """
    result = ""
    for char in string:
        result += encode_char(char)
    return result


def decode_string(binary):
    """
    Dekoduje napis, czyli z każdego znaku napisu w reprezentacji binarnej usuwa bity parzystości.
    :param binary: napis będący ciągiem bitów reprezentującym zakodowaną wiadomość (string)
    :return: Zdekodowany napis
    """
    result = ""
    while binary:
        result += decode_char(binary[:16])
        binary = binary[16:]
    return result


def verify_char(binary_char):
    """
    Weryfikuje poprawność zakodowanego znaku, mnożąc go przez macierz H. Jeżeli błąd nie wystąpił, iloczyn będzie
    wektorem składającym się z samych zer. Jeżeli wystąpił jeden błąd, iloczyn przyjmie postać kolumny, której pozycja
    w macierzy H oznacza pozycję błędu. Natomiast jeżeli wystąpiły dwa błędy, iloczyn przyjmie postać sumy dwóch kolumn,
    których pozycje w macierzy H oznaczają pozycje błędów.
    :param binary_char: napis będący 16-bitowym ciągiem reprezentującym zakodowany znak
    :return: Tablica z pozycjami, na których wystąpił błąd (numerowanie od 0), tablica będzie zawierać w sobie
     wyłącznie -1, gdy nie znaleziono błędów (list)
    """
    R = np.array(list(binary_char)).astype(int)
    HR = np.dot(H, R)
    HR %= 2
    position = [-1]
    match = False
    for j in range(16):
        match = True
        for i in range(8):
            if H[i][j] != HR[i]:
                match = False
                break
        if match:
            position.pop()
            position.append(j)
            break
    if not match:
        for i in range(16):
            for j in range(i + 1, 16):
                sum_of_columns = np.array([(H[k][i] + H[k][j]) % 2 for k in range(8)])
                if np.array_equal(sum_of_columns, HR):
                    position.pop()
                    position.append(i)
                    position.append(j)
    return position


def correct_char(binary_char, position):
    """
    Poprawia bity w zakodowanym znaku dla wskazanych pozycji błędów, negując je.
    :param binary_char: napis będący 16-bitowym ciągiem reprezentującym zakodowany znak (string)
    :param position: tablica zawierająca pozycje, na których wystąpił błąd (list)
    :return: Napis będący zakodowanym znakiem w postaci binarnej z poprawionymi bitami (string)
    """
    binary_char = list(binary_char)
    for i in position:
        if binary_char[i] == '0':
            binary_char[i] = '1'
        else:
            binary_char[i] = '0'
    binary_char = ''.join(binary_char)
    return binary_char


def verify_string(binary_string):
    """
    Weryfikuje poprawność zakodowanej wiadomości, weryfikując poszczególne znaki w napisie.
    :param binary_string: napis będący ciągiem bitów reprezentujących zakodowaną wiadomość (string)
    :return: Pozycje w wiadomości, na których wystąpił błąd (numerowanie od 0)
    """
    positions = []
    iteration = 0
    while binary_string:
        binary_char = binary_string[:16]
        verification = verify_char(binary_char)
        position = []
        for i in verification:
            position.append((iteration * 16) + i)
        if verification[0] != -1:
            for p in position:
                positions.append(p)
        binary_string = binary_string[16:]
        iteration += 1
    return positions


def correct_string(binary_string, positions):
    """
    Poprawia bity w wiadomości dla wskazanych pozycji, negując je.
    :param binary_string: napis będący ciągiem bitów reprezentujących zakodowaną wiadomość (string)
    :param positions: tablica zawierająca pozycje, na których wystąpił (list)
    :return: Nais będący zakodowaną wiadomością w postaci binarnej z poprawionymi bitami (string)
    """
    while len(positions) > 0:
        index = len(positions) - 1
        word_position = int(positions[index] / 16)
        start_index = word_position * 16
        end_index = start_index + 16
        corrected_char = correct_char(binary_string[start_index:end_index], [positions[index] % 16])
        binary_string = binary_string[:start_index] + corrected_char + binary_string[end_index:]
        positions.pop()
    return binary_string
