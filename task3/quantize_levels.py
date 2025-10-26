import numpy as np

from task_one.read_load_signals import get_signal_body


def quantize_signal_by_levels(x, y, num_levels):
    """
    Quantizes the signal amplitude using a Mid-Tread (uniform) quantizer
    based on the specified number of levels (L).

    Args:
        x (np.array): The time/index array.
        y (np.array): The original amplitude array.
        num_levels (int): The number of quantization levels (L).
    """
    if len(y) == 0:
        print("Cannot quantize an empty signal.")
        return

    # 1. Determine Range and Step Size (Delta)
    L = num_levels
    y_min = np.min(y)
    y_max = np.max(y)
    quantization_range = y_max - y_min

    # Calculate number of bits (N) for display purposes only
    num_bits = int(np.ceil(np.log2(L))) if L > 0 else 0

    if quantization_range == 0:
        print("Signal is constant. Quantization is trivial.")
        y_quantized = y
        y_error = np.zeros_like(y)
        level_index = np.zeros_like(y, dtype=int)
        # Use a minimum of 1 bit for encoding if L >= 1
        bit_length = max(1, num_bits)
        encoded_bits = [format(0, '0' + str(bit_length) + 'b') for _ in range(len(y))]
        delta = 0.0
    else:
        # Step size (Delta): distance between adjacent reconstruction levels/interval width
        delta = quantization_range / L

        # --- Quantization and Reconstruction (Mid-Tread) ---

        # 1. Normalize and Scale: Map y from [y_min, y_max] to a scaled index range [0, L]
        y_scaled = (y - y_min) / delta

        # 2. Level Index Calculation: floor(y_scaled) gives the index (0 to L-1) of the interval
        level_index = np.floor(y_scaled).astype(int)

        # 3. Clip the index to ensure it's within [0, L-1]
        level_index = np.clip(level_index, 0, L - 1)

        # 4. Reconstruct the quantized signal (y_quantized)
        # Reconstructed value is the CENTER of the interval: y_min + (i * delta) + (delta / 2)
        y_quantized = y_min + (level_index * delta) + (delta / 2)

        # 5. Calculate Quantization Error
        y_error = y - y_quantized

        y_error = y_error * -1

        y_error_rounded = np.round(y_error, 3)



        # 6. Encoded Signal (Level Index in Binary)
        bit_length = max(1, num_bits)  # Ensure bit length is at least 1
        encoded_bits = [format(level, '0' + str(bit_length) + 'b') for level in level_index]

   ## --- Console Output for Test Cases ---
   #print("\n--- Quantization Output ---")
   #print(f"Number of Levels (L): {L}")
   #print(f"Equivalent Bits (N): {num_bits} (since L = 2^N)")
   #print(f"Signal Min/Max: {y_min:.4f}/{y_max:.4f}")
   #print(f"Step Size (Delta): {delta:.6f}")

    print(f"\n| Index | Original Value | Level Index | Quantized Value | Error Value | Encoded Bit |")
    print(f"|-------|----------------|-------------|-----------------|-------------|-------------|")
    for i in range(len(x)):
        x_val = int(x[i]) if x[i] == np.round(x[i]) else f"{x[i]:<5.1f}"
        print(
            f"| {x_val:<5} | {y[i]:<14.4f} | {level_index[i]:<11} | {y_quantized[i]:<15.4f} | {y_error_rounded[i]:<11.4f} | {encoded_bits[i]:<11} |")

    return level_index , encoded_bits , y_quantized, y_error_rounded
# --- Example Usage ---
# import numpy as np
# x_data = np.array([1, 2, 3, 4, 5, 6, 7])
# y_data = np.array([-1.5, -0.4, 0.2, 1.1, 1.8, 2.5, 3.0])
# quantize_signal_bylevels(x_data, y_data, 8) # L=8 (3 bits)




#quantize_signal_by_levels(x1, y1, 4)