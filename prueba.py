import numpy as np
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
