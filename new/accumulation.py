import numpy as np
from task_one.display_discrete import draw_discrete


# This function calculates the accumulated sum of the signal amplitude.
# It implements y(n) = Sum_{k=index_start}^{n} x(k)
def signal_accumulation(x, y):
    """
    Calculates the accumulated sum of the signal amplitude (y) at each index (x).

    Args:
        x (np.array): The time/index array.
        y (np.array): The amplitude array to be accumulated.

    Returns:
        tuple: (x, y_accumulated)
    """
    if len(y) == 0:
        print("Cannot accumulate an empty signal.")
        return x, y

    # Use numpy.cumsum for efficient running sum calculation
    y_accumulated = np.cumsum(y)

    # Debug prints (optional)
    print("Final X:", x)
    print("Accumulated Y:", y_accumulated)

    draw_discrete(x, y_accumulated)
    return x, y_accumulated