import numpy as np
import matplotlib.pyplot as plt
import math
from tkinter import messagebox


# The core transformation logic is handled by NumPy's highly optimized FFT/IFFT.

def run_dft_idft(signal_y, Fs, mode='dft', X_complex_input=None):
    """
    Performs DFT or IDFT.

    Args:
        signal_y (np.array): Time-domain samples (for DFT).
        Fs (float): Sampling frequency in Hz.
        mode (str): 'dft' or 'idft'.
        X_complex_input (np.array, optional): Complex frequency components for IDFT.

    Returns:
        tuple: (Frequency array, Normalized Amplitude array, Phase array, Complex DFT) for DFT,
               or (Time index array, Reconstructed amplitude array) for IDFT.
    """
    N = len(signal_y) if mode == 'dft' else len(X_complex_input)

    if mode == 'dft':
        # 1. Compute DFT
        X_complex = np.fft.fft(signal_y)

        # 2. Extract Amplitude and Phase
        amplitude = np.abs(X_complex)
        phase = np.angle(X_complex)  # Phase in Radians

        # 3. Calculate Frequency Bins
        # The frequencies run from 0 to Fs * (N-1) / N
        f_bins = np.fft.fftfreq(N, d=1 / Fs)

        # 4. Normalize Amplitude (0 to 1)
        max_amplitude = np.max(amplitude)
        if max_amplitude == 0:
            amplitude_norm = amplitude
        else:
            # Normalizing by the absolute maximum for plotting ease
            amplitude_norm = amplitude / max_amplitude

        return f_bins, amplitude_norm, phase, X_complex

    elif mode == 'idft':
        if X_complex_input is None:
            raise ValueError("X_complex_input must be provided for IDFT.")

        # Compute IDFT (np.fft.ifft handles the 1/N scaling)
        x_reconstructed_complex = np.fft.ifft(X_complex_input)

        # Take the real part, as the imaginary part should be negligible noise
        x_reconstructed = np.real(x_reconstructed_complex)

        # Create time index array
        x_indices = np.arange(N)

        return x_indices, x_reconstructed


def plot_dft_result(f_bins, amplitude_norm, phase):
    """Plots the normalized amplitude and phase spectra."""

    # Use shifted spectrum for a centered plot (negative and positive frequencies)
    f_shifted = np.fft.fftshift(f_bins)
    amplitude_norm_shifted = np.fft.fftshift(amplitude_norm)
    phase_shifted = np.fft.fftshift(phase)

    plt.figure(figsize=(12, 8))

    # Plot 1: Amplitude Spectrum (Normalized 0 to 1)
    plt.subplot(2, 1, 1)
    plt.plot(f_shifted, amplitude_norm_shifted, marker='o', linestyle='-', markersize=4)
    plt.title("DFT Amplitude Spectrum (Normalized 0-1)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized Amplitude")
    plt.ylim(0, 1.1)
    plt.grid(True)

    # Plot 2: Phase Spectrum (in Radians)
    plt.subplot(2, 1, 2)
    plt.plot(f_shifted, phase_shifted, marker='o', linestyle='-', markersize=4)
    plt.title("DFT Phase Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (Radians)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Print output in the requested format
    print("\n--- DFT Analysis Output ---")
    print("k\tFrequency (Hz)\tNormalized Amplitude\tPhase (rad)")
    for k in range(len(f_bins)):
        print(f"{k}\t{f_bins[k]:.4f}\t\t{amplitude_norm[k]:.6f}\t\t{phase[k]:.6f}")


def display_dominant_frequencies(f_bins, amplitude_norm):
    """Displays frequencies where normalized amplitude > 0.5."""
    # Note: We check the non-shifted spectrum indices.
    dominant_indices = np.where(amplitude_norm > 0.5)[0]

    if len(dominant_indices) == 0:
        print("\nNo dominant frequencies found (Normalized Amplitude > 0.5).")
        return

    print("\n--- Dominant Frequencies (Normalized Amplitude > 0.5) ---")
    print("Frequency (Hz)\tNormalized Amplitude")
    for k in dominant_indices:
        print(f"{f_bins[k]:.4f}\t\t{amplitude_norm[k]:.6f}")


def modify_dft_components(X_complex, k, new_amplitude=None, new_phase=None):
    """
    Modifies the amplitude and phase of a single signal component at index k.

    Returns:
        np.array: The modified complex DFT array.
    """
    X_modified = np.copy(X_complex)

    # Convert complex number to magnitude and phase
    current_amplitude = np.abs(X_modified[k])
    current_phase = np.angle(X_modified[k])

    A = new_amplitude if new_amplitude is not None else current_amplitude
    P = new_phase if new_phase is not None else current_phase

    # Reconstruct the complex component: X[k] = A * e^(j * P)
    X_modified[k] = A * (math.cos(P) + 1j * math.sin(P))

    print(f"\nSuccessfully modified DFT component k={k} to A={A:.4f}, Phase={P:.4f} rad.")
    return X_modified


def remove_dc_component(X_complex):
    """Removes the DC component by setting the F[0] term to zero."""
    X_modified = np.copy(X_complex)
    if len(X_modified) > 0:
        # DC component is always at index k=0
        X_modified[0] = 0.0 + 0.0j
        print("\nDC Component (k=0) successfully removed.")
    return X_modified