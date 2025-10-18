from tkinter import *
from tkinter import ttk, messagebox
from new.Squaring import signal_squaring
from new.accumulation import signal_accumulation
from new.cosinusodial import createCos
from new.normalaization import signal_normalization
from new.sinusoidal import createSin
from new.subtraction import subtract_signals
from task_one.addition_of_signals import add_signals
from task_one.display_continuous import draw_continuous
from task_one.display_discrete import draw_discrete
from task_one.multiplication import signal_multiplication
from task_one.read_load_signals import get_signal_body
import numpy as np

# --- Pre-load Signals ---
# It's better to store these in a dictionary for easy look-up by user input
SIGNAL_DATA = {}
try:
    x1, y1 = get_signal_body("Signal1.txt")
    SIGNAL_DATA['1'] = (x1, y1)
    x2, y2 = get_signal_body("Signal2.txt")
    SIGNAL_DATA['2'] = (x2, y2)
    x3, y3 = get_signal_body("signal3.txt")
    SIGNAL_DATA['3'] = (x3, y3)
except FileNotFoundError as e:
    print(f"Error loading signal file: {e}. Ensure 'signals/Signal1.txt', 'signals/Signal2.txt', and 'signals/signal3.txt' exist.")
    # Use dummy data if files are missing to allow the GUI to start, though operations will fail
    dummy_x = np.array([0, 1, 2, 3])
    dummy_y = np.array([0, 1, 0, -1])
    if '1' not in SIGNAL_DATA: SIGNAL_DATA['1'] = (dummy_x, dummy_y)
    if '2' not in SIGNAL_DATA: SIGNAL_DATA['2'] = (dummy_x, dummy_y)
    if '3' not in SIGNAL_DATA: SIGNAL_DATA['3'] = (dummy_x, dummy_y)


# --- Helper Functions for Operations ---

def run_addition():
    """Reads signal IDs from entries and performs addition."""
    sig1_id = addition_entry1.get()
    sig2_id = addition_entry2.get()

    if sig1_id in SIGNAL_DATA and sig2_id in SIGNAL_DATA:
        x_a, y_a = SIGNAL_DATA[sig1_id]
        x_b, y_b = SIGNAL_DATA[sig2_id]
        # add_signals takes (x1, y1, x2, y2, ...)
        add_signals(x_a, y_a, x_b, y_b)
    else:
        print("Invalid signal ID for addition. Use '1', '2', or '3'.")

def run_subtraction():
    """Reads signal IDs from entries and performs subtraction (Signal 1 - Signal 2)."""
    sig1_id = subtraction_entry1.get() # You'd need a new entry widget
    sig2_id = subtraction_entry2.get() # You'd need a new entry widget

    if sig1_id in SIGNAL_DATA and sig2_id in SIGNAL_DATA:
        x_a, y_a = SIGNAL_DATA[sig1_id]
        x_b, y_b = SIGNAL_DATA[sig2_id]
        # subtract_signals takes (x1, y1, x2, y2)
        subtract_signals(x_a, y_a, x_b, y_b)
    else:
        print("Invalid signal ID for subtraction. Use '1', '2', or '3'.")


def run_multiplication():
    """Reads signal ID and constant from entries and performs multiplication."""
    sig_id = mult_sig_entry.get()
    constant_str = mult_const_entry.get()

    try:
        constant = float(constant_str)
    except ValueError:
        print("Invalid multiplication constant. Please enter a number.")
        return

    if sig_id in SIGNAL_DATA:
        x, y = SIGNAL_DATA[sig_id]
        # signal_multiplication performs the operation and calls draw_discrete
        signal_multiplication(x, y, constant)
    else:
        print("Invalid signal ID for multiplication. Use '1', '2', or '3'.")

def run_squaring():
    """Reads signal ID from entry and performs squaring."""
    sig_id = sqr_sig_entry.get()

    if sig_id in SIGNAL_DATA:
        x, y = SIGNAL_DATA[sig_id]
        # signal_squaring performs the operation and calls draw_discrete
        signal_squaring(x, y)
    else:
        print("Invalid signal ID for squaring. Use '1', '2', or '3'.")


# In the '--- Helper Functions for Operations ---' section

def run_normalization():
    """Reads signal ID and normalization range from entries and performs normalization."""
    sig_id = norm_sig_entry.get()
    range_type = norm_range_entry.get() # Should be '0' or '1'

    if sig_id not in SIGNAL_DATA:
        print("Invalid signal ID for normalization. Use '1', '2', or '3'.")
        return

    if range_type not in ['0', '1']:
        print("Invalid range type. Enter '0' for [0, 1] or '1' for [-1, 1].")
        return

    x, y = SIGNAL_DATA[sig_id]
    signal_normalization(x, y, range_type)

# In the '--- Helper Functions for Operations ---' section

def run_accumulation():
    """Reads signal ID from entry and performs signal accumulation."""
    sig_id = acc_sig_entry.get()

    if sig_id not in SIGNAL_DATA:
        print("Invalid signal ID for accumulation. Use '1', '2', or '3'.")
        return

    x, y = SIGNAL_DATA[sig_id]
    signal_accumulation(x, y)

# --- GUI Setup ---

window = Tk()
window.title("DSP FrameWork")
window.geometry("800x500")

label = ttk.Label(window, text="DSP framework", font=("Arial", 16))
label.pack(pady=20)

# --- Display Buttons (Using Signal 1 as default for simplicity) ---

# Button to show discrete
button = ttk.Button(window, text="Display Signal 1 Discrete", command=lambda: draw_discrete(SIGNAL_DATA['1'][0], SIGNAL_DATA['1'][1]))
button.place(x=20, y=80)

# Button to show continuous
button = ttk.Button(window, text="Display Signal 1 Continuous", command=lambda: draw_continuous(SIGNAL_DATA['1'][0], SIGNAL_DATA['1'][1]))
button.place(x=20, y=130)

# --- Addition Section ---

y_add_start = 180

# Button to add signals
button = ttk.Button(window, text="Add Signals", command=run_addition)
button.place(x=20, y=y_add_start)

# Entry for first signal ID
Label(window, text="Signal 1 (1, 2, or 3):").place(x=150, y=y_add_start)
addition_entry1 = Entry(window, width=5)
addition_entry1.place(x=270, y=y_add_start)
addition_entry1.insert(0, "1") # Default value

# Entry for second signal ID
Label(window, text="Signal 2 (1, 2, or 3):").place(x=350, y=y_add_start)
addition_entry2 = Entry(window, width=5)
addition_entry2.place(x=470, y=y_add_start)
addition_entry2.insert(0, "2") # Default value


# --- Multiplication Section ---

y_mult_start = 230

# Button to multiply with a constant
button = ttk.Button(window, text="Multiply Constant", command=run_multiplication)
button.place(x=20, y=y_mult_start)

# Entry for signal ID to multiply
Label(window, text="Signal ID (1, 2, or 3):").place(x=150, y=y_mult_start)
mult_sig_entry = Entry(window, width=5)
mult_sig_entry.place(x=290, y=y_mult_start)
mult_sig_entry.insert(0, "3") # Default value

# Entry for the constant
Label(window, text="Constant:").place(x=370, y=y_mult_start)
mult_const_entry = Entry(window, width=5)
mult_const_entry.place(x=450, y=y_mult_start)
mult_const_entry.insert(0, "5") # Default value

# --- Squaring Section (NEW) ---

y_sqr_start = 280

# Button to square a signal
button = ttk.Button(window, text="Square Signal", command=run_squaring)
button.place(x=20, y=y_sqr_start)

# Entry for signal ID to square
Label(window, text="Signal ID (1, 2, or 3):").place(x=150, y=y_sqr_start)
sqr_sig_entry = Entry(window, width=5)
sqr_sig_entry.place(x=290, y=y_sqr_start)
sqr_sig_entry.insert(0, "1") # Default value

# --- Subtraction Section ---
y_sub_start = 330

button = ttk.Button(window, text="Subtract Signals", command=run_subtraction)
button.place(x=20, y=y_sub_start)

Label(window, text="Signal 1 (1, 2, or 3):").place(x=150, y=y_sub_start)
subtraction_entry1 = Entry(window, width=5)
subtraction_entry1.place(x=270, y=y_sub_start)
subtraction_entry1.insert(0, "1")

Label(window, text="Signal 2 (1, 2, or 3):").place(x=350, y=y_sub_start)
subtraction_entry2 = Entry(window, width=5)
subtraction_entry2.place(x=470, y=y_sub_start)
subtraction_entry2.insert(0, "2")

# --- Normalization Section ---

y_norm_start = 380 # Start position for the new section

# Button to normalize a signal
button = ttk.Button(window, text="Normalize Signal", command=run_normalization)
button.place(x=20, y=y_norm_start)

# Entry for signal ID to normalize
Label(window, text="Signal ID (1, 2, or 3):").place(x=150, y=y_norm_start)
norm_sig_entry = Entry(window, width=5)
norm_sig_entry.place(x=290, y=y_norm_start)
norm_sig_entry.insert(0, "1") # Default value

# Entry for the normalization range type
Label(window, text="Range Type ('0' for [0,1], '1' for [-1,1]):").place(x=370, y=y_norm_start)
norm_range_entry = Entry(window, width=5)
norm_range_entry.place(x=590, y=y_norm_start)
norm_range_entry.insert(0, "1") # Default to [-1, 1]

# --- Accumulation Section ---

y_acc_start = 430 # Start position for the new section

# Button to accumulate a signal
button = ttk.Button(window, text="Accumulate Signal", command=run_accumulation)
button.place(x=20, y=y_acc_start)

# Entry for signal ID to accumulate
Label(window, text="Signal ID (1, 2, or 3):").place(x=150, y=y_acc_start)
acc_sig_entry = Entry(window, width=5)
acc_sig_entry.place(x=290, y=y_acc_start)
acc_sig_entry.insert(0, "1") # Default value

def create_generate_signal_page():
    print("hello")
    window2 = Tk()
    window2.geometry("800x500")

    label = Label(window2, text="Enter data to generate sin signal")
    label.place(x = 20, y = 20)

    label_sin_amplitude = Label(window2, text="Enter the amplitude of the signal")
    label_sin_amplitude.place(x = 20, y = 40)
    sin_amplitude_entry = Entry(window2, width=10)
    sin_amplitude_entry.place(x=290, y=40)

    label_sin_sampling_frequency = Label(window2, text="Enter the Sampling frequency of the signal")
    label_sin_sampling_frequency.place(x = 20, y = 60)
    sin_sampling_frequency_entry = Entry(window2, width=10)
    sin_sampling_frequency_entry.place(x=290, y=60)

    label_sin_analog_frequency = Label(window2, text="Enter the Analog Frequency of the signal")
    label_sin_analog_frequency.place(x = 20, y = 80)
    analog_frequency_entry = Entry(window2, width=10)
    analog_frequency_entry.place(x=290, y=80)

    label_sin_phase_shift = Label(window2, text="Enter the phase shift of the signal")
    label_sin_phase_shift.place(x = 20, y = 100)
    phase_shift_entry = Entry(window2, width=10)
    phase_shift_entry.place(x=290, y=100)

    button1 = ttk.Button(
        window2,
        text="Generate sign",
        command=lambda: createSin(
            int(sin_amplitude_entry.get()),
            float(phase_shift_entry.get()),
            int(analog_frequency_entry.get()),
            int(sin_sampling_frequency_entry.get())
        )
    )

    button1.place(x = 290, y = 120)


    label = Label(window2, text="Enter data to generate cos signal")
    label.place(x=20, y=200)

    label_cos_amplitude = Label(window2, text="Enter the amplitude of the signal")
    label_cos_amplitude.place(x=20, y=220)
    cos_amplitude_entry = Entry(window2, width=10)
    cos_amplitude_entry.place(x=290, y=220)

    label_cos_sampling_frequency = Label(window2, text="Enter the Sampling frequency of the signal")
    label_cos_sampling_frequency.place(x=20, y=240)
    cos_sampling_frequency_entry = Entry(window2, width=10)
    cos_sampling_frequency_entry.place(x=290, y=240)

    label_cos_analog_frequency = Label(window2, text="Enter the Analog Frequency of the signal")
    label_cos_analog_frequency.place(x=20, y=260)
    cos_analog_frequency_entry = Entry(window2, width=10)
    cos_analog_frequency_entry.place(x=290, y=260)

    label_cos_phase_shift = Label(window2, text="Enter the phase shift of the signal")
    label_cos_phase_shift.place(x=20, y=280)
    cos_phase_shift_entry = Entry(window2, width=10)
    cos_phase_shift_entry.place(x=290, y=280)

    button = ttk.Button(
        window2,
        text="Generate Cosine",
        command=lambda: createCos(
            int(cos_amplitude_entry.get()),
            float(cos_phase_shift_entry.get()),
            int(cos_analog_frequency_entry.get()),
            int(cos_sampling_frequency_entry.get())
        )
    )
    button.place(x=290, y=300)

    window2.mainloop()

button = ttk.Button(window, text="generate Signal", command=create_generate_signal_page)
button.place(x=500, y=100)



# Run the window
window.mainloop()