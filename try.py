import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft
import streamlit as st
import plotly.graph_objects as go
from scipy.signal import find_peaks
import pandas as pd
# SAMPLE_RATE = 44100  # Hertz
# DURATION = 5  # Seconds
# fig = go.Figure()

# # uploaded_file = st.file_uploader(label="Uploading Signal", type = ['csv',".wav"])

# def generate_sine_wave(freq, sample_rate, duration):
#     x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
#     frequencies = x * freq
#     # 2pi because np.sin takes radians
#     y = np.sin((2 * np.pi) * frequencies)
#     return x, y

# def FT(signal,Fs,duration):

#     DURATION = duration
#     SAMPLE_RATE = int(Fs)
#     mixed_tone = signal
#     normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

#     plt.plot(normalized_tone[:1000])
#     plt.show()

#     # Remember SAMPLE_RATE = 44100 Hz is our playback rate
#     write("myUploadedSignal.wav", SAMPLE_RATE, normalized_tone)


#     # Number of samples in normalized_tone
#     N = int(SAMPLE_RATE * DURATION)

#     yf = rfft(normalized_tone)
#     xf = rfftfreq(N, 1 / SAMPLE_RATE)
#     print(xf)

#     plt.plot(xf, np.abs(yf))
#     plt.show()

#     # The maximum frequency is half the sample rate
#     points_per_freq = len(xf) / (SAMPLE_RATE / 2)

#     # Our target frequency is 4000 Hz
#     target_idx = int(points_per_freq * 10)
#     target_idx_2 = int(points_per_freq * 4000)
#     yf[target_idx - 1 : target_idx_2 + 2] = 0

#     plt.plot(xf, np.abs(yf))
#     plt.show()


#     new_sig = irfft(yf)

#     plt.plot(new_sig[:1000])
#     plt.show()

#     norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))

#     write("cleanUploaded04.wav", SAMPLE_RATE, norm_new_sig)

# from scipy.io.wavfile import read,write
# from IPython.display import Audio

# Fs, data = read('mixkit-retro-game-emergency-alarm-1000.wav')
# data = data[:,0]
# duration = data.shape[0]/Fs
# FT(data,Fs,duration)
# print('Sampling Frequency is', Fs)
# import scipy
# def getPeaksFrequencies(xAxis,yAxis):
    
#     amplitude = np.abs(scipy.fft.rfft(yAxis))
#     frequency = scipy.fft.rfftfreq(len(xAxis), (xAxis[1]-xAxis[0]))
#     indices = find_peaks(amplitude)
#     return frequency[indices[0]]

    

# def trial_fourier(dataframe,Fs,duration):

    
#     DURATION = duration
#     SAMPLE_RATE = int(Fs)

#     signal_y_axis = (dataframe.iloc[:,1]).to_numpy()
#     signal_x_axis = (dataframe.iloc[:,0]).to_numpy()


#     normalized_signal_y_axis = np.int16((signal_y_axis / signal_y_axis.max()) * 32767)

#     plt.plot(normalized_signal_y_axis[:1000])
#     plt.show()

#     # Remember SAMPLE_RATE = 44100 Hz is our playback rate
#     write("michael.wav", SAMPLE_RATE, normalized_signal_y_axis)

#     # Number of samples in normalized_signal_y_axis
#     number_of_samples = int(SAMPLE_RATE * DURATION)

#     yf = rfft(normalized_signal_y_axis)

#     xf = rfftfreq(number_of_samples, 1 / SAMPLE_RATE)
#     # peaks = find_peaks(yf, height=1)
#     # peaks_indeces = peaks[0]
#     # peaks_height = peaks[1]

#     # st.write(peaks_height["peak_heights"])

#     # peaks_psotion = signal_y_axis[peaks_indeces]
    
#     peaksPositions = np.round(getPeaksFrequencies(signal_x_axis,signal_y_axis),1)
    
#     print(peaksPositions)
    
#     points_per_freq = len(xf) / (SAMPLE_RATE / 2)
    
#     fig, axs = plt.subplots()
#     fig.set_size_inches(14,5)
#     plt.plot(xf, np.abs(yf))
#     plt.show()

#     target_idx = int(points_per_freq * (peaksPositions[0]-1))
#     target_idx_2 = int(points_per_freq * peaksPositions[0]+1)
#     yf[target_idx - 1 : target_idx_2 + 2] = 0

#     plt.plot(xf,np.abs(yf))
#     plt.show()


#     new_sig = irfft(yf)

#     # one_argument_plotting(new_sig[:1000])
#     plt.plot(new_sig[:1000])
#     plt.show()

#     norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))

#     write("cleanUploaded04.wav", SAMPLE_RATE, norm_new_sig)

#     norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))

#     write("cleanUploaded04.wav", SAMPLE_RATE, norm_new_sig)

#     plt.plot(xf, np.abs(yf))
#     # plt.scatter(peaks_indeces,peaks_hight, color='black' , marker="o" ,linestyle="")
#     st.plotly_chart(fig,use_container_width=True)
    
    
# df = pd.read_csv('Signal 6.csv')
# df = pd.DataFrame(df)
# trial_fourier(df,2000,1)


import numpy as np
import matplotlib.pyplot as plt
# import streamlit as st

SAMPLE_RATE = 44100  # Hertz
DURATION = 5  # Seconds

def generate_sine_wave(freq, sample_rate=SAMPLE_RATE, duration=DURATION):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

# Generate a 2 hertz sine wave that lasts for 5 seconds
x, y = generate_sine_wave(2, SAMPLE_RATE, DURATION)
plt.plot(x, y)
plt.show()

_, nice_tone = generate_sine_wave(400)
_,nice_tone_2 = generate_sine_wave(600)
_,nice_tone_3 = generate_sine_wave(800)
_, noise_tone = generate_sine_wave(4000)
noise_tone = noise_tone * 0.3

mixed_tone = nice_tone+nice_tone_2+nice_tone_3 + noise_tone

normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

plt.plot(normalized_tone[:1000])
plt.show()
from scipy.io.wavfile import write

# Remember SAMPLE_RATE = 44100 Hz is our playback rate
write("mysinewave.wav", SAMPLE_RATE, normalized_tone)

from scipy.fft import rfft, rfftfreq

# Number of samples in normalized_tone
N = SAMPLE_RATE * DURATION

yf = rfft(normalized_tone)
xf = rfftfreq(N, 1 / SAMPLE_RATE)
print(xf)

plt.plot(xf, np.abs(yf))
plt.show()

# The maximum frequency is half the sample rate
points_per_freq = len(xf) / (SAMPLE_RATE / 2)

# Our target frequency is 4000 Hz
target_idx = int(points_per_freq * 4000)
yf[target_idx - 1 : target_idx + 2] = 0

plt.plot(xf, np.abs(yf))
plt.show()

from scipy.fft import irfft

new_sig = irfft(yf)

plt.plot(new_sig[:1000])
plt.show()

norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))

write("clean.wav", SAMPLE_RATE, norm_new_sig)



