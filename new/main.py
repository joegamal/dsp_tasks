from tkinter import *
from tkinter import ttk, messagebox
from new.Squaring import signal_squaring
from new.accumulation import signal_accumulation
from new.cosinusodial import createCos
from new.normalaization import signal_normalization
from new.sinusoidal import createSin
from new.subtraction import subtract_signals
from task_4.dft_idft import run_dft_idft, display_dominant_frequencies, plot_dft_result, remove_dc_component, \
    modify_dft_components
from task_one.addition_of_signals import add_signals
from task_one.display_continuous import draw_continuous
from task_one.display_discrete import draw_discrete
from task_one.multiplication import signal_multiplication
from task_one.read_load_signals import get_signal_body
import numpy as np

# --- Pre-load Signals ---
# It's better to store these in a dictionary for easy look-up by user input
SIGNAL_DATA = {}
GENERATED_SIGNAL_DATA = {'x': np.array([0]), 'y': np.array([0])}
LAST_DFT_RESULT = {'X_complex': None, 'Fs': None, 'N': None}

# Global entry variables for Quantization (Declare placeholders)
quant_sig_entry = None
quant_bits_entry = None
quant_choice_var = None
dft_sig_entry = None
dft_fs_entry = None
dft_comp_entry = None
dft_amp_entry = None
dft_phase_entry = None

# --- Pre-load Signals ---
# Load existing signals (adjust paths if necessary)
try:
    x1, y1 = get_signal_body("signals/Signal1.txt")
    SIGNAL_DATA['1'] = (x1, y1)
    x2, y2 = get_signal_body("signals/Signal2.txt")
    SIGNAL_DATA['2'] = (x2, y2)
    x3, y3 = get_signal_body("signals/signal3.txt")
    SIGNAL_DATA['3'] = (x3, y3)

    # Load NEW quantization signals
    x_q1, y_q1 = get_signal_body("signals/Quan1_input.txt")  # Assuming file is in the same accessible directory
    SIGNAL_DATA['Q1'] = (x_q1, y_q1)
    x_q2, y_q2 = get_signal_body("signals/Quan2_input.txt")
    SIGNAL_DATA['Q2'] = (x_q2, y_q2)
    x_dft, y_dft = get_signal_body("signals/input_Signal_DFT.txt")
    SIGNAL_DATA['DFT'] = (x_dft, y_dft)
    x_dc, y_dc = get_signal_body("signals/DC_component_input.txt")
    SIGNAL_DATA['DC'] = (x_dc, y_dc)
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


# In main.py (Place this with your other run_... helper functions)

# ------------------------------------------------------------------
# --- Helper Function for Quantization -----------------------------
# ------------------------------------------------------------------



def run_quantization():
    """Reads signal ID, value, and choice (Bits/Levels) and performs quantization."""
    global quant_sig_entry, quant_val_entry, quant_choice_var, SIGNAL_DATA

    sig_id = quant_sig_entry.get()
    val_input_str = quant_val_entry.get()
    choice = quant_choice_var.get()  # 'bits' or 'levels'

    # 1. Validate Signal ID
    if sig_id not in SIGNAL_DATA:
        messagebox.showerror("Error", f"Invalid signal ID: '{sig_id}'. Use 'Q1' or 'Q2'.")
        return

    # 2. Validate Numerical Input and Calculate Bits (N)
    try:
        val_input = int(val_input_str)
        if val_input <= 0:
            messagebox.showerror("Error", "Input must be a positive integer.")
            return

        num_bits = 0
        if choice == 'bits':
            num_bits = val_input
            if num_bits > 16:
                messagebox.showwarning("Warning", "Clamping number of bits to 16 for safety.")
                num_bits = 16
        elif choice == 'levels':
            # Calculate N = ceil(log2(L))
            num_bits = int(np.ceil(np.log2(val_input)))
            messagebox.showinfo("Conversion", f"Input of {val_input} levels (L) results in {num_bits} bits (N).")

        if num_bits <= 0:
            messagebox.showerror("Error", "Calculated number of bits must be greater than 0.")
            return

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid integer.")
        return

    # 3. Get Signal Data and Run Quantization
    x, y = SIGNAL_DATA[sig_id]
    #quantize_signal(x, y, num_bits)


# In main.py (Helper Functions Section)

def get_dft_inputs():
    """Helper to retrieve common DFT inputs and validate."""
    global dft_sig_entry, dft_fs_entry
    sig_id = dft_sig_entry.get()
    fs_str = dft_fs_entry.get()

    if sig_id not in SIGNAL_DATA:
        messagebox.showerror("Error", f"Invalid signal ID: '{sig_id}'. Use 1, 2, 3, Q1, Q2, DFT, or DC.")
        return None, None, None

    try:
        Fs = float(fs_str)
        if Fs <= 0:
            messagebox.showerror("Error", "Sampling Frequency (Fs) must be positive.")
            return None, None, None
    except ValueError:
        messagebox.showerror("Error", "Invalid Fs. Please enter a number.")
        return None, None, None

    x, y = SIGNAL_DATA[sig_id]
    return x, y, Fs


def run_dft_analysis():
    """Applies DFT, plots, and displays dominant frequencies."""
    global LAST_DFT_RESULT
    _, y, Fs = get_dft_inputs()
    if y is None: return

    try:
        f_bins, amp_norm, phase, X_complex = run_dft_idft(y, Fs, mode='dft')

        # Store result for subsequent IDFT/modification
        LAST_DFT_RESULT['X_complex'] = X_complex
        LAST_DFT_RESULT['Fs'] = Fs
        LAST_DFT_RESULT['N'] = len(y)

        plot_dft_result(f_bins, amp_norm, phase)
        display_dominant_frequencies(f_bins, amp_norm)

    except Exception as e:
        messagebox.showerror("DFT Error", f"An error occurred during DFT: {e}")


def run_remove_dc():
    """Removes the DC component (k=0) from the last computed DFT result and re-analyzes."""
    global LAST_DFT_RESULT
    if LAST_DFT_RESULT['X_complex'] is None:
        messagebox.showwarning("Warning", "Run DFT Analysis first.")
        return

    X_complex = LAST_DFT_RESULT['X_complex']
    Fs = LAST_DFT_RESULT['Fs']

    X_modified = remove_dc_component(X_complex)

    # Re-analyze and plot the new spectrum
    f_bins, amp_norm, phase, _ = run_dft_idft(X_modified, Fs, mode='dft')

    # Update stored result
    LAST_DFT_RESULT['X_complex'] = X_modified

    plot_dft_result(f_bins, amp_norm, phase)
    display_dominant_frequencies(f_bins, amp_norm)
    messagebox.showinfo("Success", "DC Component Removed. New spectrum displayed.")


def open_modify_dialog():
    """Opens a separate window for modifying Amplitude and Phase."""
    global dft_comp_entry, dft_amp_entry, dft_phase_entry, LAST_DFT_RESULT

    if LAST_DFT_RESULT['X_complex'] is None:
        messagebox.showwarning("Warning", "Run DFT Analysis first before modifying components.")
        return

    mod_window = Toplevel(window)
    mod_window.title("Modify DFT Components")
    mod_window.geometry("450x300")

    Label(mod_window, text=f"Modify Amplitude/Phase (Indices 0 to {LAST_DFT_RESULT['N'] - 1})",
          font=("Arial", 10)).pack(pady=10)

    # Component Index (k)
    Label(mod_window, text="Component Index (k):").place(x=20, y=50)
    dft_comp_entry = Entry(mod_window, width=5)
    dft_comp_entry.place(x=150, y=50)
    dft_comp_entry.insert(0, "1")

    # New Amplitude
    Label(mod_window, text="New Amplitude:").place(x=20, y=80)
    dft_amp_entry = Entry(mod_window, width=15)
    dft_amp_entry.place(x=150, y=80)
    dft_amp_entry.insert(0, "e.g., 5.0")

    # New Phase (Radians)
    Label(mod_window, text="New Phase (Radians):").place(x=20, y=110)
    dft_phase_entry = Entry(mod_window, width=15)
    dft_phase_entry.place(x=150, y=110)
    dft_phase_entry.insert(0, "e.g., 1.57 (pi/2)")

    Button(mod_window, text="Apply Modification", command=apply_modification_and_update).place(x=20, y=160)


def apply_modification_and_update():
    """Reads input from the modification dialog and applies the change."""
    global dft_comp_entry, dft_amp_entry, dft_phase_entry, LAST_DFT_RESULT

    try:
        k = int(dft_comp_entry.get())
        amp_str = dft_amp_entry.get().strip()
        phase_str = dft_phase_entry.get().strip()

        # Determine new amplitude and phase (None means use current value)
        new_amplitude = float(amp_str) if amp_str and amp_str != "e.g., 5.0" else None
        new_phase = float(phase_str) if phase_str and phase_str != "e.g., 1.57 (pi/2)" else None

        if k < 0 or k >= LAST_DFT_RESULT['N']:
            messagebox.showerror("Index Error", f"Component index k must be between 0 and {LAST_DFT_RESULT['N'] - 1}.")
            return

        X_modified = modify_dft_components(LAST_DFT_RESULT['X_complex'], k, new_amplitude, new_phase)

        # Re-analyze and plot the new spectrum
        Fs = LAST_DFT_RESULT['Fs']
        f_bins, amp_norm, phase, _ = run_dft_idft(X_modified, Fs, mode='dft')

        # Update stored result
        LAST_DFT_RESULT['X_complex'] = X_modified

        plot_dft_result(f_bins, amp_norm, phase)
        messagebox.showinfo("Success", f"Component k={k} Modified. New spectrum displayed.")

    except ValueError:
        messagebox.showerror("Input Error", "Invalid numerical input for index, amplitude, or phase.")
    except Exception as e:
        messagebox.showerror("Modification Error", f"An error occurred: {e}")


def run_idft_reconstruction():
    """Reconstructs the signal using IDFT on the last computed/modified DFT result."""
    global LAST_DFT_RESULT
    if LAST_DFT_RESULT['X_complex'] is None:
        messagebox.showwarning("Warning", "Run DFT Analysis and/or Modifications first.")
        return

    try:
        x_indices, y_reconstructed = run_dft_idft(
            signal_y=None,
            Fs=LAST_DFT_RESULT['Fs'],
            mode='idft',
            X_complex_input=LAST_DFT_RESULT['X_complex']
        )

        # Assuming draw_discrete is imported and works
        # If draw_discrete is not in scope, you'll need to update imports
        from task_one.display_discrete import draw_discrete
        draw_discrete(x_indices, y_reconstructed)
        messagebox.showinfo("Success", "Signal reconstructed using IDFT.")

        # Print output for IDFT test case comparison
        print("\n--- IDFT Reconstructed Signal ---")
        print("n\tAmplitude")
        for i in range(len(x_indices)):
            print(f"{int(x_indices[i])}\t{y_reconstructed[i]:.6f}")

    except Exception as e:
        messagebox.showerror("IDFT Error", f"An error occurred during IDFT: {e}")

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

# In main.py (Towards the end of GUI setup)

# Ensure window size is large enough
# window.geometry("800x600")

# --- Quantization Section (NEW) ---

y_quant_start = 500 # Adjust y position as needed to fit



# Tkinter variable for radio button choice
quant_choice_var = StringVar(window, "bits") # Default to bits

# Button to quantize a signal
button = ttk.Button(window, text="Quantize Signal", command=run_quantization)
button.place(x=20, y=y_quant_start)

# Entry for signal ID
Label(window, text="Signal ID (Q1 or Q2):").place(x=150, y=y_quant_start)
quant_sig_entry = Entry(window, width=5)
quant_sig_entry.place(x=280, y=y_quant_start)
quant_sig_entry.insert(0, "Q1") # Default value

# Radio Buttons for Choice
Label(window, text="Input Type:").place(x=350, y=y_quant_start)
R1 = Radiobutton(window, text="Bits", variable=quant_choice_var, value="bits")
R1.place(x=430, y=y_quant_start)
R2 = Radiobutton(window, text="Levels", variable=quant_choice_var, value="levels")
R2.place(x=490, y=y_quant_start)

# Entry for the numerical value
Label(window, text="Value (N or L):").place(x=570, y=y_quant_start)
quant_val_entry = Entry(window, width=5)
quant_val_entry.place(x=670, y=y_quant_start)
quant_val_entry.insert(0, "4") # Default value


# --- Menu Bar Setup ---
menu_bar = Menu(window)
window.config(menu=menu_bar)

# --- Frequency Domain Menu ---
freq_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Frequency Domain", menu=freq_menu)


# Function to open the dialog (placed in main.py)
def open_frequency_domain_dialog():
    global dft_sig_entry, dft_fs_entry

    freq_window = Toplevel(window)
    freq_window.title("Frequency Domain Analysis (DFT / IDFT)")
    freq_window.geometry("500x350")

    Label(freq_window, text="Discrete Fourier Transform (DFT / IDFT)", font=("Arial", 12)).pack(pady=10)

    # Input Section
    y_start = 50
    Label(freq_window, text="Choose action (DFT, DC):").place(x=20, y=y_start)
    dft_sig_entry = Entry(freq_window, width=10)
    dft_sig_entry.place(x=200, y=y_start)
    dft_sig_entry.insert(0, "DFT")

    y_start += 30
    Label(freq_window, text="Sampling Frequency (Fs in Hz):").place(x=20, y=y_start)
    dft_fs_entry = Entry(freq_window, width=10)
    dft_fs_entry.place(x=200, y=y_start)
    dft_fs_entry.insert(0, "100")

    # --- Feature Buttons ---

    y_start += 50
    # 1. DFT Analysis
    ttk.Button(freq_window, text="1. Run DFT & Plot Spectrum", command=run_dft_analysis).place(x=20, y=y_start)

    y_start += 40
    # 2. Remove DC Component
    ttk.Button(freq_window, text="2. Remove DC Component (F[0]=0)", command=run_remove_dc).place(x=20, y=y_start)

    y_start += 40
    # 3. Modify Amplitude/Phase
    ttk.Button(freq_window, text="3. Modify Components (A & Phase)", command=open_modify_dialog).place(x=20, y=y_start)

    y_start += 40
    # 4. IDFT Reconstruction
    ttk.Button(freq_window, text="4. Reconstruct Signal (IDFT)", command=run_idft_reconstruction).place(x=20, y=y_start)


# The main menu command:
freq_menu.add_command(label="Open DFT/IDFT Toolbox", command=open_frequency_domain_dialog)

# ... (window.mainloop()) ...
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