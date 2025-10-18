import numpy as np

from task_one.display_discrete import draw_discrete

# This function assumes only two signals are passed for subtraction (Signal 1 - Signal 2)

def subtract_signals(x1, y1, x2, y2):
    # Find the minimum length to ensure arrays are the same size for element-wise operation
    len1 = len(x1)
    len2 = len(x2)
    min_len = min(len1, len2)

    # Truncate both x and y arrays to the minimum length
    # This assumes that the signals are aligned and starting from the same index (e.g., index 0)
    # If signals start at different indices, more complex alignment logic is needed.
    x_final = x1[:min_len]
    y1_trunc = y1[:min_len]
    y2_trunc = y2[:min_len]


    y_final = np.absolute(y1_trunc - y2_trunc)


    print("Final X:", x_final)
    print("Final Y:", y_final)

    draw_discrete(x_final, y_final)

    return x_final, y_final