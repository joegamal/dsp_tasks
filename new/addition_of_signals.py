import numpy as np

from task_one.display_discrete import draw_discrete




def add_signals(*args):
    x_arrays = args[::2]
    y_arrays = args[1::2]

    # Find the x array with the least length
    min_len = min(len(x) for x in x_arrays)
    x_fianl = min(x_arrays, key=len)[:min_len]

    # Sum all y arrays element-wise
    y_fianl = np.sum(np.vstack(y_arrays), axis=0)

    # Debug prints (optional)
    print("Final X:", x_fianl)
    print("Final Y:", y_fianl)

    draw_discrete(x_fianl, y_fianl)
    return x_fianl, y_fianl







