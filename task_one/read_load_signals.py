import numpy as np
#file format structure
# the file have four parts


#the first part is the signal type
#if 0 -> time domain x-axis
#if 1 -> frequency domain x-axis

#the second part is the is periodic or not
#if 0 -> not periodic
#if 1 -> periodic


#the third part is the number of data points rows that contains
#if the signal type is 0 so it will be the number of samples
#if the signal type is 1 so it will be the number of frequency components


# the fourth part is the data rows
# if the signal type is 0 -> time domain
# so the data will be [index sampleAmplitude]
#if the signal type is 1 -> frequency domain
# so the data will be [frequency amplitude phaseshift]


#read the file and store it in an array


#this function reads the signal and return the whole file in an array
def read_signal(filename):
    file_as_array = []
    with open(filename, 'r') as file:
        for line in file:
            file_as_array.append(line)
    return file_as_array

#this function takes the file name and return a numpy array x, y ready to work with
def get_signal_body(filename):
    data = np.loadtxt(filename,  skiprows=3)
    x = data[:, 0]
    y = data[:, 1]
    return x, y

#this function checks the domain type
def check_domain_type(signal):
    if signal[0] == 0:
        return "time"
    return "freq"

