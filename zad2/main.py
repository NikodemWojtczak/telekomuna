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


def get_128_bit_block(binary_data, block_index):
    start = block_index * 16
    end = start + 16
    block = binary_data[start:end]
    return block


def calculate_checksum(block):
    checksum = 0
    for byte in block:
        checksum ^= byte
    return checksum


def calculate_crc16(block):
    polynomial = 0x1021
    # algorytm crc16 dla nadajnika do zaimplementowania











