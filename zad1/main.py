import error_correction as ec
import file_handler as fh
import os

is_message = False  # flaga sprawdzająca czy istnieje komunikat do transmisji
is_encoded = False  # flaga sprawdzająca czy wybrany komunikat został zakodowany

print("")
print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 1. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
while True:
    mess = ""  # wybrany komunikat do transmisji
    print("")
    print("JEŻELI DANE W PLIKACH SĄ SFORMATOWANE POPRAWNIE, ZOSTANĄ PONIŻEJ WYŚWIETLONE.")
    print("-----------------------------------------------------------------------------"
          "-------------------------------------------------------")
    if os.path.exists("do_wyslania.txt"):  # wypisanie wybranego komunikatu z pliku czysto informacyjnie
        mess = fh.read_message("do_wyslania.txt")
        if len(mess) > 0:
            print("WYBRANY KOMUNIKAT DO WYSŁANIA --> ", end='')
            print(mess, end='')
            print(", DŁUGOŚĆ:", len(mess))
            is_message = True
        else:
            is_message = False
    if os.path.exists("komunikat_zakodowany.txt"):  # sprawdzenie czy zakodowana wiadomość w pliku
        decoded_message = ""                                         # jest poprawna i czy odpowiada wybranej wiadomości
        binary_message = fh.read_message("komunikat_zakodowany.txt")
        binary_message = ec.string_to_binary(binary_message)
        if ec.is_binary_valid(binary_message):
            decoded_message = ec.decode_string(binary_message)  # jeżeli jest ok to wypisujemy potem zakodowaną
        if decoded_message == mess and len(ec.verify_string(binary_message)) == 0:  # wiadomość na ekran w celach
            is_encoded = True                                                       # informacyjnych
        else:
            is_encoded = False
    if is_encoded:  # wypisanie zakodowanej wiadomości która jest w pliku
        print("WIADOMOŚĆ ZAKODOWANA -----------> ", end="")
        zakodowana = fh.read_message("komunikat_zakodowany.txt")
        print(zakodowana, end="")
        print(", DŁUGOŚĆ:", len(zakodowana))
        print("[INFO] Możesz wprowadzić zmiany w pliku 'komunikat_zakodowany_bin.txt',"
              " jednak nie może to być więcej niż 2 błędy na 16 bitów.")
    print("-----------------------------------------------------------------------------"
          "-------------------------------------------------------")
    print("1. Wprowadź wiadomość lub zmień treść wiadomości")
    print("2. Zakoduj wiadomość przed transmisją, zresetuj wcześniej wprowadzone błędy")
    print("3. Odbierz wiadomość, zweryfikuj ją, popraw")
    print("4. Wyjście")
    print("[INFO] Wybranie innej opcji spowoduje zaktualizowanie odczytanych wiadomości z plików.")
    print("WYBÓR: ", end='')
    choice = input()
    if choice == '1':  # wybór komunikatu
        print("PODAJ KOMUNIKAT: ", end='')
        message = input()
        fh.write_message("do_wyslania.txt", message)
        print("[INFO] Zapisano komunikat. Znajduje się w pliku 'do_wyslania.txt'.")
        input("WYBIERZ ENTER ABY KONTYNUOWAĆ...")
        is_message = True
    elif choice == '2':  # zakodowanie wiadomości, zresetowanie błędów w pliku
        if is_message:
            message = fh.read_message("do_wyslania.txt")
            encoded_message = ec.encode_string(message)
            encoded_message_string = ec.binary_to_string(encoded_message)
            fh.write_message("komunikat_zakodowany.txt", encoded_message_string)
            fh.write_message("komunikat_zakodowany_bin.txt", encoded_message)
            print("[INFO] Zakodowano komunikat. Znajduje się w pliku 'komunikat_zakodowany.txt'.")
            print("[INFO] Po kontynuowaniu, możliwe będzie wprowadzanie błędów w pliku "
                  "'komunikat_zakodowany_bin.txt'.")
            is_encoded = True
        else:
            print("[BŁĄD] Brak wiadomości do zakodowania.")
        input("WYBIERZ ENTER ABY KONTYNUOWAĆ...")
    elif choice == '3':  # odbiór wiadomości, weryfikacja, poprawki
        if is_encoded:
            print("[INFO] Odczytywanie wiadomości z pliku 'komunikat_zakodowany_bin.txt'.")
            send_message = fh.read_message("komunikat_zakodowany_bin.txt")
            if ec.is_binary_valid(send_message):
                print("[INFO] Wiadomość odczytana pomyślnie.")
                error_positions = ec.verify_string(send_message)
                if len(error_positions) == 0:
                    print("[INFO] Nie wykryto błędów w odebranej wiadomości.")
                else:
                    error_positions_string = ", ".join(str(v) for v in error_positions)
                    print(f"[INFO] Znaleziono błędy w odebranej wiadomości na pozycjach: {error_positions_string}")
                    send_message = ec.correct_string(send_message, error_positions)
                    print("[INFO] Błędy zostały poprawione.")
                send_message_decoded = ec.decode_string(send_message)
                fh.write_message("komunikat_otrzymany.txt", send_message_decoded)
                print(f"[INFO] Odebrano wiadomość o treści: '{send_message_decoded}'.")
                print("[INFO] Zapisano odebraną wiadomość w pliku 'komunikat_otrzymany.txt'.")

            else:
                print("[BŁĄD] Odebrana wiadomość nie ma poprawnego formatowania.")
                print("[BŁĄD] Możliwe przyczyny: długość wiadomości nie jest wielokrotnością 16, w wiadomości znajdują"
                      " się niedopuszczalne znaki, wiadomość jest pusta.")
        else:
            print("[BŁĄD] Wiadomość nie została zakodowana.")
        input("WYBIERZ ENTER ABY KONTYNUOWAĆ...")
    elif choice == '4':
        break
