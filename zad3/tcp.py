import socket
import pickle
import huffman_tree as ht


class TCP:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, file_path):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))  # tworzymy połączenie z gniazdem sieciowym komputera docelowego
            with open(file_path, 'r') as file:
                message = file.read()  # odczytujemy wiadomość
                dictionary, encoded_bytes = ht.encode(message)  # kodujemy ją
                print("[INFO] Wiadomość zakodowana ma długość", len(encoded_bytes), "B")
                serialized_data = pickle.dumps((dictionary, encoded_bytes))  # serializujemy wiadomość i słownik
                print("[INFO] Po serializacji wiadomości i tablicy częstości przesyłam", len(serialized_data), "B")
                s.sendall(serialized_data)  # przesyłamy zserializowane dane

    def receive(self, file_path):
        serialized_data = b""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))  # powiązujemy gniazdo z własnym adresem IPv4 i numerem portu
            s.listen()  # nasłuchujemy na gnieździe
            conn, addr = s.accept()  # akceptujemy połączenie, pobieramy to połączenie i adres
            with open(file_path, 'w') as file:
                while True:  # pobieramy dane poprzez bufor 1024-bajtowy
                    data = conn.recv(1024)
                    if not data:
                        break
                    serialized_data += data
                dictionary, encoded_bytes = pickle.loads(serialized_data)  # deserializacja
                decoded_message = ht.decode(dictionary, encoded_bytes)  # dekodowanie
                file.write(decoded_message)
