import os
import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
import threading
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from zipfile import ZipFile
from scipy.io.wavfile import write
from os import remove

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2
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

    global frames
    frames = []
    recording = True
    i = 0
    while(recording):

        data = stream.read(CHUNK)
        numpydata = np.frombuffer(data, dtype=np.int16)
        frames.append(numpydata)
        if(i>=int(RATE / CHUNK * RECORD_SECONDS)):
            updatetimecanvas(np.hstack(frames))
            i=0

        i+=1

    numpyarrayfinal = np.hstack(frames)
    updatetimecanvas(numpyarrayfinal)

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



fig = Figure(figsize=(5, 3), dpi=100)
fig.add_subplot(111).plot(frames)
fig2 = Figure(figsize=(5, 3), dpi=100)
fig2.add_subplot(111).plot()

frame1 = tk.Frame(window)
frame2 = tk.Frame(window)

canvas = FigureCanvasTkAgg(fig, window)
toolbar = NavigationToolbar2Tk(canvas, frame1)
canvas2 = FigureCanvasTkAgg(fig2, window)
toolbar2 = NavigationToolbar2Tk(canvas2, frame2)


def updatetimecanvas(timeframe):


    fig.clear()
    fig.add_subplot(111).plot(timeframe)  # generate random x/y
    canvas.draw_idle()



frame1.pack(side=tk.TOP, fill=tk.X)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.X)
frame2.pack(side=tk.TOP, fill=tk.X)
canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.X)

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
window.geometry("700x1200")
window.mainloop()

#---ARCHIVOS_ATM-----

def to_atm(chunksList, wavFilePath):
    file = open("chunks.s", "w+")
    content = str(chunksList)
    file.write(content)
    with ZipFile('file.atm', 'w') as zip:
         zip.write('chunks.s')
         zip.write(wavFilePath)
    try:
        os.remove("chunks.s")
    except:
        print("File already deleted")