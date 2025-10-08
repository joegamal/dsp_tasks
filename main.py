from tkinter import *
from tkinter import ttk

from task_one.display_continuous import draw_continuous
from task_one.display_discrete import draw_discrete
from task_one.read_load_signals import read_signal, get_signal_body

fileName = "task_one/Signal1.txt"


x, y = get_signal_body(fileName)

root = Tk()
root.title("DSP FrameWork")
root.geometry("800x500")

label = ttk.Label(root, text="DSP framework", font=("Arial", 16))
label.pack(pady=20)

# Add a button
button = ttk.Button(root, text="display signal discrete", command=lambda: draw_discrete(x, y))
button.pack(pady=20)

button = ttk.Button(root, text="display signal continuous", command=lambda: draw_continuous(x, y))
button.pack(pady=20)

# Run the window
root.mainloop()