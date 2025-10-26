#!/usr/bin/env python
# coding: utf-8
import numpy as np

from new.normalaization import signal_normalization
from new.sinusoidal import createSin
from new.subtraction import subtract_signals
from task_one.read_load_signals import get_signal_body

# In[ ]:

SIGNAL_DATA = {}
try:
    x1, y1 = get_signal_body("../signals/Signal1.txt")
    SIGNAL_DATA['1'] = (x1, y1)
    x2, y2 = get_signal_body("../signals/Signal2.txt")
    SIGNAL_DATA['2'] = (x2, y2)
    x3, y3 = get_signal_body("../signals/signal3.txt")
    SIGNAL_DATA['3'] = (x3, y3)
except FileNotFoundError as e:
    print(f"Error loading signal file: {e}. Ensure 'signals/Signal1.txt', 'signals/Signal2.txt', and 'signals/signal3.txt' exist.")
    # Use dummy data if files are missing to allow the GUI to start, though operations will fail
    dummy_x = np.array([0, 1, 2, 3])
    dummy_y = np.array([0, 1, 0, -1])
    if '1' not in SIGNAL_DATA: SIGNAL_DATA['1'] = (dummy_x, dummy_y)
    if '2' not in SIGNAL_DATA: SIGNAL_DATA['2'] = (dummy_x, dummy_y)
    if '3' not in SIGNAL_DATA: SIGNAL_DATA['3'] = (dummy_x, dummy_y)

def ReadSignalFile(file_name):
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    return expected_indices,expected_samples

# In[ ]:

def SinCosSignalSamplesAreEqual(user_choice,file_name,indices,samples):
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
                
    if len(expected_samples)!=len(samples):
        print(user_choice+" Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(expected_samples)):
        if abs(samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print(user_choice+" Test case failed, your signal have different values from the expected one") 
            return
    print(user_choice +" Test case passed successfully")

# In[ ]:

def SubSignalSamplesAreEqual(userFirstSignal,userSecondSignal,Your_indices,Your_samples):
    if(userFirstSignal=='Signal1.txt' and userSecondSignal=='Signal2.txt'):
        file_name= "../signals/signal1-signal2.txt"  # write here path of signal1-signal2
    elif(userFirstSignal=='Signal1.txt' and userSecondSignal=='Signal3.txt'):
        file_name= "../signals/signal1-signal3.txt"  # write here path of signal1-signal3
        
    expected_indices,expected_samples=ReadSignalFile(file_name)   
    
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Subtraction Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Subtraction Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Subtraction Test case failed, your signal have different values from the expected one") 
            return
    print("Subtraction Test case passed successfully")

# In[ ]:
def NormalizeSignal(MinRange,MaxRange,Your_indices,Your_samples):
    if(MinRange==-1 and MaxRange==1):
        file_name= "../signals/normalize of signal 1 (from -1 to 1)-- output.txt"  # write here path of normalize signal 1 output.txt
    elif(MinRange==0 and MaxRange==1):
        file_name= "../signals/normlize signal 2 (from 0 to 1 )-- output.txt"  # write here path of normalize signal 2 output.txt
        
    expected_indices,expected_samples=ReadSignalFile(file_name)      
    
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Normalization Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Normalization Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Normalization Test case failed, your signal have different values from the expected one") 
            return
    print("Normalization Test case passed successfully")

# In[ ]:


# use this twice one for Accumlation and one for Squaring
# Task name when call ACC or SQU


#TaskName => choose it (string explain the name of task like (adding,subtracting, .... etc.))
#output_file_name => output file path (given by TAs)
# Your_indices => your indices list from your code (generated/calculated by you)
# Your_samples => your samples list from your code (generated/calculated by you)
def SignalSamplesAreEqual(TaskName,output_file_name,Your_indices,Your_samples):
    expected_indices=[]
    expected_samples=[]
    with open(output_file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print(TaskName+" Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print(TaskName+" Test case failed, your signal have different indicies from the expected one") 
            return             
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print(TaskName+" Test case failed, your signal have different values from the expected one") 
            return
    print(TaskName+" Test case passed successfully")





x, y = createSin(3,1.96349540849362, 360,720)


SinCosSignalSamplesAreEqual("sin", "../signals/SinOutput.txt", x, y)

x_f, y_f = subtract_signals(x1, y1, x2, y2)

SubSignalSamplesAreEqual("Signal1.txt","Signal2.txt",x_f,y_f)

x_n, y_n = signal_normalization(x1, y1, '1')


NormalizeSignal(-1,1,x_n,y_n)
