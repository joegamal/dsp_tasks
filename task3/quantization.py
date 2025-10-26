import numpy as np
import matplotlib.pyplot as plt

from task_one.read_load_signals import get_signal_body

import numpy as np


def quantize_signal_by_bits(x, y, num_bits):
    """
    Quantizes the signal amplitude using a Mid-Tread (uniform) quantizer,
    calculates quantization error, and displays the results.

    Args:
        x (np.array): The time/index array.
        y (np.array): The original amplitude array.
        num_bits (int): The number of bits for quantization (N).
    """
    if len(y) == 0:
        print("Cannot quantize an empty signal.")
        return

    # 1. Determine Levels (L), Range, and Step Size (Delta)
    L = 2 ** num_bits
    y_min = np.min(y)
    y_max = np.max(y)
    quantization_range = y_max - y_min

    if quantization_range == 0:
        print("Signal is constant. Quantization is trivial.")
        y_quantized = y
        y_error = np.zeros_like(y)
        level_index = np.zeros_like(y, dtype=int)
        encoded_bits = [format(0, '0' + str(num_bits) + 'b') for _ in range(len(y))]
    else:
        # Step size (Delta)
        # Note: Delta is the distance between adjacent reconstruction levels.
        # For L levels, the range is divided into L intervals.
        delta = quantization_range / L

        # --- Quantization and Reconstruction ---

        # 1. Normalize and Shift: Map y from [y_min, y_max] to [0, quantization_range]
        y_shifted = y - y_min

        # 2. Level Index Calculation (Mid-Tread Logic: Round to Nearest Level Index)
        # Scale: y_shifted / delta gives a floating-point index [0, L]
        # Rounding to the nearest integer index from 0 to L-1 is the correct Mid-Tread approach.
        # Add 0.5 to shift the boundaries for flooring, effectively rounding to nearest integer.
        level_index = np.floor(y_shifted / delta).astype(int)

        # 3. Clip the index to ensure it's within [0, L-1]
        # The last interval includes y_max and maps to L-1.
        level_index = np.clip(level_index, 0, L - 1)

        # 4. Reconstruct the quantized signal (y_quantized)
        # For a MID-TREAD quantizer, the reconstruction value is the CENTER of the interval.
        # Center of interval 'i' is: y_min + (i * delta) + (delta / 2)
        # Exception: For the highest level (L-1), the reconstruction should generally
        # be y_max if the signal is exactly y_max to maintain range, but for simplicity
        # and standard Mid-Tread, we use the center formula and let the clipping handle it.
        # The index i corresponds to the interval [y_min + i*delta, y_min + (i+1)*delta).
        y_quantized = y_min + (level_index * delta) + (delta / 2)

        # Edge Case Correction (Optional but good practice): The highest level L-1
        # should generally map to y_max or very close to it if y_max is an input.
        # For a Mid-Tread with N-bit encoding (0 to L-1 indices), a simpler approach
        # is to use the formula and rely on the clipping for indices.

        # 5. Calculate Quantization Error: The difference between the original and reconstructed signal.
        y_error = y - y_quantized

        # 6. Encoded Signal (Level Index in Binary)
        encoded_bits = [format(level, '0' + str(num_bits) + 'b') for level in level_index]

    # --- Console Output for Test Cases ---
    print("\n--- Quantization Output ---")
    print(f"Number of Bits (N): {num_bits}")
    print(f"Number of Levels (L): {L}")
    print(f"Signal Min/Max: {y_min:.2f}/{y_max:.2f}")
    print(f"Step Size (Delta): {delta:.4f}")
#
    print(f"\n| Index | Original Value | Level Index | Quantized Value | Error Value | Encoded Bit |")
    print(f"|-------|----------------|-------------|-----------------|-------------|-------------|")
    for i in range(len(x)):
        # Ensure x[i] is treated as an integer index for display if possible
        x_val = int(x[i]) if x[i] == np.round(x[i]) else f"{x[i]:<5.1f}"
        print(
            f"| {x_val:<5} | {y[i]:<14.4f} | {level_index[i]:<11} | {y_quantized[i]:<15.4f} | {y_error[i]:<11.4f} | {encoded_bits[i]:<11} |")
    return encoded_bits, y_quantized

# Example Usage to Demonstrate (You'd need to import numpy to run this)
# x_data = np.array([0, 1, 2, 3, 4, 5])
# y_data = np.array([0.1, 0.4, 1.2, 1.9, 2.7, 3.1]) # Range [0.1, 3.1], Range = 3.0
# quantize_signal_bybits(x_data, y_data, 2) # N=2, L=4, Delta = 3.0/4 = 0.75
# Intervals (Centers):
# [0.1, 0.85) -> Center 0.475 (Index 0)
# [0.85, 1.6) -> Center 1.225 (Index 1)
# [1.6, 2.35) -> Center 1.975 (Index 2)
# [2.35, 3.1] -> Center 2.725 (Index 3)
# Note: The test cases require the output in specific lists (encoded and quantized).
# The current function prints a comprehensive table. You may need to adapt your
# Task1Test.py or the output format here to match those exact list requirements.
# This implementation provides all the requested data.

#x1, y1 = get_signal_body("../signals/Quan1_input.txt")



