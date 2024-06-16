from adc import Recorder
from dac import Player


can_continue = False
main_recorder = Recorder()
main_player = Player()
quantization = 16


print("")
print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 4. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
while True:
    print("1. Ustalenie częstotliwości próbkowania i poziomu kwantyzacji")
    print("2. Nagrywanie")
    print("3. Odtwarzanie, snr")
    print("4. Wyjście")
    print("Twój wybór:")
    choice = input(">> ")
    if choice == "1":
        try:
            print("Podaj częstotliwość próbkowania")
            main_recorder.samplerate = abs(int(input(">> ")))
        except:
            print("[BŁĄD] Wprowadzono niewłaściwą częstotliwość. Wybieram domyślną: 48 kHz")
            main_recorder.samplerate = 48000
        try:
            print("Podaj poziom kwantyzacji (8, 16, 32)")
            quantization = int(input(">> "))
        except:
            print("[BŁĄD] Wprowadzono niewłaściwy poziom kwantowania. Wybieram domyślny: 16-bit")
            quantization = 16
        can_continue = True
    if choice == "2" and can_continue:
        print("Podaj długość nagrywania")
        record_seconds = int(input(">> "))
        print("[INFO] Rozpocząłem nagrywanie...")
        main_recorder.record(record_seconds)
        print("[INFO] Skończyłem nagrywanie.")
        print("Podaj ścieżkę zapisu pliku z nagraniem (bez rozszerzenia)")
        filename = input(">> ")
        main_recorder.save_to_file("{}.wav".format(filename), quantization)
        print("[INFO] Zapisano.")
    if choice == "3":
        print("Podaj ścieżkę do pliku z nagraniem (bez rozszerzenia)")
        filename = input(">> ")
        print("[INFO] Odtwarzam nagranie...")
        snr = main_player.play_from_file("{}.wav".format(filename))
        print("[INFO] Skończyłem odtwarzanie.")
        print("SNR dla nagrania wynosi {} dB".format(snr))
    if choice == "4":
        break
