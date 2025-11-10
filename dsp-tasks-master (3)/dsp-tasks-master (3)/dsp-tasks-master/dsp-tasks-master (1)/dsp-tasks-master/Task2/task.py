import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
from typing import Dict, List, Tuple, Any
import Task1Test as t
import Task2Test as t2

class SignalProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processing GUI")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        self.signals = {}
        self.results = {}
        self.current_signal = None

        self.setup_gui()
        self.load_default_signals()

    def setup_gui(self):
        """Setup the main GUI layout"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        title_label = ttk.Label(main_frame, text="Signal Processing Application",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        self.setup_control_panel(main_frame)

        self.setup_plot_panel(main_frame)

    def setup_control_panel(self, parent):
        outer_frame = ttk.Frame(parent)
        outer_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        outer_frame.grid_rowconfigure(0, weight=1)
        outer_frame.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(outer_frame)
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.grid(row=0, column=0, sticky="nsew")

        control_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=control_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        control_frame.bind("<Configure>", on_configure)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        ttk.Label(control_frame, text="Select Signal:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.signal_var = tk.StringVar()
        self.signal_combo = ttk.Combobox(control_frame, textvariable=self.signal_var,
                                         state="readonly", width=20)
        self.signal_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        self.signal_combo.bind('<<ComboboxSelected>>', self.on_signal_selected)

        ttk.Button(control_frame, text="Load Custom Signal",
                   command=self.load_custom_signal).grid(row=1, column=0, columnspan=2,
                                                         sticky=(tk.W, tk.E), pady=5)

        ttk.Button(control_frame, text="Graph Selected Signal",
                   command=self.graph_signal).grid(row=2, column=0, columnspan=1,
                                                   sticky=(tk.W, tk.E), pady=5)

        ttk.Button(control_frame, text="Graph Selected Signal(Discrete)",
                   command=self.graph_signal_discrete).grid(row=2, column=1, columnspan=2,
                                                   sticky=(tk.W, tk.E), pady=5)

        ttk.Separator(control_frame, orient='horizontal').grid(row=3, column=0, columnspan=2,
                                                               sticky=(tk.W, tk.E), pady=10)

        ttk.Label(control_frame, text="Arithmetic Operations:",
                  font=('Arial', 10, 'bold')).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)

        ttk.Label(control_frame, text="Signal 1:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.signal1_var = tk.StringVar()
        self.signal1_combo = ttk.Combobox(control_frame, textvariable=self.signal1_var,
                                          state="readonly", width=15)
        self.signal1_combo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(control_frame, text="Signal 2:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.signal2_var = tk.StringVar()
        self.signal2_combo = ttk.Combobox(control_frame, textvariable=self.signal2_var,
                                          state="readonly", width=15)
        self.signal2_combo.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=2)

        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Signals",
                   command=self.add_signals).grid(row=0, column=0, padx=5)

        ttk.Button(button_frame, text="Sub Signals",
                   command=self.sub_signals).grid(row=0, column=2, padx=5)

        ttk.Button(button_frame, text="Multiply Signals",
                   command=self.multiply_signals).grid(row=0, column=1, padx=5)

        ttk.Button(button_frame, text="Square Signals",
                   command=self.square_signals).grid(row=1, column=1, padx=5)

        ttk.Button(button_frame, text="Accumulate Signal",
                   command=self.accumulate_signal).grid(row=1, column=0, padx=5)

        ttk.Label(control_frame, text="Multiply by Constant:").grid(row=8, column=0, sticky=tk.W, pady=5)
        constant_frame = ttk.Frame(control_frame)
        constant_frame.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.constant_var = tk.StringVar(value="1")
        ttk.Entry(constant_frame, textvariable=self.constant_var, width=10).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(constant_frame, text="Multiply",
                   command=self.multiply_by_constant).grid(row=0, column=1)

        ttk.Separator(control_frame, orient='horizontal').grid(row=10, column=0, columnspan=2,
                                                               sticky=(tk.W, tk.E), pady=10)

        ttk.Label(control_frame, text="Results:",
                  font=('Arial', 10, 'bold')).grid(row=11, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.results_var = tk.StringVar()
        self.results_combo = ttk.Combobox(control_frame, textvariable=self.results_var,
                                          state="readonly", width=20)
        self.results_combo.grid(row=12, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.results_combo.bind('<<ComboboxSelected>>', self.on_result_selected)

        ttk.Button(control_frame, text="Graph Result",
                   command=self.graph_result).grid(row=13, column=0, columnspan=1,
                                                   sticky=(tk.W, tk.E), pady=5)

        ttk.Button(control_frame, text="Graph Result (Discrete)",
                   command=self.graph_result_discrete).grid(row=13, column=1, columnspan=2,
                                                   sticky=(tk.W, tk.E), pady=5)

        ttk.Button(control_frame, text="Save Result",
                   command=self.save_result).grid(row=14, column=0, columnspan=1,
                                                  sticky=(tk.W, tk.E), pady=5)
        ttk.Button(control_frame, text="Test Result",
                   command=self.test_result).grid(row=14, column=1, columnspan=1,
                                                  sticky=(tk.W, tk.E), pady=5)

        ttk.Separator(control_frame, orient='horizontal').grid(row=15, column=0, columnspan=2,
                                                               sticky=(tk.W, tk.E), pady=10)
        ttk.Label(control_frame, text="Normalization:",
                  font=('Arial', 10, 'bold')).grid(row=15, column=0, columnspan=2, sticky=tk.W, pady=5)

        ttk.Button(control_frame, text="from 0 to 1",
                   command=self.normalize0).grid(row=16, column=0)

        ttk.Button(control_frame, text="from -1 to 1",
                   command=self.normalize1).grid(row=16, column=1)

        ttk.Separator(control_frame, orient='horizontal').grid(row=20, column=0, columnspan=2,
                                                               sticky=(tk.W, tk.E), pady=10)
        ttk.Label(control_frame, text="Generate Wave:",
                  font=('Arial', 10, 'bold')).grid(row=20, column=0, columnspan=2, pady=5)

        self.wave_type = tk.StringVar(value="sin")

        ttk.Radiobutton(control_frame, text="Sine", variable=self.wave_type, value="sin").grid(row=21, column=0,
                                                                                               sticky=tk.W)
        ttk.Radiobutton(control_frame, text="Cosine", variable=self.wave_type, value="cos").grid(row=21, column=1,
                                                                                                 sticky=tk.W)
        ttk.Label(control_frame, text="Amplitude:").grid(row=22, column=0, sticky=tk.W)
        self.amp_entry = ttk.Entry(control_frame, width=8)
        self.amp_entry.grid(row=22, column=1)

        ttk.Label(control_frame, text="Phase (radians):").grid(row=23, column=0, sticky=tk.W)
        self.phase_entry = ttk.Entry(control_frame, width=8)
        self.phase_entry.grid(row=23, column=1)

        ttk.Label(control_frame, text="Analog Freq (Hz):").grid(row=24, column=0, sticky=tk.W)
        self.freq_entry = ttk.Entry(control_frame, width=8)
        self.freq_entry.grid(row=24, column=1)

        ttk.Label(control_frame, text="Sampling Freq (Hz):").grid(row=25, column=0, sticky=tk.W)
        self.fs_entry = ttk.Entry(control_frame, width=8)
        self.fs_entry.grid(row=25, column=1)

        ttk.Button(control_frame, text="Generate Signal",
                   command=self.generate_wave).grid(row=26, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

    def setup_plot_panel(self, parent):
        """Setup the plotting panel"""
        plot_frame = ttk.LabelFrame(parent, text="Signal Plot", padding="10")
        plot_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_title("Signal Visualization")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_default_signals(self):
        """Load the default signals from the signals directory"""
        signals_dir = "signals"
        signal_files = ["Signal1.txt", "Signal2.txt", "signal3.txt"]

        for signal_file in signal_files:
            file_path = os.path.join(signals_dir, signal_file)
            if os.path.exists(file_path):
                try:
                    original_dir = os.getcwd()
                    os.chdir(signals_dir)
                    indices, samples = t.ReadSignalFile(signal_file)
                    os.chdir(original_dir)

                    signal_name = signal_file.replace('.txt', '')
                    self.signals[signal_name] = {
                        'indices': indices,
                        'samples': samples,
                        'file': signal_file
                    }
                except Exception as e:
                    if 'original_dir' in locals():
                        os.chdir(original_dir)
                    messagebox.showerror("Error", f"Failed to load {signal_file}: {str(e)}")

        self.update_signal_combos()

    def load_custom_signal(self):
        """Load a custom signal file"""
        file_path = filedialog.askopenfilename(
            title="Select Signal File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                filename = os.path.basename(file_path)
                file_dir = os.path.dirname(file_path)

                original_dir = os.getcwd()
                os.chdir(file_dir)
                indices, samples = t.ReadSignalFile(filename)
                os.chdir(original_dir)

                signal_name = filename.replace('.txt', '')
                self.signals[signal_name] = {
                    'indices': indices,
                    'samples': samples,
                    'file': filename
                }
                self.update_signal_combos()
                messagebox.showinfo("Success", f"Loaded signal: {signal_name}")
            except Exception as e:
                if 'original_dir' in locals():
                    os.chdir(original_dir)
                messagebox.showerror("Error", f"Failed to load signal: {str(e)}")

    def update_signal_combos(self):
        """Update the signal selection combo boxes"""
        signal_names = list(self.signals.keys())
        self.signal_combo['values'] = signal_names
        self.signal1_combo['values'] = signal_names
        self.signal2_combo['values'] = signal_names

        if signal_names:
            self.signal_var.set(signal_names[0])
            self.signal1_var.set(signal_names[0])
            if len(signal_names) > 1:
                self.signal2_var.set(signal_names[1])
            else:
                self.signal2_var.set(signal_names[0])

    def on_signal_selected(self, event=None):
        """Handle signal selection"""
        signal_name = self.signal_var.get()
        if signal_name in self.signals:
            self.current_signal = signal_name

    def graph_signal(self):
        """Graph the selected signal"""
        signal_name = self.signal_var.get()
        if not signal_name or signal_name not in self.signals:
            messagebox.showwarning("Warning", "Please select a signal to graph")
            return

        signal_data = self.signals[signal_name]
        indices = signal_data['indices']
        samples = signal_data['samples']

        self.ax.clear()
        self.ax.plot(indices, samples, 'b-', linewidth=1.5, label=signal_name)
        self.ax.set_title(f"Signal: {signal_name}")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()

        self.canvas.draw()

    def graph_signal_discrete(self):
        signal_name = self.signal_var.get()
        if not signal_name or signal_name not in self.signals:
            messagebox.showwarning("Warning", "Please select a signal to graph")
            return

        signal_data = self.signals[signal_name]
        indices = signal_data['indices']
        samples = signal_data['samples']

        self.ax.clear()
        (markerline, stemlines, baseline) = self.ax.stem(indices, samples, linefmt='b-', markerfmt='bo', basefmt='k-')
        plt.setp(markerline, markersize=4)
        plt.setp(stemlines, linewidth=1)
        plt.setp(baseline, linewidth=0.5, color='gray')

        self.ax.set_title(f"Signal: {signal_name} (Discrete)")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend([signal_name])

        self.canvas.draw()

    def add_signals(self):
        """Add two selected signals"""
        signal1_name = self.signal1_var.get()
        signal2_name = self.signal2_var.get()

        if not signal1_name or not signal2_name:
            messagebox.showwarning("Warning", "Please select both signals")
            return

        if signal1_name not in self.signals or signal2_name not in self.signals:
            messagebox.showerror("Error", "Selected signals not found")
            return

        try:
            signal1_data = self.signals[signal1_name]
            signal2_data = self.signals[signal2_name]

            result_samples, result_indices = t.add_signales(
                signal1_data['indices'], signal1_data['samples'],
                signal2_data['indices'], signal2_data['samples']
            )

            result_name = f"{signal1_name} + {signal2_name}"
            self.results[result_name] = {
                'indices': result_indices,
                'samples': result_samples
            }

            self.update_results_combo()
            messagebox.showinfo("Success", f"Added signals: {result_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add signals: {str(e)}")

    def sub_signals(self):
        """Add two selected signals"""
        signal1_name = self.signal1_var.get()
        signal2_name = self.signal2_var.get()

        if not signal1_name or not signal2_name:
            messagebox.showwarning("Warning", "Please select both signals")
            return

        if signal1_name not in self.signals or signal2_name not in self.signals:
            messagebox.showerror("Error", "Selected signals not found")
            return

        try:
            signal1_data = self.signals[signal1_name]
            signal2_data = self.signals[signal2_name]

            result_samples, result_indices = t.sub_signales(
                signal1_data['indices'], signal1_data['samples'],
                signal2_data['indices'], signal2_data['samples']
            )

            result_name = f"{signal1_name} - {signal2_name}"
            self.results[result_name] = {
                'indices': result_indices,
                'samples': result_samples
            }

            self.update_results_combo()
            messagebox.showinfo("Success", f"Added signals: {result_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add signals: {str(e)}")

    def multiply_signals(self):
        """Multiply two selected signals"""
        signal1_name = self.signal1_var.get()
        signal2_name = self.signal2_var.get()

        if not signal1_name or not signal2_name:
            messagebox.showwarning("Warning", "Please select both signals")
            return

        if signal1_name not in self.signals or signal2_name not in self.signals:
            messagebox.showerror("Error", "Selected signals not found")
            return

        try:
            signal1_data = self.signals[signal1_name]
            signal2_data = self.signals[signal2_name]

            result_samples, result_indices = t.multiply_signales(
                signal1_data['indices'], signal1_data['samples'],
                signal2_data['indices'], signal2_data['samples']
            )

            result_name = f"{signal1_name} × {signal2_name}"
            self.results[result_name] = {
                'indices': result_indices,
                'samples': result_samples
            }

            self.update_results_combo()
            messagebox.showinfo("Success", f"Multiplied signals: {result_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to multiply signals: {str(e)}")

    def multiply_by_constant(self):
        """Multiply selected signal by a constant"""
        signal1_name = self.signal1_var.get()
        constant_str = self.constant_var.get()

        if not signal1_name:
            messagebox.showwarning("Warning", "Please select a signal")
            return

        if signal1_name not in self.signals:
            messagebox.showerror("Error", "Selected signal not found")
            return

        try:
            constant = float(constant_str)
            signal_data = self.signals[signal1_name]

            result_samples, result_indices = t.multiply_signales_constant(
                signal_data['indices'], signal_data['samples'], constant
            )

            result_name = f"{signal1_name} × {constant}"
            self.results[result_name] = {
                'indices': result_indices,
                'samples': result_samples
            }

            self.update_results_combo()
            messagebox.showinfo("Success", f"Multiplied signal by constant: {result_name}")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the constant")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to multiply by constant: {str(e)}")

    def square_signals(self):
        signal1_name = self.signal1_var.get()
        constant_str = self.constant_var.get()

        if not signal1_name:
            messagebox.showwarning("Warning", "Please select a signal")
            return

        if signal1_name not in self.signals:
            messagebox.showerror("Error", "Selected signal not found")
            return

        try:
            constant = float(constant_str)
            signal_data = self.signals[signal1_name]

            result_samples, result_indices = t.square_signales(
                signal_data['indices'], signal_data['samples']
            )

            result_name = f"{signal1_name} ^ 2"
            self.results[result_name] = {
                'indices': result_indices,
                'samples': result_samples
            }

            self.update_results_combo()
            messagebox.showinfo("Success", f"Squared a signal: {result_name}")

        except ValueError:
            messagebox.showerror("Error", "")
        except Exception as e:
            messagebox.showerror("Error", f" {str(e)}")

    def accumulate_signal(self):
        signal_name = self.signal_var.get()

        if not signal_name or signal_name not in self.signals:
            messagebox.showwarning("Warning", "Please select a signal to accumulate")
            return
        try:
            signal_data = self.signals[signal_name]
            indices = signal_data['indices']
            samples = signal_data['samples']

            new_indices, accumulated_samples = t.accumulate_signals(indices, samples)

            result_name = f"Accumulated({signal_name})"
            self.results[result_name] = {
                'indices': new_indices,
                'samples': accumulated_samples
            }
            self.update_results_combo()
            messagebox.showinfo("Success", f"Accumulated signal saved as '{result_name}'")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to accumulate signal: {str(e)}")

    def normalize0(self):
        """Normalize selected signal to range [0, 1]"""
        signal1_name = self.signal1_var.get()

        if not signal1_name:
            messagebox.showwarning("Warning", "Please select a signal to normalize")
            return

        if signal1_name not in self.signals:
            messagebox.showerror("Error", "Selected signal not found")
            return

        try:
            signal_data = self.signals[signal1_name]

            normalized_samples, normalized_indices = t.normalize_zero_to_one(
                signal_data['indices'], signal_data['samples']
            )

            result_name = f"{signal1_name} (Normalized 0–1)"
            self.results[result_name] = {
                'indices': normalized_indices,
                'samples': normalized_samples
            }

            self.update_results_combo()
            messagebox.showinfo("Success", f"Normalized signal: {result_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to normalize signal: {str(e)}")

    def normalize1(self):
        signal1_name = self.signal1_var.get()

        if not signal1_name:
            messagebox.showwarning("Warning", "Please select a signal to normalize")
            return

        if signal1_name not in self.signals:
            messagebox.showerror("Error", "Selected signal not found")
            return

        try:
            signal_data = self.signals[signal1_name]

            normalized_samples, normalized_indices = t.normalize_minus_to_one(
                signal_data['indices'], signal_data['samples']
            )

            result_name = f"{signal1_name} (Normalized -1 –> 1)"
            self.results[result_name] = {
                'indices': normalized_indices,
                'samples': normalized_samples
            }

            self.update_results_combo()
            messagebox.showinfo("Success", f"Normalized signal: {result_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to normalize signal: {str(e)}")

    def generate_wave(self):
        try:
            A = float(self.amp_entry.get())
            phi = float(self.phase_entry.get())
            f = float(self.freq_entry.get())
            fs = float(self.fs_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
            return

        if fs <= 0 or f <= 0:
            messagebox.showerror("Invalid Values", "Frequencies must be positive.")
            return
        if fs < 2*f:
            messagebox.showerror("Invalid Values", "Fs must be at least 2F.")
            return

        n = np.arange(0, fs)
        if self.wave_type.get() == "sin":
            samples = A * np.sin(2 * np.pi * f * n / fs + phi)
            wave_name = f"Sine_{f}Hz"
        else:
            samples = A * np.cos(2 * np.pi * f * n / fs + phi)
            wave_name = f"Cosine_{f}Hz"

        indices = list(n)
        samples = list(samples)

        self.results[wave_name] = {'indices': indices, 'samples': samples}
        self.update_results_combo()

        messagebox.showinfo("Success", f"{self.wave_type.get().capitalize()} wave generated: {wave_name}")

    def update_results_combo(self):
        """Update the results combo box"""
        result_names = list(self.results.keys())
        self.results_combo['values'] = result_names
        if result_names:
            self.results_var.set(result_names[-1])

    def on_result_selected(self, event=None):
        """Handle result selection"""
        pass  # Could add functionality here if needed

    def graph_result(self):
        """Graph the selected result"""
        result_name = self.results_var.get()
        if not result_name or result_name not in self.results:
            messagebox.showwarning("Warning", "Please select a result to graph")
            return

        result_data = self.results[result_name]
        indices = result_data['indices']
        samples = result_data['samples']

        self.ax.clear()
        self.ax.plot(indices, samples, 'r-', linewidth=1.5, label=result_name)
        self.ax.set_title(f"Result: {result_name}")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()

        self.canvas.draw()

    def graph_result_discrete(self):
        result_name = self.results_var.get()
        if not result_name or result_name not in self.results:
            messagebox.showwarning("Warning", "Please select a result to graph")
            return

        result_data = self.results[result_name]
        indices = result_data['indices']
        samples = result_data['samples']

        step = max(1, len(indices) // 720)
        indices_ds = indices[::step]
        samples_ds = samples[::step]

        self.ax.clear()

        (markerline, stemlines, baseline) = self.ax.stem(indices_ds, samples_ds, linefmt='r-', markerfmt='ro', basefmt='k-')

        plt.setp(markerline, markersize=4)
        plt.setp(stemlines, linewidth=1)
        plt.setp(baseline, linewidth=0.5, color='gray')

        self.ax.set_title(f"Result (Discrete): {result_name}")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend([result_name])

        self.canvas.draw()

    def save_result(self):
        """Save the selected result to a file"""
        result_name = self.results_var.get()
        if not result_name or result_name not in self.results:
            messagebox.showwarning("Warning", "Please select a result to save")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Result",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                result_data = self.results[result_name]
                indices = result_data['indices']
                samples = result_data['samples']

                with open(file_path, 'w') as f:
                    f.write("0\n")
                    f.write("0\n")
                    f.write(f"{len(indices)}\n")
                    for i, (idx, sample) in enumerate(zip(indices, samples)):
                        f.write(f"{int(idx)} {sample}\n")

                messagebox.showinfo("Success", f"Result saved to: {file_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save result: {str(e)}")

    def test_result(self):
        """Run validation test on the selected result"""
        result_name = self.results_var.get()
        if not result_name or result_name not in self.results:
            messagebox.showwarning("Warning", "Please select a result to test")
            return
        # Ask user for the expected (reference) output file
        expected_file = filedialog.askopenfilename(
            title="Select Expected Output File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not expected_file:
            return
        result_data = self.results[result_name]
        indices = result_data['indices']
        samples = result_data['samples']
        try:

            #from Task1Test import SignalSamplesAreEqual

            task_name = result_name.upper() + " Test"

            t2.SignalSamplesAreEqual(task_name, expected_file, indices, samples)
            messagebox.showinfo("Test Completed", f"{task_name} test completed. Check console for results.")
        except Exception as e:
            messagebox.showerror("Error", f"Testing failed: {str(e)}")


def main():
    root = tk.Tk()
    app = SignalProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
