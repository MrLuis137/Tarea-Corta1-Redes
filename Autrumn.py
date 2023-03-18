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
from scipy.fft import rfft, fftfreq, fftshift, irfft
import time
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
        files = zip.namelist()
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
                frames = zip.read(files[i])
            
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
    vec_fourier_frames = []
    
    i = 0
    while(recording):

        data = stream.read(CHUNK)
        numpydata = np.frombuffer(data, dtype=np.int16)
        frames.append(numpydata)
        
        #Se calcula la transformada de fourier
        '''transformada = rfft(numpydata) 
         
        # Concatenación de la mitad de la Transformada de Fourier con su reflexión simétrica
        full_spectrum = np.concatenate((transformada, np.flip(transformada)))
        
        #para mostrar ambos lados del espectro
        
        shifted_spectrum =  np.fft.fftshift(full_spectrum)

        
        #se agrega el nuevo calculo a los frames antes calculados
        fourier_frames.append(np.real(shifted_spectrum))'''
        
         # Calcular transformada de Fourier
        fft_data = np.fft.fft(numpydata)
        freqs = np.fft.fftfreq(len(numpydata), d=1/RATE)
        
        fourier_frames.append(fft_data)  #datos  de la transformada
        vec_fourier_frames.append(freqs)  #datos de frecuencia de la transformada
        
        print("freq->",np.hstack(fft_data).shape)
        print("data-> ",np.hstack((np.abs(freqs)).shape))
      
        
        if(i>=int(RATE / CHUNK * RECORD_SECONDS)):
            updatetimecanvas(np.hstack(frames))
            updatefouriercanvas(fft_data,freqs)
            
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
fig2.add_subplot(111).hist(fourier_frames, bins=100)

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


'''def updatefouriercanvas(freqframe):
    fig2.clear()
    
    ax = fig2.add_subplot(111)
    ax.hist(freqframe, bins=350)
    
     
    ax.set_xlabel('Magnitud')
    ax.set_ylabel('Frecuencia')
    #ax.set_xlim(-3000, 3000)
    canvas2.draw_idle()'''
    
def updatefouriercanvas(fft_data,freqs):
    fig2.clear()
    
    ax = fig2.add_subplot(111)
    ax.hist(freqs, bins=100, weights=np.abs(fft_data))
    
     
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel('Conteo') #cantidad de veces que aparece cada frecuencia en el espectro de Fourier
    #ax.set_xlim(-3000, 3000)
    canvas2.draw_idle()
    

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


 