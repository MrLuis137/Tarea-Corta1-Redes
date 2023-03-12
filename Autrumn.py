import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
import threading
from scipy.io.wavfile import write

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
frames = []
recording = False

def recordingAudio():
    global recording
    recording = False




def startRecording():
    global recording
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []
    recording = True
    while(recording):
        data = stream.read(CHUNK)
        numpydata = np.frombuffer(data, dtype=np.int16)
        frames.append(numpydata)

    plt.plot(frames)
    plt.show()

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def start_recording_thread():
    x = threading.Thread(target=startRecording)
    x.start()

window = tk.Tk()
window.title("Autrumn")




start_recording_button = ttk.Button(
    window,
    text='Start recording',
    compound=tk.LEFT,
    command=start_recording_thread
)

start_recording_button.pack(
    expand=True
)

stop_recording_button = ttk.Button(
    window,
    text='Stop recording',
    compound=tk.LEFT,
    command=recordingAudio
)

stop_recording_button.pack(
    expand=True
)

open_audio_button = ttk.Button(
    window,
    text='Open audio',
    compound=tk.LEFT,
    command=recordingAudio
)

open_audio_button.pack(
    expand=True
)
window.geometry("700x350")
window.mainloop()