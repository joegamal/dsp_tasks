import argparse
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Tuple


def read_signal_file(file_path: str) -> Tuple[List[int], List[float]]:
	indices: List[int] = []
	samples: List[float] = []
	with open(file_path, 'r') as f:
		_ = f.readline()  # typically 0
		_ = f.readline()  # typically 0
		count_line = f.readline().strip()
		try:
			count = int(count_line)
		except ValueError:
			raise ValueError(f"Invalid samples count line: '{count_line}' in {file_path}")
		for _ in range(count):
			line = f.readline()
			if not line:
				break
			parts = line.strip().split()
			if len(parts) != 2:
				break
			idx = int(float(parts[0]))
			val = float(parts[1])
			indices.append(idx)
			samples.append(val)
	return indices, samples


def write_header(f, n: int) -> None:
	f.write("0\n")
	f.write("0\n")
	f.write(f"{n}\n")


def compute_levels_and_step(samples: List[float], levels: int | None, bits: int | None) -> Tuple[int, float, float, float]:
	if (levels is None) == (bits is None):
		raise ValueError("Specify exactly one of levels or bits")
	L = levels if levels is not None else (1 << bits)
	min_val = min(samples)
	max_val = max(samples)
	# Avoid zero range
	if max_val == min_val:
		max_val = min_val + 1.0
	delta = (max_val - min_val) / L
	return L, delta, min_val, max_val


def mid_rise_quantize(samples: List[float], L: int, delta: float, min_val: float) -> Tuple[List[int], List[str], List[float], List[float]]:
	# Returns (interval_indices_1based, encoded_bits, quantized_values, errors)
	bits = (L - 1).bit_length()
	interval_indices: List[int] = []
	encoded_bits: List[str] = []
	quantized_values: List[float] = []
	errors: List[float] = []
	for x in samples:
		k = int((x - min_val) // delta)
		if (x - min_val) < 0:
			k = -1
		if k < 0:
			k = 0
		elif k >= L:
			k = L - 1
		q = min_val + (k + 0.5) * delta
		e = q - x
		interval_indices.append(k + 1)
		encoded_bits.append(format(k, f"0{bits}b"))
		quantized_values.append(q)
		errors.append(e)
	return interval_indices, encoded_bits, quantized_values, errors


def write_simple_output(file_path: str, encoded: List[str], quantized: List[float]) -> None:
	with open(file_path, 'w') as f:
		write_header(f, len(encoded))
		for code, q in zip(encoded, quantized):
			f.write(f"{code} {q}\n")


def write_detailed_output(file_path: str, indices1: List[int], encoded: List[str], quantized: List[float], errors: List[float]) -> None:
	with open(file_path, 'w') as f:
		write_header(f, len(indices1))
		for idx, code, q, e in zip(indices1, encoded, quantized, errors):
			f.write(f"{idx} {code} {q:.3f} {e:.3f}\n")


def quantize_file(input_path: str, output_path: str, fmt: str, levels: int | None, bits: int | None) -> Tuple[List[int], List[str], List[float], List[float]]:
	_, samples = read_signal_file(input_path)
	L, delta, min_val, _ = compute_levels_and_step(samples, levels, bits)
	indices1, encoded, quantized, errors = mid_rise_quantize(samples, L, delta, min_val)
	if fmt == 'simple':
		write_simple_output(output_path, encoded, quantized)
	elif fmt == 'detailed':
		write_detailed_output(output_path, indices1, encoded, quantized, errors)
	else:
		raise ValueError("fmt must be 'simple' or 'detailed'")
	return indices1, encoded, quantized, errors


def run_test1(expected_file: str, encoded: List[str], quantized: List[float]) -> None:
	from QuanTest1 import QuantizationTest1
	QuantizationTest1(expected_file, encoded, quantized)


def run_test2(expected_file: str, indices1: List[int], encoded: List[str], quantized: List[float], errors: List[float]) -> None:
	from QuanTest2 import QuantizationTest2
	QuantizationTest2(expected_file, indices1, encoded, quantized, errors)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Uniform mid-rise quantization for signals")
	parser.add_argument('--input', required=True, help='Input signal file path')
	parser.add_argument('--output', required=True, help='Output file path')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--levels', type=int, help='Number of quantization levels L')
	group.add_argument('--bits', type=int, help='Number of bits (L = 2^bits)')
	parser.add_argument('--format', choices=['simple', 'detailed'], default='simple', help='Output format')
	parser.add_argument('--test1', help='Run QuantizationTest1 against expected file path')
	parser.add_argument('--test2', help='Run QuantizationTest2 against expected file path')
	return parser.parse_args()


def main() -> None:
	# If no CLI args provided, launch GUI
	if len(sys.argv) == 1:
		launch_gui()
		return
	args = parse_args()
	indices1, encoded, quantized, errors = quantize_file(
		args.input, args.output, args.format, args.levels, args.bits
	)
	if args.test1:
		run_test1(args.test1, encoded, quantized)
	if args.test2:
		run_test2(args.test2, indices1, encoded, quantized, errors)


class QuantizationGUI:
	def __init__(self, root: tk.Tk) -> None:
		self.root = root
		self.root.title("Task 3 - Signal Quantization")
		self.root.geometry("700x420")

		self.input_path_var = tk.StringVar()
		self.output_path_var = tk.StringVar()
		self.mode_var = tk.StringVar(value="bits")
		self.bits_var = tk.StringVar(value="3")
		self.levels_var = tk.StringVar(value="8")
		self.format_var = tk.StringVar(value="simple")

		self.last_indices1: List[int] = []
		self.last_encoded: List[str] = []
		self.last_quantized: List[float] = []
		self.last_errors: List[float] = []

		self._build()

	def _build(self) -> None:
		pad = {"padx": 8, "pady": 6}
		frm = ttk.Frame(self.root, padding=10)
		frm.pack(fill=tk.BOTH, expand=True)

		# Input selection
		row = 0
		ttk.Label(frm, text="Input file:").grid(row=row, column=0, sticky=tk.W, **pad)
		entry_in = ttk.Entry(frm, textvariable=self.input_path_var, width=60)
		entry_in.grid(row=row, column=1, sticky=tk.W, **pad)
		ttk.Button(frm, text="Browse", command=self._choose_input).grid(row=row, column=2, **pad)

		# Output selection
		row += 1
		ttk.Label(frm, text="Output file:").grid(row=row, column=0, sticky=tk.W, **pad)
		entry_out = ttk.Entry(frm, textvariable=self.output_path_var, width=60)
		entry_out.grid(row=row, column=1, sticky=tk.W, **pad)
		ttk.Button(frm, text="Browse", command=self._choose_output).grid(row=row, column=2, **pad)

		# Bits / Levels
		row += 1
		mfrm = ttk.LabelFrame(frm, text="Quantizer settings")
		mfrm.grid(row=row, column=0, columnspan=3, sticky="nsew", **pad)
		mfrm.columnconfigure(1, weight=1)

		bits_rb = ttk.Radiobutton(mfrm, text="Use bits", variable=self.mode_var, value="bits", command=self._update_state)
		bits_rb.grid(row=0, column=0, sticky=tk.W, **pad)
		self.bits_entry = ttk.Entry(mfrm, textvariable=self.bits_var, width=10)
		self.bits_entry.grid(row=0, column=1, sticky=tk.W, **pad)

		levels_rb = ttk.Radiobutton(mfrm, text="Use levels", variable=self.mode_var, value="levels", command=self._update_state)
		levels_rb.grid(row=1, column=0, sticky=tk.W, **pad)
		self.levels_entry = ttk.Entry(mfrm, textvariable=self.levels_var, width=10)
		self.levels_entry.grid(row=1, column=1, sticky=tk.W, **pad)

		# Output format
		row += 1
		ffrm = ttk.LabelFrame(frm, text="Output format")
		ffrm.grid(row=row, column=0, columnspan=3, sticky="nsew", **pad)
		ttk.Radiobutton(ffrm, text="Simple (Quan1)", variable=self.format_var, value="simple").grid(row=0, column=0, sticky=tk.W, **pad)
		ttk.Radiobutton(ffrm, text="Detailed (Quan2)", variable=self.format_var, value="detailed").grid(row=0, column=1, sticky=tk.W, **pad)

		# Actions
		row += 1
		btn_frm = ttk.Frame(frm)
		btn_frm.grid(row=row, column=0, columnspan=3, sticky=tk.W, **pad)
		ttk.Button(btn_frm, text="Quantize", command=self._quantize).grid(row=0, column=0, **pad)
		ttk.Button(btn_frm, text="Run Test1 (Quan1)", command=self._run_test1).grid(row=0, column=1, **pad)
		ttk.Button(btn_frm, text="Run Test2 (Quan2)", command=self._run_test2).grid(row=0, column=2, **pad)

		# Result preview (first few lines)
		row += 1
		preview = ttk.LabelFrame(frm, text="Preview (first lines)")
		preview.grid(row=row, column=0, columnspan=3, sticky="nsew", **pad)
		preview.columnconfigure(0, weight=1)
		self.preview_box = tk.Text(preview, height=20)
		self.preview_box.grid(row=0, column=0, sticky="nsew", **pad)

		self._update_state()

	def _choose_input(self) -> None:
		path = filedialog.askopenfilename(title="Select input signal", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
		if path:
			self.input_path_var.set(path)

	def _choose_output(self) -> None:
		path = filedialog.asksaveasfilename(title="Select output path", defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
		if path:
			self.output_path_var.set(path)

	def _update_state(self) -> None:
		use_bits = self.mode_var.get() == "bits"
		state_bits = "normal" if use_bits else "disabled"
		state_levels = "disabled" if use_bits else "normal"
		self.bits_entry.configure(state=state_bits)
		self.levels_entry.configure(state=state_levels)

	def _quantize(self) -> None:
		in_path = self.input_path_var.get().strip()
		out_path = self.output_path_var.get().strip()
		fmt = self.format_var.get()
		if not in_path:
			messagebox.showwarning("Missing input", "Please choose an input file")
			return
		if not out_path:
			messagebox.showwarning("Missing output", "Please choose an output file")
			return
		levels = None
		bits = None
		try:
			if self.mode_var.get() == "bits":
				bits = int(self.bits_var.get())
				if bits <= 0:
					raise ValueError
			else:
				levels = int(self.levels_var.get())
				if levels <= 1:
					raise ValueError
		except ValueError:
			messagebox.showerror("Invalid setting", "Please enter a valid positive integer for bits/levels")
			return
		try:
			self.last_indices1, self.last_encoded, self.last_quantized, self.last_errors = quantize_file(
				in_path, out_path, fmt, levels, bits
			)
			messagebox.showinfo("Done", f"Quantized output saved to:\n{out_path}")
			self._refresh_preview(out_path)
		except Exception as e:
			messagebox.showerror("Error", str(e))

	def _refresh_preview(self, path: str) -> None:
		try:
			with open(path, 'r') as f:
				lines = f.readlines()
			self.preview_box.configure(state="normal")
			self.preview_box.delete("1.0", tk.END)
			for line in lines[:10]:
				self.preview_box.insert(tk.END, line)
			self.preview_box.configure(state="disabled")
		except Exception:
			pass

	def _run_test1(self) -> None:
		if not self.last_encoded or not self.last_quantized:
			messagebox.showwarning("No data", "Please run quantization first (Simple format)")
			return
		expected = filedialog.askopenfilename(title="Select expected Quan1 output", filetypes=[("Text files", "*.txt")])
		if not expected:
			return
		try:
			run_test1(expected, self.last_encoded, self.last_quantized)
		except Exception as e:
			messagebox.showerror("Test1 Error", str(e))

	def _run_test2(self) -> None:
		if not self.last_indices1 or not self.last_errors:
			messagebox.showwarning("No data", "Please run quantization first (Detailed format)")
			return
		expected = filedialog.askopenfilename(title="Select expected Quan2 output", filetypes=[("Text files", "*.txt")])
		if not expected:
			return
		try:
			run_test2(expected, self.last_indices1, self.last_encoded, self.last_quantized, self.last_errors)
		except Exception as e:
			messagebox.showerror("Test2 Error", str(e))


def launch_gui() -> None:
	root = tk.Tk()
	QuantizationGUI(root)
	root.mainloop()


if __name__ == '__main__':
	main()


