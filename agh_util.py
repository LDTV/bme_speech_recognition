import re
import scipy.io.wavfile
import scipy.signal as sig
import numpy as np
from math import floor, ceil

# Returns python list of lists in format [beginning_time(int), end_time(int), word(string)]
def parse_timestamps(filename):

    timestamps_file = open(filename)
    list_of_words = timestamps_file.readlines()
    timestamps = list()
    for i in list_of_words:
        t = re.split('\s+', i)
        timestamps.append([float(t[0].replace(',', '.')), float(t[1].replace(',', '.')), t[2]])
    timestamps_file.close()
    return timestamps

# returns signal (THE LEFT SIGNAL CHANNEL IF STEREO) and sampling frequency
def get_signal_from_file(filename):
    fs, signal = scipy.io.wavfile.read(filename)
    if signal.ndim>1:
        signal = signal[:,0]
    return signal, fs

# Get an envelope
# Originally developed by C. Jarne from University of Quilmes (UNQ), cecilia.jarne@unq.edu.ar
# https://pdfs.semanticscholar.org/401b/10f76b1a9b668a5df0a829873aaf356ac27f.pdf
# Major function rework and improvement by Jacek Fidos, AGH UST, jacekffid@os.pl

def get_envelope(input_signal, interval_length = 100, f_s = 44100, f_cut = 300):

    # Taking the absolute value
    absolute_signal = abs(input_signal)

    # Peak detection
    output_signal = [absolute_signal[0]]

    signal_len = len(absolute_signal)
    samples_behind = floor(interval_length/2)
    samples_ahead = ceil(interval_length/2)

    for base_index in range (1, samples_behind):
        output_signal.append(np.amax(absolute_signal[0:base_index]))

    for base_index in range (samples_behind, signal_len - samples_ahead):
        output_signal.append(np.amax(absolute_signal[base_index - samples_behind : base_index + samples_ahead]))

    for base_index in range (signal_len - samples_ahead, signal_len):
        output_signal.append(np.amax(absolute_signal[base_index: len(absolute_signal)]))

    W1 = float(f_cut)/f_s #filter parameter Cut frequency over the sample frequency
    (b, a) = sig.butter(4, W1, btype='lowpass')
    output_signal = sig.filtfilt(b, a, output_signal)

    return output_signal

# Cutting silence from both sides of the signal, based on envelope level.
def cut_silence(input_signal, silence_level = 0.01, envelope = None):
    word_beginning = np.argmax(envelope>(np.amax(envelope)*silence_level))
    word_end = len(envelope) - np.argmax(envelope[::-1]>(np.amax(envelope)*silence_level)) - 1
    ret_signal = input_signal[word_beginning: word_end]
    return ret_signal
