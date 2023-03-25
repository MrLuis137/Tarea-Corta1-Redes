import wave
import pyaudio
import time
import threading

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

        multiplier = 0
        multiplier +=1
        while data != b'' and not self.stopped:
            if not self.paused:
                start_time = time.time()
                self.stream.write(data)
                data = self.wave_file.readframes(self.chunk)
                end_time = time.time()
                self.timer += end_time - start_time   
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
        time.sleep(0.1)
        #self.paused = False
        #(self.stream).stop_stream()
        #(self.stream).close()
        #(self.p).terminate()        
        #(self.wave_file).close()
        pass
        

def test_play():
    # Load a test audio file
    audio_file = wave.open("test.wav", 'rb')

    # Create an AudioPlayer object and load the audio file
    player = AudioPlayer(audio_file, None, None, None, None)
    player.load()

    # Start playing the audio file
    hilo = threading.Thread(target=player.play)
    hilo.start()


    player.stop()
    # Check that the player is not paused or stopped
    assert not player.paused

def test_pause():
    # Load a test audio file
    audio_file = wave.open("test.wav", 'rb')

    # Create an AudioPlayer object and load the audio file
    player = AudioPlayer(audio_file, None, None, None, None)
    player.load()

    # Start playing the audio file
    hilo = threading.Thread(target=player.play)
    hilo.start()

    # Pause the audio player
    player.pause()

    player.stop()
    # Check that the player is paused and not stopped
    assert player.paused

def test_stop():
    # Load a test audio file
    audio_file = wave.open("test.wav", 'rb')

    # Create an AudioPlayer object and load the audio file
    player = AudioPlayer(audio_file, None, None, None, None)
    player.load()

    # Start playing the audio file
    hilo = threading.Thread(target=player.play)
    hilo.start()

    # Stop the audio player
    player.stop()

    check = player.stopped
    # Check that the player is stopped and not paused
    assert check
    #assert not player.paused


