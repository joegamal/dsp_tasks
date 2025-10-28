from task_4.dft_idft import run_dft_idft
from task_one.read_load_signals import get_signal_body

def SignalsAreEqual(TaskName,given_output_filePath,Your_indices,Your_samples):
    expected_indices=[]
    expected_samples=[]
    with open(given_output_filePath, 'r') as f:
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
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print(TaskName+" Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print(TaskName+" Test case failed, your signal have different indices from the expected one")
            return             
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print(TaskName+" Test case failed, your signal have different values from the expected one") 
            return
    print(TaskName+" Test case passed successfully")


x1, y1 = get_signal_body("../../signals/DC_component_input.txt")
x2, y2 = get_signal_body("../../signals/input_Signal_DFT.txt")

Time_index_array, Reconstructed_amplitude_array = run_dft_idft(y2, 16, mode='idft')

SignalsAreEqual("Task Four", "../../signals/Output_Signal_IDFT.txt", x1,
                Reconstructed_amplitude_array)