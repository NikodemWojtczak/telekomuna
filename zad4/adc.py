from typing import Optional
import soundcard as sc
import numpy as np
from scipy.io.wavfile import write

class Recorder:

    def __init__(self, device=None, samplerate: Optional[int] = 48000, channels=None) -> None:
        self.channels = channels if channels is not None else [0, 1]
        self.device = device if device is not None else sc.default_microphone()
        self.samplerate = samplerate
        self.recording = None

    def record(self, seconds: int) -> None:
        self.recording = self.device.record(int(seconds * self.samplerate), self.samplerate, self.channels)

    def get_recording(self) -> np.ndarray:
        return self.recording

    def save_to_file(self, filename: str, quant: Optional[int] = 16) -> None:
        if quant not in [8, 16, 32]:
            raise Exception("[Błąd] Poziom kwantyzacji może wynieść 8, 16 lub 32 bity.")
        data = self.recording
        if quant == 8:
            data = np.uint8(data / np.max(abs(data)) * np.iinfo("uint8").max)
        if quant == 16:
            data = np.int16(data / np.max(abs(data)) * np.iinfo("int16").max)
        if quant == 32:
            data = np.int32(data / np.max(abs(data)) * np.iinfo("int32").max)
        write(filename, self.samplerate, data)
