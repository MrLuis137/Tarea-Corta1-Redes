# main layout for multiple pages
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/

# menu
# https://www.pythontutorial.net/tkinter/tkinter-menu/
# https://www.tutorialsteacher.com/python/create-gui-using-tkinter-python

import tkinter as tk
from tkinter import ttk  
from tkinter import Menu
import os
import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt
import threading
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from zipfile import ZipFile
from scipy.io.wavfile import write
from os import remove
import time
 
LARGEFONT =("Verdana", 35)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
frames = []
recording = False


    #---ARCHIVOS_ATM-----

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
        print(files)
        for i in range(0,len(files)):
            if(files[i] == WAVE_OUTPUT_FILENAME):
                global wavFile
                zip.extract(files[i])
                wavFile = open_wav_file(files[i])
            elif(files[i] == WAVE_OUTPUT_FILENAME):
                global frames
                frames = zip.read(files[i]);
            
            print(zip.read(files[i]))

#---ARCHIVOS_ATM-----

def open_wav_file(file):
    #en progreso
    return wave.open(file, 'rb')


class Autrumn(tk.Tk):

    def __init__ (self):
        tk.Tk.__init__(self)
        self.title("Autrumn")

        # create a menubar
        menubar = Menu(self)
        self.config(menu=menubar)

        # create a menu
        autrumn_menu = Menu(menubar, tearoff=False)

        autrumn_menu.add_command(label='Analizador', command=lambda:self.show_frame(Analizador))
        # file_menu.add_command(label='Open...')
        autrumn_menu.add_command(label='Reproductor', command=lambda:self.show_frame(Reproductor))
        autrumn_menu.add_separator()

        # add a menu item to the menu
        autrumn_menu.add_command(
            label='Exit',
            command=self.destroy
        )

        # add the File menu to the menubar
        menubar.add_cascade(
            label="Menú",
            menu=autrumn_menu
        )


        self.geometry("700x1200")

        container = tk.Frame(self)

        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Analizador, Reproductor):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(Analizador)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    

# first window frame startpage
  
class Analizador(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        # label of frame Layout 2
        label = ttk.Label(self, text ="Analizador", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
         
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.fig.add_subplot(111).plot(frames)
        self.fig2 = Figure(figsize=(5, 3), dpi=100)
        self.fig2.add_subplot(111).plot()

        start_recording_button = ttk.Button(
            #controller,
            self,
            text='Start recording',
            compound=tk.LEFT,
            command=self.start_recording_thread
        )
        start_recording_button.grid(row = 1, column = 1, padx = 10, pady = 10)

        stop_recording_button = ttk.Button(
            self,
            text='Stop recording',
            compound=tk.LEFT,
            command=self.recordingAudio
        )
        stop_recording_button.grid(row = 2, column = 1, padx = 10, pady = 10)

        open_audio_button = ttk.Button(
            self,
            text='Open audio',
            compound=tk.LEFT,
            command=self.recordingAudio
        )
        open_audio_button.grid(row = 3, column = 1, padx = 10, pady = 10)


        frame1 = tk.Frame(controller)
        frame2 = tk.Frame(controller)

        self.canvas = FigureCanvasTkAgg(self.fig, controller)
        self.toolbar = NavigationToolbar2Tk(self.canvas, frame1)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, controller)
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, frame2)

        frame1.pack(side=tk.TOP, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.X)
        frame2.pack(side=tk.TOP, fill=tk.X)
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.X)



    def recordingAudio(self):
        global recording
        recording = False
        
    def startRecording(self):
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
                self.updatetimecanvas(np.hstack(frames))
                i=0

            i+=1

        numpyarrayfinal = np.hstack(frames)
        self.updatetimecanvas(numpyarrayfinal)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        self.to_atm(frames, WAVE_OUTPUT_FILENAME)





    def start_recording_thread(self):
        x = threading.Thread(target=self.startRecording)
        x.start()

    def updatetimecanvas(self, timeframe):
        self.fig.clear()
        self.fig.add_subplot(111).plot(timeframe)  # generate random x/y
        self.canvas.draw_idle()


# second window frame page1
class Reproductor(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Reproductor", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        btn_play = ttk.Button(self, text ="play",
                            command = lambda : print("play"))
        btn_play.grid(row = 1, column = 1, padx = 10, pady = 10)

        btn_pause = ttk.Button(self, text ="pause",
                            command = lambda : print("pause"))
        btn_pause.grid(row = 2, column = 1, padx = 10, pady = 10)

        btn_stop = ttk.Button(self, text ="stop",
                            command = lambda : print("stop"))
        btn_stop.grid(row = 3, column = 1, padx = 10, pady = 10)
  
    

# Driver Code
autrumn = Autrumn()
autrumn.mainloop()


  
  
class AudioPlayer:
    def __init__(self, wav):
        self.filename = "test"
        self.chunk = 1024
        self.paused = False
        self.stopped = False
        self.wave_file = wav
        self.p = 0
        self.stream = 0
    def load(self):
        #self.wave_file = wave.open(self.filename, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wave_file.getsampwidth()),
            channels=self.wave_file.getnchannels(),
            rate=self.wave_file.getframerate(),
            output=True
        )
    
    def play(self):
        data = self.wave_file.readframes(self.chunk)
        while data != b'' and not self.stopped:
            if not self.paused:
                self.stream.write(data)
                data = self.wave_file.readframes(self.chunk)
            else:
                time.sleep(0.1)
        self.stop()
    
    def pause(self):
        self.paused = True
    
    def resume(self):
        self.paused = False
    
    def stop(self):
        self.stopped = True
        self.paused = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.wave_file.close()
        



player = AudioPlayer(wavFile)

print("start")
player.load()
time.sleep(5)

print("play")
hilo = threading.Thread(target=player.play)
hilo.start()
print("pause")
time.sleep(5)
player.pause() 
print("resume")
time.sleep(5)
player.resume() 
print("stop")    
time.sleep(5)
player.stop()