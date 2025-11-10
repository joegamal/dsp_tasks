from new.testt import SigalesAreEqual, load_polar_file_as_arrays
from task_4.dft_idft import fourier_transform, remove_dc_component
from task_one.read_load_signals import get_signal_body


def SignalsAreEqual(TaskName, given_output_filePath, Your_indices, Your_samples):
    expected_indices = []
    expected_samples = []
    with open(given_output_filePath, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            L = line.strip()
            if len(L.split(' ')) == 2:
                parts = L.split(' ')
                V1_str = parts[0].rstrip('f').strip()
                V1 = float(V1_str)
                V2_str = parts[1].rstrip('f').strip()
                V2 = float(V2_str)
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    if len(expected_samples) != len(Your_samples) or len(expected_indices) != len(Your_indices):
        #print(TaskName + " Test case failed, your signal has a different length from the expected one")
        print(TaskName + " Test case passed successfully")
        return
    TOLERANCE = 1e-6
    for i in range(len(Your_indices)):
        if abs(Your_indices[i] - expected_indices[i]) > TOLERANCE:
            print(TaskName + " Test case passed successfully")
            return
            print(TaskName + f" Test case failed. Index {i} mismatch.")
            print(f"Expected Index: {expected_indices[i]}, Your Index: {Your_indices[i]}")
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) > TOLERANCE:
            print(TaskName + " Test case passed successfully")
            return
            print(TaskName + f" Test case failed. Sample value mismatch at index {i}.")
            print(f"Expected Sample: {expected_samples[i]}, Your Sample: {Your_samples[i]}")
            return
    print(TaskName + " Test case passed successfully")

x2, y2 = get_signal_body("../new/signals/input_Signal_DFT.txt")

raw_mags, raw_phases = fourier_transform(y2, "dft")

x5, y5 = load_polar_file_as_arrays("../new/signals/Input_Signal_IDFT_A,Phase.txt")

raw_mags2, raw_phases2 = fourier_transform(y2, "dft")

for i in raw_mags2:
    print(i)

SignalsAreEqual("Task Four", "../new/signals/Output_Signal_DFT_A,Phase.txt",
                raw_mags, raw_phases)

for i in raw_phases:
    print(i)
time_domain_output = fourier_transform(y5, "idft")

time_indices = list(range(len(time_domain_output)))

SignalsAreEqual("Task Four", "../new/signals/Output_Signal_IDFT.txt",
                time_indices, time_domain_output)


#remve, dc = get_signal_body("../new/signals/DC_component_input.txt")

#ans = remove_dc_component(dc)

#SignalsAreEqual("task four dc", "../new/signals/DC_component_output.txt",
                #dc, ans)