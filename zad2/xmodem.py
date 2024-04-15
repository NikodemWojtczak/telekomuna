import math
import constants


def read_file(filename):
    try:
        with open(filename, 'rb') as file:
            binary_data = file.read()
            return binary_data
    except FileNotFoundError:
        print("[BŁĄD] Plik nie został znaleziony.")
        return None
    except Exception as e:
        print("[BŁĄD] Wystąpił błąd podczas odczytu pliku:", e)
        return None


def write_file(filename, bytes_array):
    try:
        with open(filename, 'wb') as file:
            file.write(bytes_array)
    except FileNotFoundError:
        print("[BŁĄD] Plik nie został znaleziony.")
        return None
    except Exception as e:
        print("[BŁĄD] Wystąpił błąd podczas odczytu pliku:", e)
        return None


# podział bajtów na tablicę 128-bajtowych ciągów

def split_data(bytes_array):
    blocks = []
    num_blocks = math.ceil(len(bytes_array) / 128)
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
    header.append(int.from_bytes(constants.SOH, byteorder='big'))
    header.append(packet_nr)
    header.append(255 - packet_nr)
    full = header + data
    if mode == constants.C:
        crc = calculate_crc16(data)
        crc = divide_crc16(crc)
        full.append(crc[0])
        full.append(crc[1])
    elif mode == constants.NAK:
        full.append(calculate_checksum(data))
    return full


# WYSŁANIE POJEDYNCZEGO PAKIETU:
# opakowanie bloku danych w nagłówek i sumę kontrolną,
# przesłanie pakietu poprzez port (PORT.write()),
# oczyszczenie bufora portu (PORT.flush()),
# odczytanie zawartości portu szeregowego jako odpowiedź od odbiornika,
# jeżeli odpowiedź to ACK, kończymy przesyłanie pakietu, w przeciwnym razie ponawiamy transmisję.

def send_packet(port, data, packet_nr, mode):
    while True:
        packet = prepare_packet(data, packet_nr, mode)
        port.write(packet)
        port.flush()
        answer = port.read()
        if answer == constants.ACK:
            print("[ODB][ACK] Pakiet", packet_nr, "przesłany poprawnie.")
            break
        else:
            print("[ODB][NAK] Pakiet", packet_nr, "nie został przesłany poprawnie. Przechodzę do retransmisji.")


# PRZESŁANIE PLIKU:
# odczytanie bajtów z pliku,
# rozdzielenie bajtów na 128-bajtowe bloki,
# oczyszczenie bufora,
# odczytanie komunikatu inicjalnego od odbiornika, który będzie wskazanym trybem wyliczania sumy kontrolnej
# dla każdego bloku w otrzymanych blokach danych:
#   1. wysyłamy pakiet,
# po wysłaniu wszystkich pakietów nadajnik przesyła znak EOT,
# jeżeli nadajnik odbierze od odbiornika znak ACK, to znaczy, że transmisja danych przebiegła pomyślnie.

def send_file(port, filename):
    file_bytes = read_file(filename)
    file_blocks = split_data(file_bytes)
    print("[INFO] Odczytano zawartość pliku do wysłania.")
    packet_nr = 1
    port.flush()
    initial_answer = port.read()
    while initial_answer != constants.C and initial_answer != constants.NAK:
        port.flush()
        initial_answer = port.read()
    mode = initial_answer
    if mode == constants.NAK:
        print("[ODB][NAK] Odbiorca wybrał następujący sposób liczenia sumy kontrolnej: Algebraiczna Suma Kontrolna.")
    elif mode == constants.C:
        print("[ODB][ C ] Odbiorca wybrał następujący sposób liczenia sumy kontrolnej: Cykliczny Kod Nadmiarowy.")
    for block in file_blocks:
        port.flush()
        send_packet(port, block, packet_nr, mode)
        packet_nr += 1
        if packet_nr > 255:
            packet_nr = 0
    port.write(constants.EOT)
    print("[NAD][EOT] Zakończono transmisję danych.")
    if port.read() == constants.ACK:
        print("[ODB][ACK] Odebrano potwierdzenie od odbiorcy. Transmisja danych przebiegła pomyślnie.")


# ROZPOCZĘCIE TRANSMISJI PRZEZ ODBIORNIK:
# przez 1 minutę co 10 sekund:
#   1. przesyłamy do portu szeregowego odpowiedni znak (NAK lub C)
#   2. odczytujemy odpowiedź
#   3. jeżeli odpowiedzią jest znak SOH, to znaczy, że nadajnik zaczął wysyłać pierwszy pakiet

def start_receiving(port, mode):
    for _ in range(6):
        port.reset_input_buffer()
        port.write(mode)
        if mode == constants.NAK:
            print("[ODB][NAK] Wysłano znak NAK.")
        elif mode == constants.C:
            print("[ODB][ C ] Wysłano znak C.")
        initial_receive = port.read()
        if initial_receive == constants.SOH:
            print("[NAD][SOH] Nadawca zaczął przesyłać.")
            return initial_receive
        else:
            continue
    return None


# metoda odczytująca 128 bajtów (czyli blok danych) z portu szeregowego

def receive_data_block(port):
    data_block = bytearray()
    for b in range(128):
        data_block += port.read()
    return data_block


# SPRAWDZANIE POPRAWNOŚCI PAKIETU:
# opiera się wyłącznie na wyliczeniu odpowiedniej sumy kontrolnej przez odbiornik i porównaniu jej
# z sumą kontrolną z odebranego pakietu,
# jeżeli pakiet jest poprawny, odbiornik wysyła ACK, jeżeli nie, to wysyła NAK, a nadajnik będzie musiał ponownie
# przesłać pakiet.

def check_packet(port, packet, mode):
    check = bytearray()
    self_check = bytearray()
    if mode == constants.NAK:
        check += port.read()
        self_check.append(calculate_checksum(packet))
        if check[0] == self_check[0]:
            port.write(constants.ACK)
            return True
        else:
            port.write(constants.NAK)
            return False
    elif mode == constants.C:
        check += port.read()
        check += port.read()
        crc = calculate_crc16(packet)
        crc = divide_crc16(crc)
        self_check.append(crc[0])
        self_check.append(crc[1])
        for b in range(2):
            if check[b] != self_check[b]:
                port.write(constants.NAK)
                return False
        port.write(constants.ACK)
        return True


# ODEBRANIE PAKIETU:
# dodanie do nagłówka znaku SOH,
# odczytanie z portu szeregowego i dodanie do nagłówka kolejno:
#    numeru pakietu,
#    dopełnienia pakietu do 255,
# odczytanie 128-bajtowego bloku danych,
# sprawdzenie bloku danych, usunięcie paddingu, zwrócenie tego bloku


def receive_packet(port, initial_receive, mode):
    header = bytearray()
    header += initial_receive
    header += port.read()
    header += port.read()
    packet = receive_data_block(port)
    if check_packet(port, packet, mode):
        print("[INFO] Otrzymano pakiet nr", header[1])
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

def receive_file(port, mode, filename):
    initial_receive = start_receiving(port, mode)
    file_bytes = bytearray()
    if initial_receive == constants.SOH:
        while True:
            packet = receive_packet(port, initial_receive, mode)
            file_bytes += packet
            initial_receive = port.read()
            if initial_receive == constants.EOT:
                print("[NAD][EOT] Nadawca zakończył przesyłanie danych.")
                break
        port.write(constants.ACK)
        print("[ODB][ACK] Informuję nadajnik o poprawności przesłania wszystkich danych.")
        write_file(filename, file_bytes)
        print("[INFO] Zapisano dane do wskazanego pliku.")
    else:
        print("[BŁĄD] Minęła minuta, nadajnik nie zaczął przesyłać. Kończę transmisję.")
