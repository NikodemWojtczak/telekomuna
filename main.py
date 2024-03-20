import error_correction as ec
import file_handler as fh
import os

is_message = False
is_encoded = False


def is_binary_valid(binary_string):
    if not all(char in '01' for char in binary_string):
        return False
    if len(binary_string) % 16 != 0:
        return False
    if len(binary_string) == 0:
        return False
    return True


print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 1. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
while True:
    mess = ""
    print("")
    print("----- PONIŻEJ ZNAJDĄ SIĘ WARTOŚCI ODCZYTANE Z PLIKÓW, O ILE SĄ ONE POPRAWNE. -----")
    if os.path.exists("komunikat_przed_transmisja.txt"):
        mess = fh.read_message("komunikat_przed_transmisja.txt")
        if len(mess) > 0:
            print("")
            print("--- W PLIKU ZNAJDUJE SIĘ NASTĘPUJĄCY KOMUNIKAT: ---")
            print(mess)
            print("")
            print("--- POSTAĆ BINARNA WIADOMOŚCI: ---")
            print(ec.string_to_binary(mess))
            print("")
            is_message = True
        else:
            is_message = False
    if os.path.exists("komunikat_przed_transmisja_zakodowany.txt"):
        decoded_message = ""
        binary_message = fh.read_binary_message("komunikat_przed_transmisja_zakodowany.txt")
        if is_binary_valid(binary_message):
            decoded_message = ec.decode_string(binary_message)
        if decoded_message == mess and len(ec.verify_string(binary_message)) == 0:
            is_encoded = True
            fh.write_binary_message("komunikat_otrzymany_zakodowany.txt", binary_message)
        else:
            is_encoded = False
    if is_encoded:
        print("--- WIADOMOŚĆ ZAKODOWANA: ---")
        print(fh.read_binary_message("komunikat_przed_transmisja_zakodowany.txt"))
        print("")
        print("UWAGA: Możesz wprowadzić zmiany w pliku 'komunikat_otrzymany_zakodowany.txt',"
              "jednak nie może to być więcej niż 2 błędy na 16 bitów.")
    print("")
    print("1. Wprowadź wiadomość lub zmień treść wiadomości")
    print("2. Zakoduj wiadomość przed transmisją")
    print("3. Odbiór wiadomości i weryfikacja")
    print("4. Wyjście")
    print("Wybór: ", end='')
    choice = input()
    if choice == '1':
        print("Podaj komunikat: ", end='')
        message = input()
        fh.write_message("komunikat_przed_transmisja.txt", message)
        print("*** UWAGA: Zapisano komunikat do pliku 'komunikat_przed_transmisja.txt' ***")
        is_message = True
    elif choice == '2':
        if is_message and not is_encoded:
            message = fh.read_message("komunikat_przed_transmisja.txt")
            encoded_message = ec.encode_string(message)
            fh.write_binary_message("komunikat_przed_transmisja_zakodowany.txt", encoded_message)
            print("*** UWAGA: Zapisano zakodowany komunikat do pliku 'komunikat_przed_transmisja_zakodowany.txt'."
                  "Można wprowadzać błędy w pliku 'komunikat_otrzymany_zakodowany.txt'. ***")
            is_encoded = True
        else:
            print("*** NAPOTKANO BŁĄD ***")
            print("*** UWAGA: Brak wiadomości, którą można zakodować, bądź wiadomość została już zakodowana. ***")
    elif choice == '3':
        if is_encoded:
            print("*** UWAGA: Odczytuję wiadomość z pliku 'komunikat_otrzymany_zakodowany.txt' ***")
            send_message = fh.read_binary_message("komunikat_otrzymany_zakodowany.txt")
            if is_binary_valid(send_message):
                print("*** UWAGA: Wiadomość odebrana pomyślnie. ***")
                error_positions = ec.verify_string(send_message)
                if len(error_positions) == 0:
                    print("*** WIADOMOŚĆ POPRAWNA. NIE NAPOTKANO BŁĘDÓW. ***")
                else:
                    error_positions_string = ", ".join(str(v) for v in error_positions)
                    print(f"*** UWAGA: W WIADOMOŚCI ZNALEZIONO BŁĘDY NA POZYCJACH {error_positions_string} ***")
                    send_message = ec.correct_string(send_message, error_positions)
                    print("*** BŁĘDY ZOSTAŁY POPRAWIONE. ***")
            else:
                print("*** NAPOTKANO BŁĄD ***")
                print("*** UWAGA: W odebranej wiadomości napotkano błędy, które nie pozwalają na jej odczyt. ***")
                print("*** Liczba bitów może nie być wielokrotnością 16, wiadomość jest pusta bądź w wiadomości"
                      " znajdują się niedopuszczalne znaki.")
            send_message_decoded = ec.decode_string(send_message)
            print(f"*** ODEBRANA WIADOMOŚĆ: {send_message_decoded} ***")
        else:
            print("*** NAPOTKANO BŁĄD ***")
            print("*** UWAGA: Wiadomość nie została zakodowana. Zakoduj ją przed próbą jej odebrania. ***")
    elif choice == '4':
        break

