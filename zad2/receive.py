import serial
import constants
import xmodem

is_port_open = True

print("")
print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 2. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
print("ROLA W TRANSMISJI: Odbiornik")
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
    file_name = input(">>> Wprowadź nazwę pliku, do którego zostaną zapisane odebrane dane: ")
    print("Wybierz sposób obliczania sumy kontrolnej")
    print("1. Algebraiczna Suma Kontrolna")
    print("2. Cykliczny Kod Nadmiarowy")
    mode = input(">>> Twój wybór: ")
    if mode == '1':
        xmodem.receive_file(PORT, constants.NAK, file_name)
    elif mode == '2':
        xmodem.receive_file(PORT, constants.C, file_name)
    else:
        print("[BŁĄD] Brak takiej opcji w menu.")
    PORT.close()