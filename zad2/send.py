import serial
import constants
import xmodem

is_port_open = True

print("")
print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 2. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
print("ROLA W TRANSMISJI: Nadajnik")
port_name = input(">>> Wprowadź numer portu: ")

if "COM" not in port_name:
    port_name = "COM" + port_name

try:
    PORT = serial.Serial(
        port=port_name,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=10
    )
except Exception as e:
    print("[BŁĄD] Port nie mógł zostać otwarty.")
    is_port_open = False

if is_port_open:
    file_name = input(">>> Wprowadź nazwę pliku do transmisji: ")
    xmodem.send_file(PORT, file_name)
    PORT.close()
