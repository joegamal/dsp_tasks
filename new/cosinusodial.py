import math
import numpy as np
from matplotlib import pyplot as plt


def createCos(A,PhaseShift,AnalogFrequency, SamplingFrequency):

    if SamplingFrequency < AnalogFrequency * 2:
        return
    # Number of samples
    num_samples = SamplingFrequency

    # Generate the samples
    samples = []

    for n in range(num_samples):
        # formula: y = A * sin(2πf * n / Fs + Phase)
        y = A * math.cos(2 * math.pi * AnalogFrequency * n / SamplingFrequency + PhaseShift)
        samples.append(y)

    # Print first few samples
    for i in samples:
        print(i)

    x = np.arange(num_samples)
    y = np.array(samples)

    # Plot the signal
    plt.plot(x, y)
    plt.title(f"generate cosinusoidal signal")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()


#createCos(3,2.35619449019235,200,500)
