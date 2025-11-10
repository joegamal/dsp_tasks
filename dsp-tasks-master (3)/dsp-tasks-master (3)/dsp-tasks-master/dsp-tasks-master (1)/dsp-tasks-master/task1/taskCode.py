signal1File = "D:/dspTasks/task1/signals/Signal1.txt"
signal2File = "D:/dspTasks/task1/signals/Signal2.txt"
signal3File = "D:/dspTasks/task1/signals/signal3.txt"

def ReadSignalFile(file_name):
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    return expected_indices,expected_samples

signum = input("choose signal (1, 2, 3): ")

sig1indx,sig1samples = ReadSignalFile(signal1File)
sig2indx,sig2samples = ReadSignalFile(signal2File)
sig3indx,sig3samples = ReadSignalFile(signal3File)

signals = {
    "1": (sig1indx, sig1samples),
    "2": (sig2indx, sig2samples),
    "3": (sig3indx, sig3samples)
}

choice = input("1 for all data, 2 for every 20th sample: ")

import matplotlib.pyplot as plt

x, y = signals[signum]

if(choice=="1"):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    ax1.plot(x, y)
    ax1.set_title("Continuous Signal")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True)

    ax2.stem(x, y, linefmt='r-', markerfmt='ro')
    ax2.set_title("Discrete Signal")
    ax2.set_xlabel("Sample Index")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()


else:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    ax1.plot(x, y)
    ax1.set_title("Continuous Signal")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True)

    ax2.stem(x[::20], y[::20], linefmt='r-', markerfmt='ro')
    ax2.set_title("Discrete Signal (Downsampled)")
    ax2.set_xlabel("Sample Index")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()