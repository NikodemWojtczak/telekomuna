import time

import serial


print("")
print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 2. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
port_name = input("Wprowadź numer portu: ")

if "COM" not in port_name:
    port_name = "COM" + port_name

# domyślne ustawienia portu szeregowego

PORT = serial.Serial(
    port=port_name,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
)

# znaki, które będą wysyłane i odbierane poprzez port szeregowy

SOH = bytearray.fromhex("01")  # StartOfHeader - początek nagłówka
EOT = bytearray.fromhex("04")  # EndOfTransmission - koniec transmisji
ACK = bytearray.fromhex("06")  # Acknowledgement - potwierdzenie
NAK = bytearray.fromhex("15")  # NotAcknowledement - brak potwierdzenia (albo rozpocznij przesyłanie wykorzystując ASK)
CAN = bytearray.fromhex("18")  # Cancel - przerwij
C = bytearray.fromhex("43")  # C - rozpocznij przesyłanie wykorzystując CRC


def read_file(filename):
    try:
        with open(filename, 'rb') as file:
            binary_data = file.read()
            return binary_data
    except FileNotFoundError:
        print("Plik nie został znaleziony.")
        return None
    except Exception as e:
        print("Wystąpił błąd podczas odczytu pliku:", e)
        return None


def write_file(filename, bytes_array):
    try:
        with open(filename, 'wb') as file:
            file.write(bytes_array)
    except FileNotFoundError:
        print("Plik nie został znaleziony.")
        return None
    except Exception as e:
        print("Wystąpił błąd podczas odczytu pliku:", e)
        return None


# podział bajtów na tablicę 128-bajtowych ciągów

def split_data(bytes_array):
    blocks = []
    num_blocks = len(bytes_array) // 128
    for block_nr in range(num_blocks):
        block = bytearray()
        for b in range(128):
            if 128*block_nr+b < len(bytes_array):
                block.append(bytes_array[128*block_nr+b])
            else:
                block.append(0x1A)  # jeżeli długość tablicy bajtów nie jest wielokrotnością 128
        blocks.append(block)        # dodajemy padding złożony ze znaków o kodzie 26 (0x1A)
    return blocks


def calculate_checksum(block):  # obliczenie algebraicznej sumy kontrolnej (1 bajt)
    checksum = 0
    for byte in block:
        checksum ^= byte
    return checksum


def calculate_crc16(data):  # obliczenie crc16 w standardzie XMODEM (2 bajty)
    crc = 0
    msb = crc >> 8
    lsb = crc & 255
    for b in data:
        x = b ^ msb
        x ^= (x >> 4)
        msb = (lsb ^ (x >> 3) ^ (x << 4)) & 255
        lsb = (x ^ (x << 5)) & 255
    return (msb << 8) + lsb


def divide_crc16(crc):  # podzielenie crc16 na dwa oddzielne bajty
    first_byte = (crc >> 8) & 0xFF
    second_byte = crc & 0xFF
    return [first_byte, second_byte]


# PRZYGOTOWANIE PAKIETU DO WYSŁANIA:
# 1. bajt stanowi znak SOH,
# 2. bajt stanowi numer pakietu,
# 3. bajt stanowi dopełnienie numeru pakietu do 255,
# bajty od 4. do 131. stanowią 128-bajtowy blok przesyłanych danych,
# jeżeli mode == NAK, to 132. bajt to algebraiczna suma kontrolna,
# jeżeli mode == C, to bajty 132. i 133. stanowią sumę kontrolną crc16,
# zwracamy zatem 132 (NAK) lub 133 (C) bajtowy pakiet.

def prepare_packet(data, packet_nr, mode):
    header = bytearray()
    header.append(int.from_bytes(SOH, byteorder='big'))
    header.append(packet_nr)
    header.append(255 - packet_nr)
    full = header + data
    if mode == C:
        crc = calculate_crc16(data)
        crc = divide_crc16(crc)
        full.append(crc[0])
        full.append(crc[1])
    elif mode == NAK:
        full.apend(calculate_checksum(data))
    return full


# WYSŁANIE POJEDYNCZEGO PAKIETU:
# opakowanie bloku danych w nagłówek i sumę kontrolną,
# przesłanie pakietu poprzez port (PORT.write()),
# oczyszczenie bufora portu (PORT.flush()),
# odczytanie zawartości portu szeregowego jako odpowiedź od odbiornika,
# jeżeli odpowiedź to ACK, kończymy przesyłanie pakietu, w przeciwnym razie ponawiamy transmisję.

def send_packet(data, packet_nr, mode):
    while True:
        packet = prepare_packet(data, packet_nr, mode)
        PORT.write(packet)
        PORT.flush()
        answer = PORT.read()
        if answer == ACK:
            break


# PRZESŁANIE PLIKU:
# odczytanie bajtów z pliku,
# rozdzielenie bajtów na 128-bajtowe bloki,
# oczyszczenie bufora,
# odczytanie komunikatu inicjalnego od odbiornika, który będzie wskazanym trybem wyliczania sumy kontrolnej
# dla każdego bloku w otrzymanych blokach danych:
#   1. wysyłamy pakiet,
# po wysłaniu wszystkich pakietów nadajnik przesyła znak EOT,
# jeżeli nadajnik odbierze od odbiornika znak ACK, to znaczy, że transmisja danych przebiegła pomyślnie.

def send_file(filename):
    file_bytes = read_file(filename)
    file_blocks = split_data(file_bytes)
    packet_nr = 1
    PORT.flush()
    initial_answer = PORT.read()
    while initial_answer != C and initial_answer != NAK:
        PORT.flush()
        initial_answer = PORT.read()
    mode = initial_answer
    for block in file_blocks:
        PORT.flush()
        send_packet(block, packet_nr, mode)
        print("Wysłano pakiet nr", packet_nr)
        packet_nr += 1
        if packet_nr > 255:
            packet_nr = 0
    PORT.write(EOT)
    if PORT.read() == ACK:
        print("Odebrano potwierdzenie od odbiorcy, dane zostały przesłane poprawnie.")


# ROZPOCZĘCIE TRANSMISJI PRZEZ ODBIORNIK:
# przez 1 minutę co 10 sekund:
#   1. przesyłamy do portu szeregowego odpowiedni znak (NAK lub C)
#   2. odczytujemy odpowiedź
#   3. jeżeli odpowiedzią jest znak SOH, to znaczy, że nadajnik zaczął wysyłać pierwszy pakiet

def start_receiving(mode):
    for _ in range(1, 7):
        time.sleep(10)
        PORT.reset_input_buffer()
        PORT.write(mode)
        initial_receive = PORT.read()
        if initial_receive == SOH:
            return initial_receive
        else:
            return None


# metoda odczytująca 128 bajtów (czyli blok danych) z portu szeregowego

def receive_data_block():
    data_block = bytearray()
    for b in range(128):
        data_block += PORT.read()
    return data_block


# SPRAWDZANIE POPRAWNOŚCI PAKIETU:
# opiera się wyłącznie na wyliczeniu odpowiedniej sumy kontrolnej przez odbiornik i porównaniu jej
# z sumą kontrolną z odebranego pakietu,
# jeżeli pakiet jest poprawny, odbiornik wysyła ACK, jeżeli nie, to wysyła NAK, a nadajnik będzie musiał ponownie
# przesłać pakiet.

def check_packet(packet, mode):
    check = bytearray()
    self_check = bytearray()
    if mode == NAK:
        check += PORT.read()
        self_check += calculate_checksum(packet)
        if check[0] == self_check[1]:
            PORT.write(ACK)
            return True
        else:
            PORT.write(NAK)
            return False
    elif mode == C:
        check += PORT.read()
        check += PORT.read()
        crc = calculate_crc16(packet)
        crc = divide_crc16(crc)
        self_check.append(crc[0])
        self_check.append(crc[1])
        for b in range(2):
            if check[b] != self_check[b]:
                PORT.write(NAK)
                return False
        PORT.write(ACK)
        return True


# ODEBRANIE PAKIETU:
# dodanie do nagłówka znaku SOH,
# odczytanie z portu szeregowego i dodanie do nagłówka kolejno:
#    numeru pakietu,
#    dopełnienia pakietu do 255,
# odczytanie 128-bajtowego bloku danych,
# sprawdzenie bloku danych, usunięcie paddingu, zwrócenie tego bloku


def receive_packet(initial_receive, mode):
    header = bytearray()
    header += initial_receive
    header += PORT.read()
    header += PORT.read()
    packet = receive_data_block()
    if check_packet(packet, mode):
        print("Otrzymano pakiet nr", header[1])
        while packet[-1] == 0x1A:
            packet = packet[:-1]
        return packet


# ODEBRANIE DANYCH:
# rozpoczęcie odbierania,
# jeżeli pierwszym odebranym znakiem jest SOH, to nadajnik zainicjował transmisję:
#   1. odczytujemy z portu 128-bajtowy blok danych i dodajemy go do tablicy,
#   2. aktualizujemy odpowiedź od odbiornika,
#   3. jeżeli odpowiedzią było EOT, to znaczy, że nadajnik zakończył przesyłanie danych,
# odbiornik przesyła znak ACK, informując nadajnik, że odebrał dane,
# odebrane dane zapisywane są w pliku.

def receive_data(mode, filename):
    initial_receive = start_receiving(mode)
    file_bytes = bytearray()
    if initial_receive == SOH:
        while True:
            packet = receive_packet(initial_receive, mode)
            file_bytes += packet
            initial_receive = PORT.read()
            if initial_receive == EOT:
                break
    PORT.write(ACK)
    print("Wszystkie dane zostały odebrane.")
    write_file(filename, file_bytes)
