# Signal Processing GUI

A user-friendly graphical interface for signal processing operations including signal visualization, addition, and multiplication.

## Features

- **Signal Loading**: Load default signals (Signal1.txt, Signal2.txt, signal3.txt) or custom signal files
- **Signal Visualization**: Graph any loaded signal with matplotlib
- **Signal Addition**: Add two signals together
- **Signal Multiplication**: Multiply two signals or multiply a signal by a constant
- **Result Management**: View and save operation results
- **Interactive Interface**: Easy-to-use dropdown menus and buttons

## Installation

1. Make sure you have Python 3.7+ installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python run_gui.py
```

Or directly:
```bash
python signal_gui.py
```

### Using the Interface

1. **Select a Signal**: Use the "Select Signal" dropdown to choose from loaded signals
2. **Graph Signal**: Click "Graph Selected Signal" to visualize the signal
3. **Load Custom Signal**: Click "Load Custom Signal" to load your own signal files
4. **Arithmetic Operations**:
   - Select two signals from the Signal 1 and Signal 2 dropdowns
   - Click "Add Signals" or "Multiply Signals" to perform operations
   - For constant multiplication, enter a number and click "Multiply"
5. **View Results**: Select results from the "Results" dropdown and click "Graph Result"
6. **Save Results**: Click "Save Result" to save the current result to a file

### Signal File Format

Signal files should follow this format:
```
0
0
1001
0 0
1 1
2 2
...
```

Where:
- Line 1: Usually 0
- Line 2: Usually 0  
- Line 3: Number of data points
- Subsequent lines: Index and amplitude values separated by space

## File Structure

- `signal_gui.py`: Main GUI application
- `run_gui.py`: Simple launcher script
- `requirements.txt`: Python dependencies
- `signals/`: Directory containing signal files
- `Task1Test.py`: Signal processing functions (existing)

## Dependencies

- `tkinter`: GUI framework (usually included with Python)
- `matplotlib`: For signal plotting
- `numpy`: For numerical operations

## Troubleshooting

- **Import Error**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **Signal Loading Error**: Check that signal files are in the correct format
- **File Not Found**: Ensure signal files are in the `signals/` directory or use "Load Custom Signal"

## Example Operations

1. Load Signal1 and Signal2
2. Graph Signal1 to see the signal
3. Add Signal1 + Signal2
4. Graph the result to see the sum
5. Multiply Signal1 by constant 5
6. Save the result to a file
