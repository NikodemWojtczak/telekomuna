import error_correction as ec
import file_handler as fh

# napis = "hello"
#
# print("Napis: ", napis)
# napis_zakodowany = ec.encode_string(napis)
# print(fh.print_binary_string(napis_zakodowany))
# napis_zakodowany = list(napis_zakodowany)
# napis_zakodowany[0] = '1'
# napis_zakodowany[19] = '1'
# napis_zakodowany[37] = '0'
# napis_zakodowany = ''.join(napis_zakodowany)
# print(fh.print_binary_string(napis_zakodowany))
# print(ec.verify_string(napis_zakodowany))

is_message = False
is_encoded = False


print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 1.")
print("Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
while True:
    if is_encoded:
        print("Możesz wprowadzić zmiany w pliku 'komunikat_przed_transmisja_zakodowany.txt',")
        print("jednak nie może to być na ten moment więcej niż 1 błąd na słowo.")
    print("1. Wprowadź wiadomość")
    print("2. Zakoduj wiadomość przed transmisją")
    print("3. Odbiór wiadomości i weryfikacja")
    print("4. Wyjście")
    print("Wybór: ", end='')
    choice = input()
    if choice == '1':
        print("Podaj komunikat: ", end='')
        message = input()
        fh.write_message("komunikat_przed_transmisja.txt", message)
        print("Zapisano komunikat do pliku 'komunikat_przed_transmisja.txt'")
        is_message = True
    elif choice == '2':
        if is_message:
            message = fh.read_message("komunikat_przed_transmisja.txt")
            encoded_message = ec.encode_string(message)
            fh.write_binary_message("komunikat_przed_transmisja_zakodowany.txt", encoded_message)
            print("Zapisano zakodowany komunikat do pliku 'komunikat_przed_transmisja_zakodowany.txt")
            is_encoded = True
    elif choice == '3':
        if is_encoded:
            send_message = fh.read_binary_message("komunikat_przed_transmisja_zakodowany.txt")
            error_positions = ec.verify_string(send_message)
            if len(error_positions) == 0:
                print("Podczas transmisji nie napotkano błędów.")
            else:
                error_positions_string = ", ".join(str(v) for v in error_positions)
                print("Po odebraniu wiadomości wykryto błędy na pozycjach: ", error_positions_string)
                send_message = ec.correct_string(send_message, error_positions)
                send_message_decoded = ec.decode_string(send_message)
                print("Błędy zostały poprawione. Odebrano wiadomość o treści: ", send_message_decoded)
    elif choice == '4':
        break

