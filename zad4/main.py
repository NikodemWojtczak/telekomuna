import pyaudio
import wave
import numpy as np
from scipy.io import wavfile

breakFlag = False
quantization_lvl = None
CHANNELS = 2
CHUNK = 1024


# def calculate_snr(original_signal, quantized_signal):
#     noise = original_signal - quantized_signal
#     signal_sqr = np.mean(original_signal ** 2)
#     noise_sqr = np.mean(noise ** 2)
#     snr = 10 * np.log10(signal_sqr / noise_sqr)
#     return snr


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
            quantization_lvl = pyaudio.paInt8
        elif quantization_lvl_choice == "2":
            quantization_lvl = pyaudio.paInt16
        elif quantization_lvl_choice == "3":
            quantization_lvl = pyaudio.paInt32
        else:
            print("Nieprawidłowy wybór!")
            wrong_choice = True
        if not wrong_choice:
            print("Wprowadź częstotliwość próbkowania (w Hz)")
            sampling_rate = int(input(">> "))
            print("Wprowadź długość nagrywania (w sekundach)")
            record_seconds = int(input(">> "))
            p = pyaudio.PyAudio()
            stream = p.open(format=quantization_lvl,
                            channels=CHANNELS,
                            rate=sampling_rate,
                            frames_per_buffer=CHUNK,
                            input=True)
            print("Nagrywanie...")
            frames = []
            for i in range(0, int(sampling_rate / CHUNK * record_seconds)):
                data = stream.read(CHUNK)
                frames.append(data)
            print("Nagrywanie zakończone.")
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("Wprowadź ścieżkę zapisu pliku z nagraniem")
            filename = input(">> ")
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(quantization_lvl))
            wf.setframerate(sampling_rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            print("Plik został zapisany.")
    elif choice == "2":
        print("Wprowadź ścieżkę do pliku z nagraniem")
        filename = input(">> ")
        wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        while len(data := wf.readframes(CHUNK)):
            stream.write(data)
        stream.close()
        p.terminate()
    else:
        breakFlag = True
    if breakFlag:
        break
