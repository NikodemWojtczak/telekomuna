import soundcard as sc
import numpy as np
from scipy.io.wavfile import read, write

breakFlag = False
quantization_lvl = None


def calculate_snr(original_signal, quantized_signal):
    noise = original_signal - quantized_signal
    signal_sqr = np.mean(original_signal ** 2)
    noise_sqr = np.mean(noise ** 2)
    snr = 10 * np.log10(signal_sqr / noise_sqr)
    return snr


print("")
print("TELEKOMUNIKACJA I PRZETWARZANIE SYGNAŁÓW - ĆWICZENIE 4. | Autorzy: Kamil Jaśkiewicz, Nikodem Wojtczak")
while True:
    wrong_choice = False
    print("1. Nagranie dźwięku")
    print("2. Odtworzenie dźwięku z pliku wav, SNR")
    print("3. Wyjście z programu")
    print("Twój wybór:")
    choice = input(">> ")
    if choice == "1":
        print("Wybierz poziom kwantyzacji:")
        print("1. 8-bit")
        print("2. 16-bit")
        print("3. 32-bit")
        print("Twój wybór:")
        quantization_lvl_choice = input(">> ")
        if quantization_lvl_choice == "1":
            quantization_lvl = 8
        elif quantization_lvl_choice == "2":
            quantization_lvl = 16
        elif quantization_lvl_choice == "3":
            quantization_lvl = 32
        else:
            print("Nieprawidłowy wybór!")
            wrong_choice = True
        if not wrong_choice:
            print("Wprowadź częstotliwość próbkowania (w Hz)")
            sampling_rate = int(input(">> "))
            print("Wprowadź długość nagrywania (w sekundach)")
            record_seconds = int(input(">> "))
            audio = sc.default_microphone()
            print("Nagrywanie...")
            recorded_audio = audio.record(record_seconds*sampling_rate, sampling_rate)
            original_audio = recorded_audio.copy()
            print("Nagrywanie zakończone.")
            if quantization_lvl == 8:
                recorded_audio = np.int8(recorded_audio / np.max(abs(recorded_audio)) * np.iinfo("int8").max)
            elif quantization_lvl == 16:
                recorded_audio = np.int16(recorded_audio / np.max(abs(recorded_audio)) * np.iinfo("int16").max)
            else:
                recorded_audio = np.int32(recorded_audio / np.max(abs(recorded_audio)) * np.iinfo("int32").max)
            quantized_audio = recorded_audio.astype(np.float64) / np.max(abs(recorded_audio))
            print(calculate_snr(original_audio, quantized_audio))
            print("Wprowadź ścieżkę zapisu pliku z nagraniem")
            filename = input(">> ")
            write(filename, sampling_rate, recorded_audio)
            print("Plik został zapisany.")
    elif choice == "2":
        print("Wprowadź ścieżkę do pliku z nagraniem")
        filename = input(">> ")
        data = read(filename)
        sampling_rate = data[0]
        print("Częstotliwość próbkowania: ", sampling_rate)
        data = np.float64(data[1] / np.max(abs(data[1])))
        channels = []
        for i in range(len(data[0])):
            channels.append(i)
        print("Kanały: ", channels)
        audio = sc.default_speaker()
        audio.play(data, sampling_rate, channels)
        print("Odtwarzanie zakończone.")
    else:
        breakFlag = True
    if breakFlag:
        break
