#!/usr/bin/env python3
"""
Demo script showing how to use the new Task 4 Operations tab
"""

import os
import sys
import numpy as np

def create_demo_signal():
    """Create a demo signal for testing Task 4 operations"""
    print("Creating demo signal...")
    
    # Create a simple test signal: sine wave + DC component
    N = 8
    fs = 100  # Sampling frequency
    t = np.arange(N) / fs
    
    # Signal: 2*sin(2*pi*10*t) + 5 (DC component)
    signal = 2 * np.sin(2 * np.pi * 10 * t) + 5
    
    # Save to file in Task 4 input format
    filename = "task4/input/demo_signal.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        f.write("0\n")  # First line
        f.write("0\n")  # Second line
        f.write(f"{N}\n")  # Number of samples
        for i, val in enumerate(signal):
            f.write(f"{i} {val:.6f}\n")
    
    print(f"✓ Demo signal saved to: {filename}")
    print(f"  Signal: {signal}")
    return filename

def demonstrate_operations():
    """Demonstrate the Task 4 operations workflow"""
    print("\n" + "="*60)
    print("TASK 4 OPERATIONS DEMONSTRATION")
    print("="*60)
    
    print("\n1. CREATED DEMO SIGNAL")
    print("   - Signal: 2*sin(2*pi*10*t) + 5")
    print("   - 8 samples, DC component = 5")
    print("   - Saved to: task4/input/demo_signal.txt")
    
    print("\n2. AVAILABLE OPERATIONS IN THE NEW TAB:")
    print("   📊 DFT - Discrete Fourier Transform")
    print("   🔄 IDFT - Inverse Discrete Fourier Transform") 
    print("   🔧 Remove DC Component")
    print("   📈 Modify Amplitude")
    print("   📐 Modify Phase")
    print("   🎯 Show Dominant Frequencies")
    
    print("\n3. WORKFLOW:")
    print("   Step 1: Load signal file using 'Load Signal File' button")
    print("   Step 2: Select operation from dropdown menu")
    print("   Step 3: Set parameters (sampling frequency, etc.)")
    print("   Step 4: Click 'Execute Operation'")
    print("   Step 5: View results in plot and text area")
    print("   Step 6: Enter result name and click 'Save Result'")
    print("   Step 7: Switch to 'Task 4 Testing' tab to test your results")
    
    print("\n4. EXAMPLE WORKFLOW:")
    print("   a) Load demo_signal.txt")
    print("   b) Select 'DFT' operation")
    print("   c) Set sampling frequency to 100 Hz")
    print("   d) Execute → See frequency domain plot")
    print("   e) Save as 'demo_DFT_result.txt'")
    print("   f) Select 'Remove DC Component'")
    print("   g) Execute → See DC-removed signal")
    print("   h) Save as 'demo_DC_removed.txt'")
    print("   i) Switch to Testing tab to verify results")
    
    print("\n5. SAVE FORMATS:")
    print("   📁 DFT Results: Amplitude and Phase pairs")
    print("   📁 IDFT Results: Reconstructed signal samples")
    print("   📁 DC Removal: Signal with DC component removed")
    print("   📁 All formats compatible with Task 4 testing functions")

def show_file_structure():
    """Show the expected file structure"""
    print("\n" + "="*60)
    print("FILE STRUCTURE")
    print("="*60)
    
    print("\ntask4/")
    print("├── input/")
    print("│   ├── demo_signal.txt          ← Your input signals")
    print("│   ├── input_Signal_DFT.txt     ← Original test files")
    print("│   └── ...")
    print("├── output/")
    print("│   ├── demo_DFT_result.txt       ← Your DFT results")
    print("│   ├── demo_DC_removed.txt       ← Your DC removal results")
    print("│   └── ...")
    print("├── dftCompare/")
    print("│   └── signalcompare.py          ← Testing functions")
    print("└── dc_compare/")
    print("    └── CompareSignals.py         ← Testing functions")

def main():
    """Main demonstration function"""
    print("Task 4 Operations Tab - Demonstration")
    
    # Create demo signal
    demo_file = create_demo_signal()
    
    # Show demonstration
    demonstrate_operations()
    
    # Show file structure
    show_file_structure()
    
    print("\n" + "="*60)
    print("READY TO USE!")
    print("="*60)
    print("Run: python taskCode.py")
    print("Then switch to the 'Task 4 Operations' tab")
    print("Load the demo signal and try the operations!")

if __name__ == "__main__":
    main()
