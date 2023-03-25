# main layout for multiple pages
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/

# menu
# https://www.pythontutorial.net/tkinter/tkinter-menu/
# https://www.tutorialsteacher.com/python/create-gui-using-tkinter-python

from io import BytesIO
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
from scipy.fft import rfft
 
LARGEFONT =("Verdana", 15)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"
PLAY_RANGE = 5


frames = []
recording = False
wavFile= []
fourier_frames = []
vec_fourier_frames = []
external_wav_path = ""


    #---ARCHIVOS_ATM-----

   #---ARCHIVOS_ATM-----

def to_atm(chunksList, wavFilePath):
  
    file = open("chunks", "wb")
    content = array_to_bytes(chunksList)
    file.write(content)
    file.close
    global frames
    with ZipFile('file.atm', 'w') as zip:
         zip.write('chunks')
         zip.write(wavFilePath)
         print(chunksList)
    try:
        os.remove("chunks")
    except:
        print("File already deleted")

def from_atm(filepath):
    with ZipFile(filepath) as zip:
        files = zip.namelist()
        for i in range(0,len(files)):
            if(".wav" in files[i]):
                global wavFile
                zip.extract(files[i])
                wavFile = open_wav_file(files[i])
            elif(files[i] == "chunks"):
                global frames
                frames = bytes_to_array(zip.read(files[i]))
                
                print(type(frames))
                print(frames)
               
def array_to_bytes(x):
    np_bytes = BytesIO()
    np.save(np_bytes, x, allow_pickle=True)
    return np_bytes.getvalue()


def bytes_to_array(b):
    np_bytes = BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)
            

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
        container.grid(row = 1, column = 1, padx = 10, pady = 10)
        

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
        
        top_frame = tk.Frame(self, width=200, height=400, bg='grey')
        label = ttk.Label(top_frame, text ="Analizador", font = LARGEFONT)
        top_frame.grid(row=0, column=0, padx=10, pady=5)
        label.grid(row = 0, column = 0, padx = 10, pady = 10)
         
        self.fig = Figure(figsize=(5, 1), dpi=100)
        self.fig.add_subplot(111).plot(frames)
        self.fig2 = Figure(figsize=(5, 3), dpi=100)
        self.fig2.add_subplot(111).hist(fourier_frames, bins=100)
        self.ax= 0
        self.entry = ttk.Entry(top_frame)
        self.entry.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.btn_load = ttk.Button(top_frame, text ="Load",
                            command = self.start_loading_thread )
        self.btn_load.grid(row = 1, column = 1, padx = 10, pady = 10)

        start_recording_button = ttk.Button(
            #controller,
            top_frame,
            text='Start recording',
            compound=tk.LEFT,
            command=self.start_recording_thread
        )
        start_recording_button.grid(row = 0, column = 2, padx = 10, pady = 10)

        stop_recording_button = ttk.Button(
            top_frame,
            text='Stop recording',
            compound=tk.LEFT,
            command=self.recordingAudio
        )
        stop_recording_button.grid(row = 0, column = 3, padx = 10, pady = 10)

        open_audio_button = ttk.Button(
            top_frame,
            text='Open audio',
            compound=tk.LEFT,
            command=self.recordingAudio
        )
        open_audio_button.grid(row = 0, column = 4, padx = 10, pady = 10)


        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame1)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, self)
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.frame2)


        self.frame1.grid(row = 4, column = 0, padx = 10, pady = 10)
        self.canvas.get_tk_widget().grid(row = 5, column = 0, padx = 10, pady = 10)
        self.frame2.grid(row = 6, column = 0, padx = 10, pady = 10)
        self.canvas2.get_tk_widget().grid(row = 7, column = 0, padx = 10, pady = 10)

    def load_wav(self):
        chunk = 1024  
        f = wave.open(self.entry.get(), 'rb')
        global external_wav_path
        external_wav_path = self.entry.get()
        p = pyaudio.PyAudio()
        global frames
        frames=[]
        global vec_fourier_frames
        vec_fourier_frames = []
        #Abre stream de pyaudio
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output = True)  
        #Lee los chunks del wav y los almacena en data
        data = f.readframes(chunk)  
        i=0
        #Abre un ciclo para cada elemento en data
        while data:  
            stream.write(data)  


            numpydata = np.frombuffer(data, dtype=np.int16)
            frames.append(numpydata)
            # Calcular transformada de Fourier
            fft_data = np.fft.fft(numpydata)
            freqs = np.fft.fftfreq(len(numpydata), d=1/f.getframerate())
            
            fourier_frames.append(fft_data)  #datos  de la transformada
            vec_fourier_frames.append(freqs)  #datos de frecuencia de la transformada

            
            #calcula si han pasado RECORD_SECONDS segundos antes de graficar de nuevo
            #formula recuperada de https://stackoverflow.com/questions/35344649/reading-input-sound-signal-using-python

            if (i >= int(f.getframerate() / chunk * 1)):
                self.updatetimecanvas(np.hstack(frames)) #llama a actualizar el canvas

                self.updatefouriercanvas(fft_data,freqs)

                i = 0

            i += 1
            data = f.readframes(chunk)


        numpyarrayfinal = np.hstack(frames)
        self.updatetimecanvas(numpyarrayfinal)
        #cierra el stream de datos
        stream.stop_stream()  
        stream.close()  

        #cierra pyaudio
        p.terminate()

        #guarda un wav como output.wav
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(f.getnchannels())
        wf.setsampwidth(p.get_sample_size(p.get_format_from_width(f.getsampwidth())))
        wf.setframerate(f.getframerate())
        wf.writeframes(b''.join(frames))
        wf.close()
        ##print(frames)
        #to_atm(frames, ( WAVE_OUTPUT_FILENAME if external_wav_path == "" else external_wav_path))


    def recordingAudio(self):
        global recording
        recording = False
        
    def startRecording(self):
        global recording
        p = pyaudio.PyAudio()
        # abre el stream de pyAudio
        # Channels abre para surround o mono, este proyecto se hace con mono
        # Rate da el samplerate del canal
        # input abre el micrófono
        # frames per buffer muestre cuántos frames se graban a la vez.
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

        #Ciclo continúa hasta que a nivel global se indique que ya no está grabando
        while(recording):
            data = stream.read(CHUNK)
            numpydata = np.frombuffer(data, dtype=np.int16)
            frames.append(numpydata)
            
            # Calcular transformada de Fourier
            fft_data = np.fft.fft(numpydata)
            freqs = np.fft.fftfreq(len(numpydata), d=1/RATE)
            
            fourier_frames.append(fft_data)  #datos  de la transformada
            vec_fourier_frames.append(freqs)  #datos de frecuencia de la transformada

            #Cada ciertos segundos RECORD_SECONDS se entra al ciclo para actualizar el gráfico
            #En este caso se escogen 2 segundos
            #como esto es por ciclo, este se calcula con la formula Rate/chunk * 2
            # Este número se compara con el número de iteraciones que debe tener en i
            if(i>=int(RATE / CHUNK * RECORD_SECONDS)):
                self.updatetimecanvas(np.hstack(frames)) #hstack vuelve el array de frames unidimensional
                self.updatefouriercanvas(fft_data,freqs)
                i=0

            i+=1

        numpyarrayfinal = np.hstack(frames)
        self.updatetimecanvas(numpyarrayfinal) #última actualización

        #Cierra el input de datos del micrófono
        stream.stop_stream()
        stream.close()
        p.terminate()

        #crea un wav con el ncon el nombre output.wav
        #toda la información se guarda en
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        to_atm(frames, WAVE_OUTPUT_FILENAME)





    def start_recording_thread(self):
        x = threading.Thread(target=self.startRecording)
        x.start()

    def start_loading_thread(self):
        x = threading.Thread(target=self.load_wav)
        x.start()


    def updatetimecanvas(self, timeframe):
        self.fig.clear()
        self.fig.add_subplot(111).plot(timeframe)  # Refrezca el plot con los frames actuales
        self.canvas.draw_idle()

    def updatefouriercanvas(self,fft_data,freqs):
        
        self.fig2.clear()
        
        self.ax = self.fig2.add_subplot(111)
        self.ax.hist(freqs, bins=100, weights=np.abs(fft_data))
        
        
        self.ax.set_xlabel('Frecuencia (Hz)')
        self.ax.set_ylabel('Conteo') #cantidad de veces que aparece cada frecuencia en el espectro de Fourier
        self.ax.set_xlim(-8000, 8000) # establecer los límites de la dimensión x
        self.ax.set_ylim(0, 50000) # establecer los límites de la dimensión y
        self.canvas2.draw_idle()
    
    
class AudioPlayer:
    def __init__(self, wav,figtime, figfreq, canvasTime,canvasFreq):
        self.filename = "test"
        self.chunk = 1024
        self.paused = False
        self.stopped = False
        self.wave_file = wav
        self.p = 0
        self.stream = 0
        self.timer = 0
        self.fig =figtime
        self.fig2 = figfreq
        self.canvas = canvasTime
        self.canvas2 = canvasFreq

    def updatetimecanvas(self, timeframe):


        self.fig.clear() #limpia el gráfico actual
        self.fig.add_subplot(111).plot(timeframe)  # Genera un plot con los valores especificado
        self.canvas.draw_idle()
        
    def updatefouriercanvas(self,fft_data,freqs):
        self.fig2.clear()
        
        self.ax = self.fig2.add_subplot(111)
        self.ax.hist(freqs, bins=100, weights=np.abs(fft_data))
        
        
        self.ax.set_xlabel('Frecuencia (Hz)')
        self.ax.set_ylabel('Conteo') #cantidad de veces que aparece cada frecuencia en el espectro de Fourier
        self.ax.set_xlim(-8000, 8000) # establecer los límites de la dimensión x
        self.ax.set_ylim(0, 100000) # establecer los límites de la dimensión y
        self.canvas2.draw_idle()
    
    
    def check_realtime(self, multiplier):
        global frames
        global fourier_frames
        global vec_fourier_frames
        
        # Calcular transformada de Fourier
        fourier_frames = np.fft.fft(frames)
        vec_fourier_frames = np.fft.fftfreq(len(frames), d=1/RATE)
        
        print("fourier-> ", fourier_frames[0])
        print("vec-> ", fourier_frames[1])
        
        fourier_frames = fourier_frames[:, 0]
        
        print("fourier-> ", fourier_frames.shape)
        print("vec-> ", vec_fourier_frames.shape)
        
        #se busca que no grafique más allá del total de frames
        # si el próximo rango de graficación excede el largo del frame, utiliza el largo del frame como límite superior
        # Para encontrar una medición exacta de los 5 segundos a lo largo de frames, se calculó que hay 43 frames por segundo
        # Estos 43 se multiplica por un PLAY_RANGE que sería de 5 para 5 segundos
        # Para encontrar el punto actual se multiplica por el multiplicador actual para buscar el frame 10, 15, etc
        # Para el límite superior, se le suma 1 al multiplicador para que de el siguiente punto
        if (43 * (multiplier + 1) * PLAY_RANGE <= len(frames)):
            self.updatetimecanvas(np.hstack(frames[43*multiplier*PLAY_RANGE:43 * (multiplier + 1) * PLAY_RANGE]))
            self.updatefouriercanvas(fourier_frames[43*multiplier*PLAY_RANGE:43 * (multiplier + 1) * PLAY_RANGE],vec_fourier_frames[43*multiplier*PLAY_RANGE:43 * (multiplier + 1) * PLAY_RANGE])
            
            
            
        else:
            self.updatetimecanvas(np.hstack(frames[43 * multiplier * PLAY_RANGE:len(frames)-1]))
            self.updatefouriercanvas(fourier_frames[43 * multiplier * PLAY_RANGE:len(frames)-1],vec_fourier_frames[43 * multiplier * PLAY_RANGE:len(frames)-1])
            
            
            
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
        global frames
        print(frames)

        multiplier = 0
        self.check_realtime(multiplier)
        multiplier +=1
        while data != b'' and not self.stopped:
            if not self.paused:
                start_time = time.time()
                self.stream.write(data)
                data = self.wave_file.readframes(self.chunk)
                end_time = time.time()
                self.timer += end_time - start_time

                ## Función de tiempo
                if self.timer >= multiplier*PLAY_RANGE: #si el tiempo ya es mayor que el multiplicador por el rango de segundos
                    self.check_realtime(multiplier)
                    multiplier += 1 #aumentar el multiplicador en 1.




            else:
                time.sleep(0.1)
        self.stop()
    
    def pause(self):
        self.paused = True
        print(self.timer)
    
    def resume(self):
        self.paused = False
    
    def stop(self):
        self.stopped = True
        self.paused = False
        self.stream.stop_stream()
        #self.stream.close()
        #self.p.terminate()
        #self.wave_file.close()
        pass

# second window frame page1
class Reproductor(tk.Frame):
    player = AudioPlayer(wavFile,0,0,0,0)
    playing = False
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        self.label = ttk.Label(self, text ="Reproductor", font = LARGEFONT)
        top_frame = tk.Frame(self, width=200, height=400, bg='grey')
        top_frame.grid(row=0, column=0, padx=10, pady=5)
        self.label = ttk.Label(top_frame, text ="Reproductor", font = LARGEFONT)
        self.label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.btn_load = ttk.Button(top_frame, text ="Load",
                            command = lambda : self.create_player() )
        self.btn_load.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.entry = ttk.Entry(top_frame)
        self.entry.grid(row = 0, column = 1, padx = 10, pady = 10)
  
        self.btn_play = ttk.Button(top_frame, text ="play",
                            command = lambda : self.play())
        self.btn_play.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.btn_pause = ttk.Button(top_frame, text ="pause",
                            command = lambda : self.pause())
        self.btn_pause.grid(row = 0, column = 3, padx = 10, pady = 10)

        self.btn_stop = ttk.Button(top_frame, text ="stop",
                            command = lambda : self.stop())
        self.btn_stop.grid(row = 0, column = 4, padx = 10, pady = 10)


        self.fig = Figure(figsize=(5, 1), dpi=100)
        self.fig.add_subplot(111).plot(frames)
        self.fig2 = Figure(figsize=(5, 3), dpi=100)
        self.fig2.add_subplot(111).hist(vec_fourier_frames, bins=100, weights=np.abs(fourier_frames))



        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame1)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, self)
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.frame2)


        self.frame1.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.canvas.get_tk_widget().grid(row = 2, column = 0, padx = 10, pady = 10)
        self.frame2.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.canvas2.get_tk_widget().grid(row = 4, column = 0, padx = 10, pady = 10)

        # Posicionarla en la ventana.
        # self.entry.place(x=50, y=50)
    
    def create_player(self):
        path = ""
        from_atm(self.entry.get())
        global wavFile
        self.player = AudioPlayer(wavFile, self.fig, self.fig2, self.canvas, self.canvas2)
        self.player.load()

    def play(self):
        hilo = threading.Thread(target=self.player.play)
        hilo.start()

    def pause(self):
        if self.player.paused == False:
            self.player.pause()
        else:
            self.player.resume() 
    
    def stop(self):
        self.player.stop()
        
    

# Driver Code
autrumn = Autrumn()
autrumn.mainloop()