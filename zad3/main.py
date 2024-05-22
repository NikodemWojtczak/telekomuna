import tcp

print("")
print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 3. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
print("Wybierz rolę w komunikacji")
print("1. Klient (wysłanie pliku)")
print("2. Serwer (odebranie pliku)")
print("Twój wybór")
choice = input(">> ")
if choice == '1':
    print("[1] Wprowadź ścieżkę do pliku z komunikatem tekstowym do przesłania")
    filename = input(">> ")
    print("[2] Wprowadź adres IP serwera, do którego chcesz wysłać plik")
    host_address = input(">> ")
    print("[3] Wprowadź numer portu")
    port = input(">> ")
    tcp_socket = tcp.TCP(host_address, int(port))
    try:
        dictionary, enc_bytes = tcp_socket.send(filename)
        print("[INFO] Plik został przesłany pomyślnie.")
        print("[4] Czy chcesz zapisać słownik z częstościami do pliku? [t/n]")
        choice = input(">> ")
        if choice == 't':
            print("   * Podaj ścieżkę zapisu")
            filename = input(">> ")
            with open(filename, 'wb') as file:
                file.write(dictionary)
            print("[INFO] Słownik zapisany.")
        print("[5] Czy chcesz zapisać zakodowaną wiadomość do pliku? [t/n]")
        choice = input(">> ")
        if choice == 't':
            print("   * Podaj ścieżkę zapisu")
            filename = input(">> ")
            with open(filename, 'wb') as file:
                file.write(enc_bytes)
            print("[INFO] Zakodowana wiadomość zapisana.")
    except Exception as e:
        print("[BŁĄD] Nie można wysłać pliku.", e)
elif choice == '2':
    print("[1] Wprowadź ścieżkę zapisu odebranego pliku")
    filename = input(">> ")
    print("[2] Wprowadź swój adres IP")
    host_address = input(">> ")
    print("[3] Wprowadź numer portu")
    port = input(">> ")
    tcp_socket = tcp.TCP(host_address, int(port))
    try:
        tcp_socket.receive(filename)
        print("[INFO] Plik został odebrany pomyślnie.")
    except Exception as e:
        print("[BŁĄD] Nie można odebrać pliku.", e)
