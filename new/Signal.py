import numpy as np
import matplotlib.pyplot as plt
import os
# Import test functions and the signal reading utility from the companion file
from new.Task1Test import ReadSignalFile, AddSignalSamplesAreEqual, MultiplySignalByConst


# --- 1. Signal Data Structure ---

class Signal:
    """
    A class to represent a discrete-time signal.

    Attributes:
        indices (np.ndarray): The index (time) values of the samples.
        samples (np.ndarray): The amplitude (value) of the samples.
        filename (str): The source file name or description of the signal.
    """

    def __init__(self, indices=None, samples=None, filename=""):
        # Convert inputs to numpy arrays for efficient computation
        self.indices = np.array(indices, dtype=int) if indices is not None else np.array([], dtype=int)
        self.samples = np.array(samples, dtype=float) if samples is not None else np.array([], dtype=float)
        self.filename = filename

    def is_valid(self):
        """Checks if the signal contains valid data (non-empty and matching lengths)."""
        return len(self.indices) > 0 and len(self.indices) == len(self.samples)


# --- 2. File Reading and Display Functions ---

def read_signal_file(file_path):
    """
    Reads signal indices and samples from a text file.
    It uses the ReadSignalFile function from the Task1Test.py for parsing.
    """
    try:
        # Use the provided function to read the data
        indices, samples = ReadSignalFile(file_path)
        return Signal(indices, samples, os.path.basename(file_path))
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'.")
        return Signal()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return Signal()


def plot_signal(signals, plot_type='discrete'):
    """
    Displays one or two signals in a plot in either continuous or discrete representation.

    Args:
        signals (list[Signal]): A list containing one or two valid Signal objects.
        plot_type (str): 'discrete' (stem plot) or 'continuous' (line plot).
    """
    # Filter out invalid signals before plotting
    valid_signals = [s for s in signals if s.is_valid()]

    if not valid_signals:
        print("No valid signals to display.")
        return

    # Use a modern style for better aesthetics
    plt.style.use('seaborn-v0_8-darkgrid')

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Define styles for the plots
    line_styles = ['o-', 's--']
    stem_markers = ['o', 's']
    colors = ['#1f77b4', '#ff7f0e']  # Blue and Orange

    title_suffix = "Discrete (Stem Plot)" if plot_type == 'discrete' else "Continuous (Line Plot)"
    ax.set_title(f"Signal Representation ({title_suffix})", fontsize=16, fontweight='bold')
    ax.set_xlabel("Time Index (n)", fontsize=14)
    ax.set_ylabel("Amplitude (x[n])", fontsize=14)

    # Track the min/max index and sample values for proper axis limits
    all_indices = np.concatenate([s.indices for s in valid_signals])
    all_samples = np.concatenate([s.samples for s in valid_signals])

    if len(all_indices) > 0:
        index_min = np.min(all_indices)
        index_max = np.max(all_indices)
        ax.set_xlim(index_min - 1, index_max + 1)

        sample_max = np.max(all_samples)
        sample_min = np.min(all_samples)

        # Add a small buffer (10% of range) to y-limits
        buffer = max((sample_max - sample_min) * 0.1, 1.0)  # Ensure at least 1 unit buffer
        ax.set_ylim(sample_min - buffer, sample_max + buffer)

    for i, sig in enumerate(valid_signals):
        label = f"Signal: {sig.filename or 'Result Signal'}"
        color = colors[i % len(colors)]

        if plot_type == 'discrete':
            # Stem plot for discrete representation
            ax.stem(sig.indices, sig.samples,
                    linefmt=color,
                    markerfmt=f'{stem_markers[i % len(stem_markers)]}{color}',
                    basefmt=" ",
                    label=label)
        else:
            # Line plot for continuous representation (joining the discrete points)
            ax.plot(sig.indices, sig.samples,
                    line_styles[i % len(line_styles)],
                    color=color,
                    linewidth=2,
                    markersize=6,
                    label=label)

    ax.legend(loc='upper right', frameon=True, shadow=True, fontsize=12)
    # Add a horizontal line at y=0 for better readability
    ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
    plt.show()


# --- 3. Arithmetic Operations ---

def align_signals(sig1, sig2):
    """
    Aligns two signals to a common time index set for arithmetic operations.
    If a signal is not defined at an index, its sample value is assumed to be 0.0.
    Returns: aligned_sig1_samples, aligned_sig2_samples, common_indices
    """
    if not sig1.is_valid() or not sig2.is_valid():
        return np.array([]), np.array([]), np.array([])

    # 1. Determine the common range of indices
    min_idx = min(np.min(sig1.indices), np.min(sig2.indices))
    max_idx = max(np.max(sig1.indices), np.max(sig2.indices))

    # 2. Create the complete set of indices for the resulting signal
    common_indices = np.arange(min_idx, max_idx + 1)

    # 3. Create dictionaries for quick sample lookup (index: sample)
    map1 = dict(zip(sig1.indices, sig1.samples))
    map2 = dict(zip(sig2.indices, sig2.samples))

    # 4. Align samples: use 0.0 for indices where a signal is not defined
    aligned_samples1 = np.array([map1.get(i, 0.0) for i in common_indices])
    aligned_samples2 = np.array([map2.get(i, 0.0) for i in common_indices])

    return aligned_samples1, aligned_samples2, common_indices


def add_signals(signals):
    """
    Adds any number of input signals, handling alignment across all of them.

    Args:
        signals (list[Signal]): List of signals to add.

    Returns:
        Signal: The resulting summed signal.
    """
    # Filter out invalid signals
    valid_signals = [s for s in signals if s.is_valid()]

    if not valid_signals:
        print("No valid signals provided for addition.")
        return Signal()
    if len(valid_signals) == 1:
        return valid_signals[0]

    # 1. Determine the overall common index range across ALL signals
    all_indices = np.concatenate([s.indices for s in valid_signals])
    if len(all_indices) == 0:
        return Signal()

    min_idx = np.min(all_indices)
    max_idx = np.max(all_indices)
    common_indices = np.arange(min_idx, max_idx + 1)

    # Initialize the result array with zeros
    total_samples = np.zeros(len(common_indices), dtype=float)

    # 2. Create index-to-value maps for all signals
    for sig in valid_signals:
        sig_map = dict(zip(sig.indices, sig.samples))

        # 3. Align and add the samples from the current signal
        for i, idx in enumerate(common_indices):
            total_samples[i] += sig_map.get(idx, 0.0)

    return Signal(common_indices, total_samples, filename="Summed Signal")


def multiply_signal_by_constant(signal, constant):
    """
    Multiplies a signal's amplitude by a constant value (amplification/reduction/inversion).

    Args:
        signal (Signal): The input signal.
        constant (float): The multiplication factor.

    Returns:
        Signal: The resulting scaled signal.
    """
    if not signal.is_valid():
        print("Cannot multiply an invalid signal.")
        return Signal()

    # Element-wise multiplication
    result_samples = signal.samples * constant

    result_signal = Signal(signal.indices, result_samples, filename=f"{signal.filename.split('.')[0]} * {constant}")

    # Check for inversion
    if constant < 0:
        print(f"\nNote: Signal amplitude has been inverted and scaled by {constant}.")

    return result_signal


# --- 4. Menu and Main Logic ---

def display_main_menu():
    """Displays the main menu options."""
    print("\n--- Signal Processing Framework Menu ---")
    print("1. Load Signal from File")
    print("2. Display Loaded Signals (Max 2 simultaneous plots)")
    print("3. Arithmetic Operations")
    print("4. Run Test Cases (Requires expected output files)")
    print("5. Exit")


def display_arithmetic_menu():
    """Displays the arithmetic operations menu."""
    print("\n--- Arithmetic Operations Menu ---")
    print("A. Addition (Add any number of loaded signals)")
    print("M. Multiplication (Multiply one signal by a constant)")
    print("B. Back to Main Menu")


def main():
    """Main application loop."""
    # Global state to hold loaded signals
    loaded_signals = {}

    # Default files to attempt loading
    default_files = ["Signal1.txt", "Signal2.txt", "signal3.txt"]

    # Initialize state by attempting to load default files
    print("Attempting to load default signals (Signal1.txt, Signal2.txt, signal3.txt)...")
    for path in default_files:
        if os.path.exists(path):
            sig = read_signal_file(path)
            if sig.is_valid():
                key = os.path.basename(path)
                loaded_signals[key] = sig
                print(f"Loaded signal '{key}' successfully.")
        else:
            print(f"Warning: Default file '{path}' not found.")

    while True:
        display_main_menu()
        choice = input("Enter your choice (1-5): ").strip().lower()

        if choice == '1':
            file_path = input("Enter the path/name of the signal file (e.g., 'Signal4.txt'): ").strip()
            if not file_path:
                print("Operation cancelled.")
                continue

            sig = read_signal_file(file_path)
            if sig.is_valid():
                key = os.path.basename(file_path)
                loaded_signals[key] = sig
                print(f"Signal '{key}' loaded successfully. Total loaded signals: {len(loaded_signals)}")

        elif choice == '2':
            if not loaded_signals:
                print("No signals are currently loaded.")
                continue

            available_keys = list(loaded_signals.keys())
            print("\nAvailable Signals:")
            for i, key in enumerate(available_keys):
                print(f"  {i + 1}: {key}")

            # Request up to two signals for dual display
            indices_str = input(
                "Enter the numbers (1, 2, ...) of up to two signals to display (e.g., '1' or '1,3'): ").strip()

            try:
                # Convert input numbers to 0-based list indices
                selected_indices = [int(i.strip()) - 1 for i in indices_str.split(',') if i.strip()]
                # Filter valid indices and take max 2
                signals_to_display = [loaded_signals[available_keys[i]] for i in selected_indices if
                                      0 <= i < len(available_keys)][:2]

                if not signals_to_display:
                    print("No valid signals selected.")
                    continue

                plot_mode = input("Display as 'discrete' (d) or 'continuous' (c)? ").strip().lower()

                if plot_mode in ['d', 'discrete']:
                    plot_signal(signals_to_display, 'discrete')
                elif plot_mode in ['c', 'continuous']:
                    plot_signal(signals_to_display, 'continuous')
                else:
                    print("Invalid display mode. Plotting cancelled.")

            except ValueError:
                print("Invalid input format for signal selection.")
            except Exception as e:
                print(f"An unexpected error occurred during plotting: {e}")


        elif choice == '3':
            # Arithmetic Operations Menu
            while True:
                display_arithmetic_menu()
                op_choice = input("Enter your operation choice (A, M, B): ").strip().lower()

                if op_choice == 'b':
                    break  # Back to main menu

                if not loaded_signals:
                    print("Please load signals first before performing arithmetic operations.")
                    continue

                available_keys = list(loaded_signals.keys())
                print("\nAvailable Signals:")
                for i, key in enumerate(available_keys):
                    print(f"  {i + 1}: {key}")

                if op_choice == 'a':
                    # Addition
                    indices_str = input("Enter the numbers of signals to add (e.g., '1,2,3'): ").strip()
                    try:
                        selected_indices = [int(i.strip()) - 1 for i in indices_str.split(',') if i.strip()]

                        signals_to_add = [loaded_signals[available_keys[i]] for i in selected_indices if
                                          0 <= i < len(available_keys)]

                        if len(signals_to_add) < 1:
                            print(
                                "Please select at least one signal. If only one is selected, it will be returned unchanged.")
                            continue

                        result_signal = add_signals(signals_to_add)
                        print("\nSignal Addition complete.")

                        # Display the result
                        plot_mode = input("Display result as 'discrete' (d) or 'continuous' (c)? ").strip().lower()
                        if plot_mode in ['d', 'discrete']:
                            plot_signal([result_signal], 'discrete')
                        elif plot_mode in ['c', 'continuous']:
                            plot_signal([result_signal], 'continuous')
                        else:
                            print("Invalid display mode. Addition successful, but not plotted.")

                        # Optionally save the result signal to the loaded signals list
                        save_choice = input("Do you want to save the resulting signal? (y/n): ").strip().lower()
                        if save_choice == 'y':
                            # Create a dynamic key based on file names
                            base_names = [s.filename.split('.')[0] for s in signals_to_add]
                            result_key = f"{'_'.join(base_names)}_Sum.txt"
                            loaded_signals[result_key] = result_signal
                            print(f"Result saved as '{result_key}'.")

                    except ValueError:
                        print("Invalid input format for signal selection.")

                elif op_choice == 'm':
                    # Multiplication by Constant
                    index_str = input("Enter the number of the signal to multiply: ").strip()
                    const_str = input("Enter the constant value (e.g., 5.0 or -1): ").strip()

                    try:
                        signal_index = int(index_str) - 1
                        constant = float(const_str)

                        if 0 <= signal_index < len(available_keys):
                            original_signal = loaded_signals[available_keys[signal_index]]

                            result_signal = multiply_signal_by_constant(original_signal, constant)
                            print("\nMultiplication complete.")

                            # Display the result (alongside the original for comparison)
                            print("Displaying original and resulting signal for comparison.")
                            plot_mode = input("Display result as 'discrete' (d) or 'continuous' (c)? ").strip().lower()

                            signals_to_plot = [original_signal, result_signal]

                            if plot_mode in ['d', 'discrete']:
                                plot_signal(signals_to_plot, 'discrete')
                            elif plot_mode in ['c', 'continuous']:
                                plot_signal(signals_to_plot, 'continuous')
                            else:
                                print("Invalid display mode. Multiplication successful, but not plotted.")

                            # Optionally save the result signal
                            save_choice = input("Do you want to save the resulting signal? (y/n): ").strip().lower()
                            if save_choice == 'y':
                                original_name = original_signal.filename.split('.')[0]
                                result_key = f"{original_name}_Mult_{constant}.txt"
                                loaded_signals[result_key] = result_signal
                                print(f"Result saved as '{result_key}'.")

                        else:
                            print("Invalid signal number selected.")

                    except ValueError:
                        print("Invalid input for signal number or constant value.")

                else:
                    print("Invalid operation choice.")

        elif choice == '4':
            print("\nRunning Arithmetic Test Cases based on provided output files...")

            # --- Addition Tests ---
            print("\n--- Running Addition Tests ---")
            addition_tests = [
                ("Signal1.txt", "Signal2.txt"),
                ("Signal1.txt", "signal3.txt")
            ]

            for file1_key, file2_key in addition_tests:
                if file1_key in loaded_signals and file2_key in loaded_signals:
                    s1 = loaded_signals[file1_key]
                    s2 = loaded_signals[file2_key]

                    # Core logic for addition with alignment

                    # 1. Determine the overall common index range across ALL signals
                    all_indices = np.concatenate([s1.indices, s2.indices])
                    min_idx = np.min(all_indices)
                    max_idx = np.max(all_indices)
                    common_indices = np.arange(min_idx, max_idx + 1)

                    # Initialize the result array with zeros
                    total_samples = np.zeros(len(common_indices), dtype=float)

                    # Create maps
                    map1 = dict(zip(s1.indices, s1.samples))
                    map2 = dict(zip(s2.indices, s2.samples))

                    # Add samples
                    for i, idx in enumerate(common_indices):
                        total_samples[i] = map1.get(idx, 0.0) + map2.get(idx, 0.0)

                    # Call the test function from Task1Test.py
                    AddSignalSamplesAreEqual(file1_key, file2_key, common_indices, total_samples)
                else:
                    print(f"Skipping Addition Test: Required signals '{file1_key}' or '{file2_key}' not loaded.")

            # --- Multiplication Tests ---
            print("\n--- Running Multiplication Tests ---")
            multiplication_tests = [
                ("Signal1.txt", 5.0),  # Corresponds to MultiplySignalByConstant-Signal1 - by 5.txt
                ("Signal2.txt", 10.0)  # Corresponds to MultiplySignalByConstant-signal2 - by 10.txt
            ]

            for file_key, constant in multiplication_tests:
                if file_key in loaded_signals:
                    s = loaded_signals[file_key]
                    # Core logic for multiplication
                    result_samples = s.samples * constant

                    # Call the test function from Task1Test.py, passing the signal name
                    MultiplySignalByConst(file_key, constant, s.indices, result_samples)
                else:
                    print(f"Skipping Multiplication Test: Required signal '{file_key}' not loaded.")


        elif choice == '5':
            print("Exiting Signal Processing Framework. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    # Ensure matplotlib is set to interactive mode for plotting in certain environments
    plt.ion()
    try:
        main()
    except Exception as e:
        print(f"A fatal error occurred: {e}")
    finally:
        plt.ioff()  # Turn off interactive mode before exiting
