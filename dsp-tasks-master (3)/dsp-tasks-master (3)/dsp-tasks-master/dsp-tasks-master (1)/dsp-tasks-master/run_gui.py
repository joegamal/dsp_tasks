#!/usr/bin/env python3
"""
Simple script to run the Signal Processing GUI
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from signal_gui import main
    
    if __name__ == "__main__":
        print("Starting Signal Processing GUI...")
        main()
        
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please make sure you have installed the required dependencies:")
    print("pip install matplotlib numpy")
    sys.exit(1)
except Exception as e:
    print(f"Error starting the application: {e}")
    sys.exit(1)
