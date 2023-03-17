'''import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Crear una señal de prueba
t = np.linspace(0, 1, 1000, endpoint=False)
y = np.sin(2 * np.pi * 5 * t) + np.sin(2 * np.pi * 10 * t)

# Realizar la transformada de Fourier
y_fft = fft(y)
freq = fftfreq(len(y), t[1]-t[0])

# Graficar la señal y su transformada de Fourier
fig, axs = plt.subplots(2, 1, figsize=(8, 6))
axs[0].plot(t, y)
axs[0].set_xlabel('Tiempo (s)')
axs[0].set_ylabel('Amplitud')
axs[1].plot(freq, np.abs(y_fft))
axs[1].set_xlim(0, 15)
axs[1].set_xlabel('Frecuencia (Hz)')
axs[1].set_ylabel('Amplitud')
plt.show()


======================================================

from scipy.fft import fft, fftfreq, fftshift
import numpy as np
# number of signal points
N = 400
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.exp(50.0 * 1.j * 2.0*np.pi*x) + 0.5*np.exp(-80.0 * 1.j * 2.0*np.pi*x)
yf = fft(y)
xf = fftfreq(N, T)
xf = fftshift(xf)
yplot = fftshift(yf)
import matplotlib.pyplot as plt
plt.plot(xf, 1.0/N * np.abs(yplot))
plt.grid()
plt.show() '''

from scipy.io import wavfile
from scipy.fft import fft
import numpy as np
import matplotlib.pyplot as plt

N = 400
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.exp(50.0 * 1.j * 2.0*np.pi*x) + 0.5*np.exp(-80.0 * 1.j * 2.0*np.pi*x)
# Calcular la transformada de Fourier
fft_data = fft(y)

# Calcular la magnitud de la transformada de Fourier y normalizarla
fft_mag = np.abs(fft_data)
fft_mag = fft_mag / np.max(fft_mag)

# Crear un histograma de la magnitud de la transformada de Fourier
plt.hist(fft_mag, bins=100)
plt.xlabel("Magnitud")
plt.ylabel("Número de ocurrencias")
plt.show()
