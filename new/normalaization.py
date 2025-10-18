import numpy as np
from task_one.display_discrete import draw_discrete



def signal_normalization(x, y, range_type):
    """
    Normalizes the signal amplitude to either [0, 1] or [-1, 1].

    Args:
        x (np.array): The time/index array.
        y (np.array): The amplitude array to be normalized.
        range_type (str): '0' for [0, 1] range, '1' for [-1, 1] range.

    Returns:
        tuple: (x, y_normalized)
    """
    if len(y) == 0:
        print("Cannot normalize an empty signal.")
        return x, y

    y_min = np.min(y)
    y_max = np.max(y)

    # Handle the trivial case where the signal is a constant (y_max == y_min)
    if y_max == y_min:
        y_normalized = np.zeros_like(y, dtype=float)
        if range_type == '1':
            # If normalizing to [-1, 1], and y is constant, result is 0
            y_normalized = y_normalized
        elif range_type == '0':
            # If normalizing to [0, 1], and y is constant, result is 0
            y_normalized = y_normalized
    else:
        # Standard Min-Max Normalization
        y_normalized = (y - y_min) / (y_max - y_min)

        # Adjust range if user chose [-1, 1]
        if range_type == '1':
            y_normalized = (2 * y_normalized) - 1

    # Debug prints (optional)
    print("Normalization Range:", "[0, 1]" if range_type == '0' else "[-1, 1]")
    print("Original Min:", y_min, " Max:", y_max)
    print("Final X:", x)
    print("Final Y:", y_normalized)
    print("Normalized Min:", np.min(y_normalized), " Max:", np.max(y_normalized))

    draw_discrete(x, y_normalized)

    return x, y_normalized