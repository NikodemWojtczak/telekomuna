from typing import Optional
import soundcard as sc
import numpy as np
from scipy.io.wavfile import write


class Recorder:  # klasa umożliwiająca nagrywanie

    def __init__(self, device=None, samplerate: Optional[int] = 48000, channels=None) -> None:
        # self.channels określa, w jakim trybie będzie nagrywany dźwięk, jest to lista
        # jeżeli wybrano [0], to nagrywamy na jednym kanale (mono)
        # jeżeli wybrano [0,1], to nagrywamy na dwóch kanałach (stereo) (domyślnie)
        self.channels = channels if channels is not None else [0, 1]
        # wybieramy domyślne urządzenie mikrofonu w systemie do nagrywania (domyślnie)
        self.device = device if device is not None else sc.default_microphone()
        # ustawiamy częstotliwość próbkowania (liczba całkowita, w Hz)
        self.samplerate = samplerate
        # zmienna przechowująca nagranie (w formie np.ndarray)
        self.recording = None

    def record(self, seconds: int) -> None:
        # nagrywanie dźwięku
        # pierwszy argument określa ilość próbek dźwięku do pobrania w czasie nagrywania
        # drugi argument określa częstotliwość próbkowania
        # trzeci argument określa tryb nagrywania (domyślnie stereo, lista [0,1])
        self.recording = self.device.record(int(seconds * self.samplerate), self.samplerate, self.channels)

    def get_recording(self) -> np.ndarray:
        # zwracanie nagrania
        return self.recording

    def save_to_file(self, filename: str, quant: Optional[int] = 16) -> None:
        # program umożliwia kwantyzacje: 8-bit unsigned PCM, 16-bit PCM, 32-bit PCM
        if quant not in [8, 16, 32]:
            raise Exception("[Błąd] Poziom kwantyzacji może wynieść 8, 16 lub 32 bity.")
        data = self.recording
        # formatujemy nagranie do zapisu (dokonujemy kwantyzacji)
        # dzielimy próbki dźwięku przez próbkę o największej wartości (normalizacja), a potem skalujemy
        # do przedziału odpowiadającego typowi (uint8, int16, int32)
        if quant == 8:  # PCM 8-bit unsigned
            data = np.uint8(data / np.max(abs(data)) * np.iinfo("uint8").max)
        if quant == 16:  # PCM 16-bit
            data = np.int16(data / np.max(abs(data)) * np.iinfo("int16").max)
        if quant == 32:  # PCM 32-bit
            data = np.int32(data / np.max(abs(data)) * np.iinfo("int32").max)
        # zapis skwantyzowanego nagrania
        # pierwszy argument to nazwa pliku
        # drugi argument to częstotliwość próbkowania
        # trzeci argument to tablica z danymi
        write(filename, self.samplerate, data)
