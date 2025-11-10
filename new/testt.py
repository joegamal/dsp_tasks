def SigalesAreEqual(TaskName, given_output_filePath, Your_indices, Your_samples):
    """
    Compares two signals (e.g., Index/Sample) against a reference file.
    This version correctly uses a tolerance for all float comparisons.
    """
    expected_indices = []
    expected_samples = []

    # --- 1. Read Expected Values from File ---
    with open(given_output_filePath, 'r') as f:
        # Skip header lines (e.g., 1, 0, 8)
        # NOTE: You may need to adjust this skip count for your IDFT output file
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()

        while line:
            L = line.strip()
            if len(L.split(' ')) == 2:
                parts = L.split(' ')

                # V1: Expected Index (or Magnitude)
                V1_str = parts[0].rstrip('f').strip()
                V1 = float(V1_str)

                # V2: Expected Sample (or Phase)
                V2_str = parts[1].rstrip('f').strip()
                V2 = float(V2_str)

                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break

    # --- 2. Check Length ---
    if len(expected_samples) != len(Your_samples) or len(expected_indices) != len(Your_indices):
        print(TaskName + " Test case failed, your signal has a different length from the expected one")
        return

    TOLERANCE = 1e-6  # A standard tolerance for float comparison

    # --- 3. Check Indices (e.g., time 0, 1, 2...) ---
    for i in range(len(Your_indices)):
        # **BUG FIX:** Compare floats using a tolerance, not '!='
        if abs(Your_indices[i] - expected_indices[i]) > TOLERANCE:
            print(TaskName + f" Test case failed. Index {i} mismatch.")
            print(f"Expected Index: {expected_indices[i]}, Your Index: {Your_indices[i]}")
            return

            # --- 4. Check Samples (the actual signal values) ---
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) > TOLERANCE:
            print(TaskName + f" Test case failed. Sample value mismatch at index {i}.")
            print(f"Expected Sample: {expected_samples[i]}, Your Sample: {Your_samples[i]}")
            return

    print(TaskName + " Test case passed successfully")


import cmath
import numpy as np  # Needed for the loader

import cmath
import math

import cmath
import math


def load_polar_file_as_arrays(filename):
    """
    Reads a Mag/Phase file, skips the header, and returns the data
    as two separate lists (vertical arrays) of floats.

    This function manually parses the file to avoid np.loadtxt errors.
    """
    magnitudes = []
    phases = []

    try:
        with open(filename, 'r') as f:
            # 1. Skip the 3-line header (e.g., "1", "0", "8")
            # You can adjust this number if your headers are different
            f.readline()
            f.readline()
            f.readline()

            # 2. Process each data line
            for line in f:
                line = line.strip()  # Remove leading/trailing whitespace and newlines

                if not line:
                    continue  # Skip empty lines

                # 3. Split the line by *any* whitespace (handles spaces, tabs, etc.)
                # This is more robust than a fixed delimiter
                parts = line.split()

                if len(parts) == 2:
                    # 4. Clean and convert Magnitude (Column 0)
                    mag_str = parts[0].rstrip('f').strip()
                    magnitudes.append(float(mag_str))

                    # 5. Clean and convert Phase (Column 1)
                    phase_str = parts[1].rstrip('f').strip()
                    phases.append(float(phase_str))

        return magnitudes, phases

    except Exception as e:
        print(f"Error during manual file processing {filename}: {e}")
        return [], []
# --- HOW TO USE IT ---
# Your calling code remains exactly the same!
# This new function is a direct, more reliable replacement.

# y5 = load_complex_from_polar_file("../signals/Input_Signal_IDFT_A,Phase.txt")
# if y5:
#     # ... proceed with your IDFT and testing ...

import cmath
import math


# We don't need numpy for this function anymore

def load_complex_from_polar_file2(filename):
    """
    Reads a Mag/Phase file MANUALLY to bypass np.loadtxt bugs,
    skips the header, and converts the data into a list of complex numbers.
    """
    complex_signal = []

    try:
        with open(filename, 'r') as f:
            # 1. Skip the 3-line header
            f.readline()
            f.readline()
            f.readline()

            # 2. Process each data line manually
            for line in f:
                line = line.strip()  # Remove leading/trailing whitespace and newlines

                if not line:
                    continue  # Skip empty lines

                # 3. Split the line by *any* whitespace (handles spaces, tabs, etc.)
                parts = line.split()

                if len(parts) == 2:
                    # 4. Manually clean and convert each part
                    mag_str = parts[0]
                    phase_str = parts[1]

                    # Clean the 'f' suffix and convert to float
                    mag = float(mag_str.rstrip('f').strip())
                    phase = float(phase_str.rstrip('f').strip())

                    # 5. Convert from Polar (Mag, Phase) to Complex (a + bi)
                    complex_num = cmath.rect(mag, phase)
                    complex_signal.append(complex_num)

        return complex_signal

    except Exception as e:
        print(f"Error during manual file processing {filename}: {e}")
        return []