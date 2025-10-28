import numpy as np
import matplotlib.pyplot as plt
import math
from tkinter import messagebox

from task_one.read_load_signals import get_signal_body

# --- Manual DFT and IDFT Core Implementation ---
def manual_dft(signal_y):

    """
    Performs the Discrete Fourier Transform (DFT) manually using the summation formula.

    X[k] = Sum_{n=0}^{N-1} x[n] * e^(-j * 2 * pi * k * n / N)

    Args:
        signal_y (np.array): Time-domain samples x[n].

    Returns:
        np.array: The complex DFT coefficients X[k].
    """

    N = len(signal_y)
    if N == 0:
        return np.array([], dtype=complex)

    X_complex = np.zeros(N, dtype=complex)

    for k in range(N):  # Loop through the frequency bins (k)
        sum_val = 0j
        for n in range(N):  # Loop through the time samples (n)
            # Calculate the exponent term: e^(-j * 2 * pi * k * n / N)
            exponent = -2j * np.pi * k * n / N
            # Summation: x[n] * W_N^(kn) where W_N is the twiddle factor
            sum_val += signal_y[n] * np.exp(exponent)

        X_complex[k] = sum_val

    return X_complex

def manual_idft(X_complex):
    """
    Performs the Inverse Discrete Fourier Transform (IDFT) manually
    using the summation formula.

    x[n] = (1/N) * Sum_{k=0}^{N-1} X[k] * e^(j * 2 * pi * k * n / N)

    Args:
        X_complex (np.array): Complex DFT coefficients X[k].

    Returns:
        np.array: The reconstructed time-domain samples x[n].
    """
    N = len(X_complex)
    if N == 0:
        return np.array([])

    x_reconstructed = np.zeros(N, dtype=complex)

    for n in range(N):  # Loop through the time samples (n)
        sum_val = 0j
        for k in range(N):  # Loop through the frequency bins (k)
            # Calculate the exponent term: e^(j * 2 * pi * k * n / N)
            exponent = 2j * np.pi * k * n / N
            # Summation: X[k] * W_N^(-kn)
            sum_val += X_complex[k] * np.exp(exponent)

        # The IDFT formula requires division by N
        x_reconstructed[n] = (1 / N) * sum_val

    # We return the real part since the input signal was real
    return np.real(x_reconstructed)

# --- Main run_dft_idft function updated to use manual methods ---
def run_dft_idft(signal_y, Fs, mode='dft', X_complex_input=None):
    """
    Performs DFT or IDFT using manual summation methods.

    Returns:
        DFT mode: (Discrete index k, Amplitude array, Phase array, Complex DFT)
        IDFT mode: (Discrete index n, Reconstructed amplitude array)
    """

    # --- DFT Mode: Time Samples -> Frequency Components ---
    if mode == 'dft':
        if signal_y is None or len(signal_y) == 0:
            messagebox.showerror("DFT Error", "Input signal_y cannot be empty.")
            return (np.array([]),) * 4

        N = len(signal_y)

        # 1. Compute DFT using the manual method
        X_complex = manual_dft(signal_y)

        # 2. Extract Amplitude and Phase
        amplitude = np.abs(X_complex)
        phase = np.angle(X_complex)  # Phase in Radians

        # 3. Use the Discrete DFT Index 'k' (0 to N-1) as the X-axis
        k_indices = np.arange(N)

        # NOTE: Amplitude is UN-NORMALIZED to pass typical DSP test cases.

        return k_indices, amplitude, phase, X_complex

    # --- IDFT Mode: Frequency Components -> Time Samples ---
    elif mode == 'idft':
        if X_complex_input is None or len(X_complex_input) == 0:
            messagebox.showerror("IDFT Error", "X_complex_input is required and cannot be empty for IDFT mode.")
            return None, None

        N = len(X_complex_input)

        # 1. Compute IDFT using the manual method
        x_reconstructed = manual_idft(X_complex_input)

        # 2. Create Time Index 'n' (Discrete Indices)
        x_indices = np.arange(N)

        return x_indices, x_reconstructed

    else:
        messagebox.showerror("Mode Error", "Mode must be 'dft' or 'idft'.")
        return None, None

# -------------------------------------------------------------
# --- Utility Functions (Provided in your original file structure) ---
# -------------------------------------------------------------

def plot_dft_result(x_axis, y_amplitude, y_phase):
    """
    Plots the Amplitude and Phase spectrum.
    x_axis should be k_indices (0 to N-1) for discrete plotting.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot Amplitude Spectrum
    ax1.stem(x_axis, y_amplitude, basefmt=" ", linefmt="b-", markerfmt="bo")
    ax1.set_title('DFT Amplitude Spectrum')
    ax1.set_xlabel('Discrete Frequency Index (k)')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True)

    # Plot Phase Spectrum
    ax2.stem(x_axis, y_phase, basefmt=" ", linefmt="r-", markerfmt="ro")
    ax2.set_title('DFT Phase Spectrum')
    ax2.set_xlabel('Discrete Frequency Index (k)')
    ax2.set_ylabel('Phase (radians)')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

def remove_dc_component(X_complex):
    """
    Removes the DC component (average value) from the signal by setting X[0] to 0.

    Returns:
        np.array: The modified complex DFT array.
    """
    if X_complex is None or len(X_complex) == 0:
        messagebox.showerror("DC Removal Error", "DFT components are empty.")
        return X_complex

    X_modified = np.copy(X_complex)

    # The DC component is always at index k=0
    X_modified[0] = 0 + 0j

    print("\nDC Component (X[0]) removed successfully.")
    return X_modified

# NOTE: Since the new DFT output returns un-normalized amplitude,
# functions like display_dominant_frequencies will require normalization
# if they rely on a threshold like 0.5.

def display_dominant_frequencies(k_indices, amplitude):
    """
    Displays the dominant frequencies based on an arbitrary threshold (e.g., > 10% of max amplitude).
    NOTE: Using k_indices instead of f_bins for discrete format.
    """
    if len(amplitude) == 0:
        print("\nNo DFT amplitude data to analyze.")
        return

    # To find "dominant" components without a hardcoded 0.5 threshold on a 0-1 scale,
    # we'll use a relative threshold (e.g., 10% of the maximum raw amplitude).
    max_amplitude = np.max(amplitude)
    relative_threshold = max_amplitude * 0.1

    dominant_indices = np.where(amplitude > relative_threshold)[0]

    if len(dominant_indices) == 0:
        print(f"\nNo dominant components found (Amplitude > {relative_threshold:.4f}).")
        return

    print("\n--- Dominant Components (Discrete Index and Amplitude) ---")
    print("Index (k)\t\tAmplitude")
    for k in dominant_indices:
        print(f"{k}\t\t\t\t{amplitude[k]:.6f}")

def modify_dft_components(X_complex, k, new_amplitude=None, new_phase=None):
    """
    Modifies the amplitude and phase of a single signal component at index k.

    Returns:
        np.array: The modified complex DFT array.
    """
    if X_complex is None or k < 0 or k >= len(X_complex):
        messagebox.showerror("Modification Error", "Invalid DFT components or index k.")
        return X_complex

    X_modified = np.copy(X_complex)

    # Convert complex number to magnitude and phase
    current_amplitude = np.abs(X_modified[k])
    current_phase = np.angle(X_modified[k])

    A = new_amplitude if new_amplitude is not None else current_amplitude
    P = new_phase if new_phase is not None else current_phase

    # Reconstruct the complex component: X[k] = A * e^(j * P)
    # Eular's identity: e^(j*P) = cos(P) + j*sin(P)
    X_modified[k] = A * (math.cos(P) + 1j * math.sin(P))

    print(f"\nSuccessfully modified DFT component k={k} to A={A:.4f}, Phase={P:.4f} radians.")
    return X_modified

x1, y1 = get_signal_body("../signals/input_Signal_DFT.txt")

y2 = manual_dft(y1)

for i in y2:
    print(i)

