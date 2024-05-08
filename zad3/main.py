import tcp

print("")
print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 3. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
print("Chcesz wysłać plik czy go odebrać?")
print("1. Wyślij plik")
print("2. Odbierz plik")
choice = input("Twój wybór: ")
if choice == '1':
    filename = input("Wprowadź ścieżkę do pliku z komunikatem tekstowym do przesłania: ")
    print("--- USTAWIANIE POŁĄCZENIA - TWORZENIE GNIAZDA SIECIOWEGO ---")
    host_address = input("Podaj adres hosta: ")
    port = input("Podaj port: ")
    tcp_socket = tcp.TCP(host_address, int(port))
    try:
        tcp_socket.send(filename)
        print("[INFO] Plik został przesłany pomyślnie.")
    except Exception as e:
        print("[BŁĄD] Nie można wysłać pliku.", e)
elif choice == '2':
    filename = input("Wprowadź ścieżkę zapisu odebranego pliku: ")
    print("--- USTAWIANIE POŁĄCZENIA - TWORZENIE GNIAZDA SIECIOWEGO ---")
    host_address = input("Podaj adres hosta: ")
    port = input("Podaj port: ")
    tcp_socket = tcp.TCP(host_address, int(port))
    try:
        tcp_socket.receive(filename)
        print("[INFO] Plik został odebrany pomyślnie.")
    except Exception as e:
        print("[BŁĄD] Nie można odebrać pliku.", e)
