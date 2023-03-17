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
from scipy.fft import fft, fftfreq, fftshift

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
frames = []

fourier_frames = []
vec_fourier_frames = []

recording = False
wavFile= []

lenght=0

# ----Transformada de Fourier-----
N = 400  # Número de puntos de muestra
T = 1.0 / 800.0  # Espaciado de muestra

#---ARCHIVOS_ATM-----

def to_atm(chunksList, wavFilePath):
    file = open("chunks", "w+")
    content = str(chunksList)
    file.write(content)
    file.close
    with ZipFile('file.atm', 'w') as zip:
         zip.write('chunks')
         zip.write(wavFilePath)
    try:
        os.remove("./chunks")
    except:
        print("File already deleted")

def from_atm(filepath):
    with ZipFile(filepath) as zip:
        files = zip.namelist();
       # print(files)
        for i in range(0,len(files)):
            if(files[i] == WAVE_OUTPUT_FILENAME):
                global wavFile
                zip.extract(files[i])
                wavFile = open_wav_file(files[i])
                print("wavFile")
                print(wavFile)
            elif(files[i] == WAVE_OUTPUT_FILENAME):
                global frames
                frames = zip.read(files[i]);
            
            #print(zip.read(files[i]))

#---ARCHIVOS_ATM-----

def open_wav_file(file):
    #en progreso
    return wave.open(file, 'rb')

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
    global fourier_frames
    fourier_frames = []
    global vec_fourier_frames
    vec_fourier_frames = []= []
    
    i = 0
    while(recording):

        data = stream.read(CHUNK)
        numpydata = np.frombuffer(data, dtype=np.int16)
        frames.append(numpydata)
        
        #Se calcula la transformada de fourier
        transformada = fft(numpydata) 
        
        #Se calcula la magnitud de la transformada de FOurier y se normaliza
        fft_mag = np.abs(transformada)
        fft_mag = fft_mag / np.max(fft_mag)
        
        
        #se agrega el nuevo calculo a los frames antes calculados
        fourier_frames.append(fft_mag)
        
        
        #lenght=len(numpydata)
        #vec_frec = fftfreq(N, T)[:N//2]  #vector de frecuencia correspondiente a los coeficientes de la trasnformada de fourier
        #vec_fourier_frames.append(vec_frec) 
        #fourier_frames.append(transformada)

        #print("tiemp-> ",numpydata)
        #print("freq-> ",transformada)
        
        #Se reorganiza el espectro de frecuencias utilizando la funcion ffshift de spicy
        '''vec_frec=fftshift(vec_frec)
        transformada_plot=fftshift(transformada)
        vec_fourier_frames.append(vec_frec) 
        fourier_frames.append(transformada_plot)'''
 
        
        if(i>=int(RATE / CHUNK * RECORD_SECONDS)):
            updatetimecanvas(np.hstack(frames))
            updatefouriercanvas(np.hstack(fourier_frames))
            #updatefreqcanvas( transformada_plot,vec_frec)
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
    to_atm(frames, WAVE_OUTPUT_FILENAME)
    #test
   # print(frames)
   # print(wavFile)
    from_atm("file.atm")
    #print("frames")
    #print(frames)
    #print("wav file")
   # print(wavFile)





def start_recording_thread():
    x = threading.Thread(target=startRecording)
    x.start()

    
window = tk.Tk()
window.title("Autrumn")



fig = Figure(figsize=(5, 3), dpi=100)
fig.add_subplot(111).plot(frames)
fig2 = Figure(figsize=(5, 3), dpi=100)
fig2.add_subplot(111).hist(fourier_frames, bins=100, range=(0, 1), log=True)

frame1 = tk.Frame(window)
frame2 = tk.Frame(window)

canvas = FigureCanvasTkAgg(fig, window)
toolbar = NavigationToolbar2Tk(canvas, frame1)
canvas2 = FigureCanvasTkAgg(fig2, window)
toolbar2 = NavigationToolbar2Tk(canvas2, frame2)



def updatetimecanvas(timeframe):


    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(timeframe)
    ax.set_xlabel('Tiempo(s)')
    ax.set_ylabel('Amplitud')
    canvas.draw_idle()


def updatefouriercanvas(freqframe):
    fig2.clear()
    ax = fig2.add_subplot(111)
    ax.hist(freqframe, bins=100, range=(0, 1), log=True)
    ax.set_xlabel('Magnitud')
    ax.set_ylabel('Frecuencia')
    canvas2.draw_idle()
    
'''
def updatefreqcanvas(fourierframe, freq_frame):
    fig2.clear()
    ax = fig2.add_subplot(111)
    ax.plot(freq_frame, 2.0/N * np.abs(fourierframe[0:N//2]))
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel('Amplitud')
    canvas2.draw_idle()
'''
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


# ----Transformada de Fourier-----
N = 600  # Número de puntos de muestra
T = 1.0 / 800.0  # Espaciado de muestra

def fourier():
    global fourier_frames
    fourier_frames = []
    global vec_fourier_frames
    vec_fourier_frames = []= []
    i=0
    print("* TRANSFORMA")
    while (len(frames)>i):
        array = frames[i]  #se toma un chunck
        transformada = fft(array)  #transformada de fourier
        vec_frec = xf = fftfreq(N, T)[:N//2]  #vector de frecuencia correspondiente a los coeficientes de la trasndormada de fourier
        vec_fourier_frames.append(vec_frec) 
        fourier_frames.append(transformada)
        updatefreqcanvas(transformada,vec_frec)
        
        i+=1
        