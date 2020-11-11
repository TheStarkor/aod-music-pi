import pyaudio
import wave
import audioop

import sys
import webrtcvad
import numpy as np
from mic_array import MicArray
from pixel_ring import pixel_ring

import requests

CHUNK = 1024
TARGET = 2100
FORMAT = pyaudio.paInt16
RECORD_SECONDS = 120
WAVE_OUTPUT_FILENAME = "output.wav"
RATE = 16000
CHANNELS = 4
VAD_FRAMES = 10     # ms
DOA_FRAMES = 200    # ms

p = pyaudio.PyAudio()

def main():

    tream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    vad = webrtcvad.Vad(3)

    speech_count = 0
    chunks = []
    doa_chunks = int(DOA_FRAMES / VAD_FRAMES)

    try:
        with MicArray(RATE, CHANNELS, RATE * VAD_FRAMES / 1000)  as mic:
            for chunk in mic.read_chunks():
                # Use single channel audio to detect voice activity
                if vad.is_speech(chunk[0::CHANNELS].tobytes(), RATE):
                    speech_count += 1
                    sys.stdout.write('1')
                else:
                    sys.stdout.write('0')

                sys.stdout.flush()

                data = stream.read(CHUNK)
                rms = audioop.rms(data, 2)

                data = np.fromstring(data)
                fft = abs(np.fft.fft(data).real)
                fft = fft[:int(len(fft)/2)]
                freq = np.fft.fftfreq(CHUNK, 1.0/RATE)
                freq = freq[:int(len(freq)/2)]
                val = fft[np.where(freq>TARGET)[0][0]]

                chunks.append(chunk)
                if len(chunks) == doa_chunks:
                    if speech_count > (doa_chunks / 2):
                        frames = np.concatenate(chunks)
                        direction = mic.get_direction(frames)
                        pixel_ring.set_direction(direction)
                        res = requests.post('http://13.209.217.37/api', data={'location': int(direction)}).json()
                        print('\ndirection: {} volume: {} frequency: {}'.format(int(direction), int(rms), int(val)))

                    speech_count = 0
                    chunks = []

    except KeyboardInterrupt:
        pass
        
    pixel_ring.off()


if __name__ == '__main__':
    main()