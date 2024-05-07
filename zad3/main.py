import file_handler as file_h
import frequency_dictionary as freq_d
import tcp
import huffman_tree as ht

huff = ht.Huffman(freq_d.frequency_dictionary)
print("")
print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 3. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
print("Chcesz wysłać plik czy go odebrać?")
print("1. Wyślij plik")
print("2. Odbierz plik")
choice = input("Twój wybór:")
if choice == '1':
    filename1 = input("Wprowadź ścieżkę do pliku z komunikatem tekstowym do przesłania:")
    message = file_h.read_message(filename1)
    filename2 = input("Wprowadź ścieżkę zapisu pliku z zakodowanym komunikatem:")
    encoded_message = ht.encode(huff.nodes[0], message)
    file_h.write_message(filename2, encoded_message)
    print("--- USTAWIANIE POŁĄCZENIA - TWORZENIE GNIAZDA SIECIOWEGO ---")
    host_address = input("Podaj adres hosta:")
    port = input("Podaj port:")
    tcp_socket = tcp.TCP(host_address, int(port))
    try:
        tcp_socket.send_file(filename2)
        print("Plik został przesłany pomyślnie.")
    except Exception:
        print("[BŁĄD] Nie można wysłać pliku.")
elif choice == '2':
    filename1 = input("Wprowadź ścieżkę zapisu odebranego, zakodowanego pliku:")
    filename2 = input("Wprowadź ścieżkę zapisu zdekodowanego pliku:")
    print("--- USTAWIANIE POŁĄCZENIA - TWORZENIE GNIAZDA SIECIOWEGO ---")
    host_address = input("Podaj adres hosta:")
    port = input("Podaj port:")
    tcp_socket = tcp.TCP(host_address, int(port))
    try:
        tcp_socket.receive_file(filename1)
        encoded_message = file_h.read_message(filename1)
        decoded_message = ht.decode(huff.nodes[0], encoded_message)
        file_h.write_message(filename2, decoded_message)
        print("Plik został odebrany pomyślnie.")
    except Exception:
        print("[BŁĄD] Nie można odebrać pliku.")
