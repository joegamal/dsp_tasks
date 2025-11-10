#!/usr/bin/env python3
"""
Test script to verify Task 4 testing functionality
"""

import os
import sys
import numpy as np

# Add task4 testing modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'task4', 'dftCompare'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'task4', 'dc_compare'))

def test_file_reading():
    """Test the file reading functionality"""
    print("Testing file reading functionality...")
    
    # Test reading DFT input file
    dft_input_path = os.path.join('task4', 'input', 'input_Signal_DFT.txt')
    if os.path.exists(dft_input_path):
        print(f"✓ Found DFT input file: {dft_input_path}")
        
        with open(dft_input_path, 'r') as f:
            lines = f.readlines()
            print(f"  File has {len(lines)} lines")
            print(f"  First few lines: {lines[:4]}")
    else:
        print(f"✗ DFT input file not found: {dft_input_path}")
    
    # Test reading DFT output file
    dft_output_path = os.path.join('task4', 'output', 'Output_Signal_DFT_A,Phase.txt')
    if os.path.exists(dft_output_path):
        print(f"✓ Found DFT output file: {dft_output_path}")
        
        with open(dft_output_path, 'r') as f:
            lines = f.readlines()
            print(f"  File has {len(lines)} lines")
            print(f"  First few lines: {lines[:4]}")
    else:
        print(f"✗ DFT output file not found: {dft_output_path}")

def test_dft_computation():
    """Test basic DFT computation"""
    print("\nTesting DFT computation...")
    
    # Simple test signal
    test_signal = [1, 2, 3, 4]
    N = len(test_signal)
    
    # Compute DFT manually
    X_result = []
    for k in range(N):
        real = 0
        imag = 0
        for n in range(N):
            angle = -2 * np.pi * k * n / N
            real += test_signal[n] * np.cos(angle)
            imag += test_signal[n] * np.sin(angle)
        X_result.append(complex(real, imag))
    
    amplitudes = [abs(x) for x in X_result]
    phases = [np.angle(x) for x in X_result]
    
    print(f"Test signal: {test_signal}")
    print(f"DFT amplitudes: {[f'{a:.3f}' for a in amplitudes]}")
    print(f"DFT phases: {[f'{p:.3f}' for p in phases]}")
    print("✓ DFT computation completed")

def test_module_imports():
    """Test importing Task 4 testing modules"""
    print("\nTesting module imports...")
    
    try:
        from signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift, RoundPhaseShift
        print("✓ Successfully imported signalcompare module")
        
        # Test amplitude comparison
        test_amp1 = [1.0, 2.0, 3.0]
        test_amp2 = [1.001, 2.0, 3.0]
        result = SignalComapreAmplitude(test_amp1, test_amp2)
        print(f"✓ Amplitude comparison test: {result}")
        
    except ImportError as e:
        print(f"✗ Failed to import signalcompare: {e}")
    
    try:
        from CompareSignals import SignalsAreEqual
        print("✓ Successfully imported CompareSignals module")
    except ImportError as e:
        print(f"✗ Failed to import CompareSignals: {e}")

def main():
    """Run all tests"""
    print("Task 4 Testing Functionality Verification")
    print("=" * 50)
    
    test_file_reading()
    test_dft_computation()
    test_module_imports()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()
