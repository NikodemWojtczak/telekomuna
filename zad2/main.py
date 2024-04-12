import serial


print("")
print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 2. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
port_name = input("Wprowadź numer portu: ")

if "COM" not in port_name:
    port_name = "COM" + port_name

PORT = serial.Serial(
    port=port_name,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
)

SOH = bytearray.fromhex("01")
EOT = bytearray.fromhex("04")
ACK = bytearray.fromhex("06")
NAK = bytearray.fromhex("15")
CAN = bytearray.fromhex("18")
C = bytearray.fromhex("43")


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


def split_data(bytes_array):
    blocks = []
    num_blocks = len(bytes_array) // 128
    for block_nr in range(num_blocks):
        block = bytearray()
        for b in range(128):
            if 128*block_nr+b < len(bytes_array):
                block.append(bytes_array[128*block_nr+b])
            else:
                block.append(0)
        blocks.append(block)
    return blocks


def calculate_checksum(block):
    checksum = 0
    for byte in block:
        checksum ^= byte
    return checksum


def calculate_crc16(data):
    crc = 0
    msb = crc >> 8
    lsb = crc & 255
    for b in data:
        x = b ^ msb
        x ^= (x >> 4)
        msb = (lsb ^ (x >> 3) ^ (x << 4)) & 255
        lsb = (x ^ (x << 5)) & 255
    return (msb << 8) + lsb


def divide_crc16(crc):
    first_byte = (crc >> 8) & 0xFF
    second_byte = crc & 0xFF
    return [first_byte, second_byte]


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


def send_packet(data, packet_nr, mode):
    while True:
        packet = prepare_packet(data, packet_nr, mode)
        PORT.write(packet)
        PORT.flush()
        answer = PORT.read()
        if answer == ACK:
            break


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



