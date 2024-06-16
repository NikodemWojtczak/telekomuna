from typing import Optional
import soundcard as sc
import numpy as np
from scipy.io.wavfile import read


def snr(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return abs(20*np.log10(abs(np.where(sd == 0, 0, m/sd))))


class Player:

    def __init__(self, device=None) -> None:
        self.device = device if device is not None else sc.default_speaker()

    def play_from_file(self, filename: str):
        data = read(filename)
        samplerate = data[0]
        print("[INFO] Częstotliwość próbkowania zapisanego nagrania: {}".format(samplerate))
        data = np.float64(data[1]/np.max(abs(data[1])))
        channels = []
        for i in range(len(data[0])):
            channels.append(i)
        print("[INFO] Ilość kanałów: {}".format(len(channels)))
        self.device.play(data, samplerate, channels)
        return snr(data)
