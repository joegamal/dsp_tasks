from tkinter import *
from tkinter import ttk
from task_one.addition_of_signals import add_signals
from task_one.display_continuous import draw_continuous
from task_one.display_discrete import draw_discrete
from task_one.multiplication import signal_multiplication
from task_one.read_load_signals import get_signal_body

fileName = "Signal1.txt"


x, y = get_signal_body(fileName)
x2, y2 = get_signal_body("Signal2.txt")
x3, y3 = get_signal_body("Signal3.txt")

window = Tk()
window.title("DSP FrameWork")
window.geometry("800x500")


label = ttk.Label(window, text="DSP framework", font=("Arial", 16))
label.pack(pady=20)

#button to show discrete
button = ttk.Button(window, text="display signal discrete", command=lambda: draw_discrete(x, y))
button.place(x=20, y=80)
label = Label(window, text="Enter signal file name")
label.place(x=150, y=80)

#button to show continuous
button = ttk.Button(window, text="display signal continuous", command=lambda: draw_continuous(x, y))
button.place(x=20, y=130)
label = Label(window, text="Enter signal file name")
label.place(x=170, y=130)

#button to add signals
button = ttk.Button(window, text="add signals", command=lambda: add_signals(x, y, x3, y3))
button.place(x=20, y=180)
label = Label(window, text="Enter signal file names for addition")
label.place(x=170, y=130)

#button to multiply with a constant
button = ttk.Button(window, text="multiply constant", command=lambda: signal_multiplication(x, y, 5))
button.place(x=20, y=230)


# Run the window
window.mainloop()