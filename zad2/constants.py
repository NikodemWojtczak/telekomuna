SOH = bytearray.fromhex("01")  # StartOfHeader - początek nagłówka
EOT = bytearray.fromhex("04")  # EndOfTransmission - koniec transmisji
ACK = bytearray.fromhex("06")  # Acknowledgement - potwierdzenie
NAK = bytearray.fromhex("15")  # NotAcknowledement - brak potwierdzenia (albo rozpocznij przesyłanie wykorzystując ASK)
CAN = bytearray.fromhex("18")  # Cancel - przerwij
C = bytearray.fromhex("43")  # C - rozpocznij przesyłanie wykorzystując CRC