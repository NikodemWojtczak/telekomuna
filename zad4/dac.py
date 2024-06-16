import soundcard as sc
import numpy as np
from scipy.io.wavfile import read


def snr(a, axis=0, ddof=0):
    # konwersja sygnału wejściowego na tablicę numpy
    a = np.asanyarray(a)
    # wyznaczenie średniej sygnału względem kolumn
    m = a.mean(axis)
    # obliczenie odchylenia standardowego względem kolumn, ddof - stopień swobody
    sd = a.std(axis=axis, ddof=ddof)
    # zwraca dwudziestokrotność logarytmu dziesiętnego ze stosunku średniej do odchylenia standardowego sygnału
    # tam gdzie odchylenie standardowe wynosi 0, przyjmujemy stosunek za 0
    # stosunek sygnału do szumu jest wartością wyrażoną w decybelach
    return abs(20*np.log10(abs(np.where(sd == 0, 0, m/sd))))


class Player:  # klasa umożliwiająca odtwarzanie

    def __init__(self, device=None) -> None:
        # przypisanie urządzenia tak jak w Recorder, tym razem wybieramy głośnik
        self.device = device if device is not None else sc.default_speaker()

    def play_from_file(self, filename: str):
        # odczytanie zawartości pliku .wav
        data = read(filename)
        # pobranie częstotliwości próbkowania
        samplerate = data[0]
        print("[INFO] Częstotliwość próbkowania zapisanego nagrania: {}".format(samplerate))
        # przygotowanie danych w sposób umożliwiający ich odtworzenie (normalizacja)
        data = np.float64(data[1]/np.max(abs(data[1])))
        channels = []
        # pobranie listy zawierającej kanały
        for i in range(len(data[0])):
            channels.append(i)
        print("[INFO] Ilość kanałów: {}".format(len(channels)))
        # odtworzenie nagrania
        self.device.play(data, samplerate, channels)
        # zwrócenie stosunku sygnału do szumu
        return snr(data)
