import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
from typing import Dict, List, Tuple, Any
import Task1Test as t
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
        """Setup the control panel with buttons and dropdowns"""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
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
                  command=self.graph_signal).grid(row=2, column=0, columnspan=2, 
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
        ttk.Button(button_frame, text="Multiply Signals", 
                  command=self.multiply_signals).grid(row=0, column=1, padx=5)
        
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
                  command=self.graph_result).grid(row=13, column=0, columnspan=2, 
                                                 sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(control_frame, text="Save Result",
                  command=self.save_result).grid(row=14, column=0, columnspan=2, 
                                                sticky=(tk.W, tk.E), pady=5)
        
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
            
            result_samples, result_indices = t.multiply_signales(
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
    
    def update_results_combo(self):
        """Update the results combo box"""
        result_names = list(self.results.keys())
        self.results_combo['values'] = result_names
        if result_names:
            self.results_var.set(result_names[-1])  # Select the latest result
    
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
                    f.write("0\n")  # First line
                    f.write("0\n")  # Second line
                    f.write(f"{len(indices)}\n")  # Third line - number of samples
                    for i, (idx, sample) in enumerate(zip(indices, samples)):
                        f.write(f"{idx} {sample}\n")
                
                messagebox.showinfo("Success", f"Result saved to: {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save result: {str(e)}")

def main():
    root = tk.Tk()
    app = SignalProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
