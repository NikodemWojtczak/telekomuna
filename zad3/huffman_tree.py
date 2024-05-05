import heapq
import frequency_dictionary as fd


class Node:
    def __init__(self, frequency, symbol, left_node=None, right_node=None):
        self.frequency = frequency  # częstość znaku
        self.symbol = symbol  # znak
        self.left_node = left_node  # wskaźnik do węzła po lewej stronie
        self.right_node = right_node  # wskaźnik do węzła po prawej stronie
        self.huff = ''  # kod znaku w drzewie Huffmana

    def __lt__(self, next_node):
        return self.frequency < next_node.frequency


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
    def __init__(self, dictionary):
        self.nodes = create_tree(dictionary)


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


def encode(node, message):  # kodowanie wiadomości
    encoded_message = ''
    for char in message:
        encoded_message += find_huff(node, char)
    return encoded_message


def decode(node, message):  # dekodowanie wiadomości
    decoded_message = ''
    while len(message) > 0:
        message, symbol = find_symbol(node, message)
        decoded_message += symbol
    return decoded_message
