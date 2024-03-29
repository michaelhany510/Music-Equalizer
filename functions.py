import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft
from scipy.io.wavfile import write
from scipy.signal import find_peaks
import wave
import librosa
import librosa.display
from scipy import signal
import soundfile as sf
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import altair as alt
import time
import os
import streamlit.components.v1 as components
from scipy.misc import electrocardiogram
import scipy

uniformModeRanges = [(20,2000),(2000,4000),(4000,6000),(6000,8000),(8000,10000),(10000,12000),(12000,14000),(14000,16000),(16000,18000),(18000,20000)]


parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "build")
_vertical_slider = components.declare_component("vertical_slider", path=build_dir)

def vertical_slider(label ,value, step, min=min, max=max, key=None):
    st.markdown(f"<h6 style='text-align: center; color: black; '>{label}</h6>", unsafe_allow_html=True)
    slider_value = _vertical_slider(value=value,step=step, min=min, max=max, key=key, default=value)
    return slider_value

# ---------------------------------------------------------------------- FOURIER TRANSFORM ON AUDIO -----------------------------------------------------------------------


def audio_fourier_transform(audio_file, guitar, flute, piano, spectroCheckBox):
    column1, column2 = st.columns(2)
    with column1:
        st.audio(audio_file, format='audio/wav')  # displaying the audio
    obj = wave.open(audio_file, 'rb')
    sample_rate = obj.getframerate()      # number of samples per second
    n_samples = obj.getnframes()        # total number of samples in the whole audio
    duration = n_samples / sample_rate  # duration of the audio file
    signal_wave = obj.readframes(-1)      # amplitude of the sound

    signal_y_axis = np.frombuffer(signal_wave, dtype=np.int32)
    signal_x_axis = np.linspace(0, duration, len(signal_y_axis))
    with column1:
        if spectroCheckBox:
            plot_spectro(audio_file.name)

    # returns complex numbers of the y axis in the data frame
    yf = rfft(signal_y_axis)
    # returns the frequency x axis after fourier transform
    xf = rfftfreq(len(signal_y_axis), (signal_x_axis[1]-signal_x_axis[0]))

    peaks = find_peaks(yf)   # computes peaks of the signal
    peaks_indeces = peaks[0]  # indeces of frequency with high peaks
    points_per_freq = len(xf) / (xf[-1])  # NOT UNDERSTANDABLE

    # with column1:
    #     plotting(xf,np.abs(yf))

    # these three lines determine the range that will be modified by the slider
    yf[:int(600*points_per_freq)] *= guitar
    yf[int(600*points_per_freq):int(3000*points_per_freq)] *= flute
    yf[int(3000*points_per_freq):] *= piano

    # returning the inverse transform after modifying it with sliders
    modified_signal = irfft(yf)
    tryyy = np.int32(modified_signal)

    write("example.wav", sample_rate, tryyy)
    with column2:
        st.audio("example.wav", format='audio/wav')

    if spectroCheckBox:
        with column2:
            plot_spectro('example.wav')
    else:
        dynamicPlotly(signal_x_axis,signal_y_axis,tryyy)


# ---------------------------------------------------------------------- UNIFORM FOURIER TRANSFORM ON AUDIO -----------------------------------------------------------------------


def uniform_audio_fourier_transform(audio_file, uniformModeSliders, spectroCheckBox):
    """
    Deletes or multiples a range of frequencies(20 Hz-20 kHz) from an audio file
    Arguments:
        audio_file: Audio file in .wav format
        comp1 - comp10: the factor multipler of every 2 kHz frequency band
        spectroCheckBox: if you want to view the signal as a spectogram
    """


    column1, column2 = st.columns(2)
    with column1:
        st.audio(audio_file, format='audio/wav')  # displaying the audio

    obj = wave.open(audio_file, 'rb')
    sample_rate = obj.getframerate()      # number of samples per second
    n_samples = obj.getnframes()        # total number of samples in the whole audio
    duration = n_samples / sample_rate  # duration of the audio file
    signal_wave = obj.readframes(-1)      # amplitude of the sound

    signal_y_axis = np.frombuffer(signal_wave, dtype=np.int32)
    signal_x_axis = np.linspace(0, duration, len(signal_y_axis))
    
    # returns complex numbers of the y axis in the data frame
    yf = rfft(signal_y_axis)

    # returns the frequency x axis after fourier transform
    xf = rfftfreq(len(signal_y_axis), (signal_x_axis[1]-signal_x_axis[0]))


    peaks = find_peaks(yf)   # computes peaks of the signal
    peaks_indeces = peaks[0]  # indeces of frequency with high peaks
    points_per_freq = len(xf) / (xf[-1])  

   

    # these 10 lines determine the range that will be modified by the slider
    i = 0
    for range in uniformModeRanges:
        yf[int(range[0]*points_per_freq):int(range[1]*points_per_freq)] *= uniformModeSliders[i]
        i += 1
        
    # returning the inverse transform after modifying it with sliders
    modified_signal = irfft(yf)
    y_normalized = np.int32(modified_signal)


    # writing the modified signal to a .wav file to play & view it
    write("example.wav", sample_rate, y_normalized)
    with column2:
        st.audio("example.wav", format='audio/wav')

    
    if not spectroCheckBox:
        dynamicPlotly(signal_x_axis,signal_y_axis,y_normalized)
    else:
        with column1:
            plot_spectro(audio_file.name)
        with column2:
            
            plot_spectro("example.wav")

#---------------------------------------------------------------------- VOWEL REMOVER/MODIFIER FUNCTION -------------------------------------------------------------------



def vowel_triang_window(y, start, end, val, ppf):
    target = y[int(start*ppf):int(end*ppf)]
    if val == 0:
        window = -(signal.windows.triang(len(target))-1)
    elif val == 1:
        return target
    else:
        window = val * signal.windows.triang(len(target))

    return [target[i]*window[i] for i in range(len(window))]



def vowel_audio_fourier_transform(file, ʃ_slider, ʊ_slider, a_slider, r_slider, b_slider, spectroCheckBox):
    column1, column2 = st.columns(2)
    with column1:
        st.audio(file, format='audio/wav')
    tone, sample_rate = sf.read(file)  # number of samples per second
    n_samples = tone.shape[0]   # total number of samples in the whole audio
    duration = n_samples / sample_rate  # duration of the audio file
    signal_y_axis = tone
    signal_x_axis = np.linspace(0, duration, len(signal_y_axis))
    with column1:
        if spectroCheckBox:
            plot_spectro(file.name)
    
    yf = rfft(signal_y_axis)
    xf = rfftfreq(len(signal_y_axis), 1/sample_rate)

    points_per_freq = len(xf) / (sample_rate/2)


    yf[int(800*points_per_freq):int(5000*points_per_freq)]*=ʃ_slider
    yf[int(500*points_per_freq):int(2000*points_per_freq)]*=ʊ_slider
    yf[int(500*points_per_freq):int(1200*points_per_freq)]*=a_slider
    yf[int(900*points_per_freq):int(5000*points_per_freq)]*=r_slider
    yf[int(1200*points_per_freq):int(5000*points_per_freq)]*=b_slider

    


    modified_signal = irfft(yf)

    sf.write("vowel_modified.wav", modified_signal, sample_rate)
    with column2:
        st.audio("vowel_modified.wav", format='audio/wav')

    if spectroCheckBox:
        with column2:
            plot_spectro('vowel_modified.wav')
    else:
        dynamicPlotly(signal_x_axis,signal_y_axis,modified_signal)

#-------------------------------------------------------------------------- PITCH MODIFIER FUNCTION ---------------------------------------------------------------------------------------


def pitch_modifier(audio_file, semitone, spectroCheckBox):
    """
    Modifies the pitch of a given audio file
    Arguments:
        audio_file: Audio file in .wav format
        semitone: half a tone higher or lower
        spectroCheckBox: if you want to view the signal as a spectogram
    """
    fr = 20
    column1, column2 = st.columns(2)
    with column1:
        st.audio(audio_file, format='audio/wav')  # displaying the audio
    obj = wave.open(audio_file, 'rb')
    sample_rate = obj.getframerate()      # number of samples per second
    n_samples = obj.getnframes()        # total number of samples in the whole audio
    duration = n_samples / sample_rate  # duration of the audio file
    signal_wave = obj.readframes(-1)      # amplitude of the sound


    signal_y_axis = np.frombuffer(signal_wave, dtype=np.int32)
    signal_x_axis = np.linspace(0, duration, len(signal_y_axis))

    with column1:
        if spectroCheckBox:
            plot_spectro(audio_file.name)

    y_shifted = librosa.effects.pitch_shift(signal_y_axis.astype(
        float), sample_rate, n_steps=semitone)  # shifting the audio according to the semitone given

    # reconstructing the proccessed signal
    sf.write(file='example.wav', samplerate=sample_rate, data=y_shifted)

    y_normalized = np.int32(y_shifted)

    # TODO remove after playing with buttons
    with column2:
        st.audio("example.wav", format='audio/wav')

    # play/pause with plotly
    dynamicPlotly(signal_x_axis,signal_y_axis,y_normalized)
   

def arrhythima():
    col1, col2, col3 = st.columns([.2, .7, .1])
    ecg = electrocardiogram()

    fs = 360
    time = np.arange(ecg.size) / fs

    fourier_x_axis = scipy.fft.rfftfreq(len(ecg), (time[1]-time[0]))
    fourier_y_axis = scipy.fft.rfft(ecg)

    points_per_freq = len(fourier_x_axis) / (fourier_x_axis[-1])

    value = st.slider(label="Arrhythmia", min_value=0,
                      max_value=10, value=1, key=12)

    fourier_y_axis[int(points_per_freq):int(points_per_freq*5)] *= value

    modified_signal = scipy.fft.irfft(fourier_y_axis)

    fig, axs = plt.subplots()
    fig.set_size_inches(14, 5)

    plt.plot(time, (modified_signal), color='#3182ce')
    plt.xlabel("Time in s")
    plt.ylabel("ECG in mV")
    plt.xlim(45, 51)

    col2.plotly_chart(fig)



############################################################################ PLOTTING FUNCTIONS ######################################################################################

def dynamicPlotly(signalX,signalYBefore,signalYAfter):
    with st.sidebar:
        c1,c2 = st.columns(2)
        with c1:
            playButton = st.button('play')
        with c2:
            pauseButton = st.button('pause')
        
    
    placeHolder = st.empty()
    if not st.session_state['played']:
        with placeHolder.container():
            plotting(signalX,signalYBefore,signalX, signalYAfter)
    
    
    if playButton:
        while True:
            st.session_state['played'] = True
            for i in range(st.session_state['stopPoint'],len(signalX),4):
                st.session_state['stopPoint'] = i
                mn = max(0,i-(len(signalX)//300))
                st.session_state['startPoint'] = mn
                with placeHolder.container(): 
                    plotting(signalX[mn:i],signalYBefore[mn:i],signalX[mn:i], signalYAfter[mn:i])
                time.sleep(0.00001)
            st.session_state['stopPoint'] = 0
    stop = st.session_state['stopPoint']
    start = st.session_state['startPoint']
    if st.session_state['played']:
        with placeHolder.container():
            plotting(signalX[start:stop],signalYBefore[start:stop],signalX[start:stop], signalYAfter[start:stop])


def plotting(x1, y1, x2, y2):
   
    figure = make_subplots(rows=2, cols=2, shared_yaxes=True)

    figure.add_trace(go.Scatter(y=y1, x=x1, mode="lines",
                     name="Signal"), row=1, col=1)

    figure.add_trace(go.Scatter(y=y2, x=x2, mode="lines",
                     name="transformed"), row=1, col=2)

    figure.update_xaxes(matches='x')
    figure.update_layout(autosize=False,
    width=500,
    height=700,
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=4))
    st.plotly_chart(figure, use_container_width=True)



def plot_spectro(audio_file):

    y, sr = librosa.load(audio_file)
    D = librosa.stft(y)  # STFT of y
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    fig, ax = plt.subplots()
    img = librosa.display.specshow(S_db, x_axis='time', y_axis='linear', ax=ax)
    ax.set(title='')
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    st.pyplot(fig)


