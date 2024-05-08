import heapq

class Node:
    def __init__(self, frequency, symbol, left_node=None, right_node=None):
        self.frequency = frequency  # częstość znaku
        self.symbol = symbol  # znak
        self.left_node = left_node  # wskaźnik do węzła po lewej stronie
        self.right_node = right_node  # wskaźnik do węzła po prawej stronie
        self.huff = ''  # kod znaku w drzewie Huffmana

    def __lt__(self, next_node):  # potrzebne do tego, żeby węzły umieścić na stosie wg priorytetu (częstości)
        return self.frequency < next_node.frequency  # w kolejności rosnącej


def create_tree(dictionary):
    nodes = []  # lista zawierająca węzły drzewa
    for key, value in dictionary.items():
        heapq.heappush(nodes, Node(value, key))
    while len(nodes) > 1:
        # pobranie dwóch węzłów z najmniejszą częstością
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        # przyporządkowanie wartości kierunkowych tym węzłom (0 - lewy, 1 - prawy)
        left.huff = '0'
        right.huff = '1'
        # połączenie tych dwóch węzłów, aby stworzyć węzeł będący dla tych węzłów rodzicem
        newNode = Node(left.frequency + right.frequency, left.symbol + right.symbol, left, right)
        # dodanie nowego węzła do stosu
        heapq.heappush(nodes, newNode)
    return nodes


class Huffman:
    def __init__(self, dictionary):  # inicjalizujemy drzewo słownikiem zawierającym częstości
        self.nodes = create_tree(dictionary)  # poszczególnych symboli w kodowanym tekście


def find_huff(node, symbol, current_code=''):  # szuka w drzewie kodu Huffmana podanego symbolu
    if node.symbol == symbol:
        return current_code
    if node.left_node:
        left_code = find_huff(node.left_node, symbol, current_code + '0')
        if left_code:
            return left_code
    if node.right_node:
        right_code = find_huff(node.right_node, symbol, current_code + '1')
        if right_code:
            return right_code


def find_symbol(node, decoded_mess):  # szuka w drzewie symbolu, jeżeli trafi na krawędź drzewa
    next_node = node                  # to kończy szukanie i usuwa z zakodowanej wiadomości odczytane bity
    while len(decoded_mess) > 0:
        if decoded_mess[0] == '0' and next_node.left_node:
            next_node = next_node.left_node
            decoded_mess = decoded_mess[1:]
        elif decoded_mess[0] == '1' and next_node.right_node:
            next_node = next_node.right_node
            decoded_mess = decoded_mess[1:]
        if not next_node.right_node and not next_node.left_node:
            break
    return [decoded_mess, next_node.symbol]


def create_dictionary(string):  # tworzy słownik z częstością symboli występujących w tekście
    dictionary = {}  # każda para w słowniku to klucz: wartość, u nas symbol: częstość
    for char in string:
        if char in dictionary:
            dictionary[char] += 1
        else:
            dictionary[char] = 1
    return dictionary


def encode(message):  # kodowanie wiadomości
    encoded_message = ''
    zeros_added = 0
    dictionary = create_dictionary(message)
    tree = Huffman(dictionary)
    for char in message:  # tworzymy napis z kodów z drzewa Huffmana dla symboli w tekście
        encoded_message += find_huff(tree.nodes[0], char)
    while len(encoded_message) % 8 != 0:  # uzupełniamy napis zerami, aby jego długość była wielokrotnością 8 bitów
        encoded_message += '0'
        zeros_added += 1
    encoded_bytes = bytearray()
    for i in range(0, len(encoded_message), 8):  # wyciągamy z tego napisu bajty
        subarray = encoded_message[i:i+8]
        byte = int(subarray, 2)
        encoded_bytes.append(byte)
    encoded_bytes.append(zeros_added)  # dodajemy na koniec jeden bajt informujący o ilości zer dodanych jako padding
    return [dictionary, encoded_bytes]


def decode(dictionary, message_bytes):  # dekodowanie wiadomości
    message = ''
    decoded_message = ''
    tree = Huffman(dictionary)
    for i in range(len(message_bytes)-1):  # przekształcamy tablicę bajtów na ciąg bitów do napisu
        bin_array = bin(message_bytes[i])[2:].zfill(8)
        message += bin_array
    zeros_added = message_bytes[-1]
    for i in range(zeros_added):  # usuwamy padding
        message = message[:-1]
    print("[INFO] Dekodowanie odbędzie się dla następującego ciągu bitów"
          " (bez paddingu):", message, ", łącznie", len(message), "b.")
    while len(message) > 0:  # właściwe dekodowanie
        message, symbol = find_symbol(tree.nodes[0], message)
        decoded_message += symbol
    return decoded_message
