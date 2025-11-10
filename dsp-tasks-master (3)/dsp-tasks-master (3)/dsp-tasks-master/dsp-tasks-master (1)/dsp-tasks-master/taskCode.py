from typing import Dict, Any

signal1File = "D:/dspTasks/task1/signals/Signal1.txt"
signal2File = "D:/dspTasks/task1/signals/Signal2.txt"
signal3File = "D:/dspTasks/task1/signals/signal3.txt"

import Task1Test as t

sig1indx,sig1samples = t.ReadSignalFile(signal1File)
sig2indx,sig2samples = t.ReadSignalFile(signal2File)
sig3indx,sig3samples = t.ReadSignalFile(signal3File)
samples={1:[signal1File,sig1samples,sig1indx],
         2:[signal2File,sig2samples,sig2indx],
         3:[signal3File,sig3samples,sig3indx]}
all_results:dict[str,list]={}


while(True):
    signum = int(input("choose signal (1, 2, 3): "))
    choice = int(input("menu:\n 1.for graph\n 2.for signals available\n 3.for arithmatic maths\n 0.to exit\n"))
    z, y, x = samples[signum]
    if choice == 1:
        downSample = input("1 for all data, 2 for every 20th sample: ")
        import matplotlib.pyplot as plt
        if (downSample == "1"):
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
    elif choice == 2:
        pass
    elif choice == 3:
        ch = int(input("1.for addition \n 2.for multiplication \n"))
        if ch == 1:
            print("which signal do you want ?")
            print("first choice :")
            choice1 = int(input("1. sig1\n2. sig2\n3. sig3\n"))
            print("second choice :")
            choice2 = int(input("1. sig1\n2. sig2\n3. sig3\n"))
            test_sample, indices = t.add_signales(samples[choice1][2], samples[choice1][1], samples[choice2][2],
                                                  samples[choice2][1])
            all_results.update({f"{choice1}+{choice2}": [indices, test_sample]})
        else:
            h = int(input("1.by another sig \n 2.by constant \n"))
            if h == 1:
                print("which signal do you want ?")
                print("first choice :")
                choice1 = int(input("1. sig1\n2. sig2\n3. sig3\n"))
                print("second choice :")
                choice2 = int(input("1. sig1\n2. sig2\n3. sig3\n"))
                test_sample, indices = t.multiply_signales(samples[choice1][2], samples[choice1][1], samples[choice2][2],
                                                      samples[choice2][1])
                all_results.update({str(choice1) + "x" + str(choice2): indices})
            else:
                choice1 = int(input("1. sig1\n2. sig2\n3. sig3\n"))
                constant = int(input("what is the constant ?"))
                test_sample, indices = t.multiply_signales_constant(samples[choice1][2], samples[choice1][1],constant)
                all_results.update({str(choice1)+"x"+" constant": indices})
    elif choice == 0:
        break
    else:
        print("invalid choice")
        continue