#!/usr/bin/env python
# coding: utf-8

# In[ ]:

file_path="D:/dsp-tasks-master/dsp-tasks-master/task1/output/"
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
def add_signales(indices1, samples1, indices2, samples2):
    sig1 = dict(zip(indices1, samples1))
    sig2 = dict(zip(indices2, samples2))

    all_indices = sorted(set(indices1) | set(indices2))

    result_samples = []
    for i in all_indices:
        s1 = sig1.get(i, 0)
        s2 = sig2.get(i, 0)
        result_samples.append(s1 + s2)

    return result_samples, all_indices

def sub_signales(indices1, samples1, indices2, samples2):
    sig1 = dict(zip(indices1, samples1))
    sig2 = dict(zip(indices2, samples2))

    all_indices = sorted(set(indices1) | set(indices2))

    result_samples = []
    for i in all_indices:
        s1 = sig1.get(i, 0)
        s2 = sig2.get(i, 0)
        result_samples.append(s1 - s2)

    return result_samples, all_indices

def multiply_signales(indices,samples,indices1,samples1):
    sample=[]
    if(len(indices)==len(indices1)):
        for i in range(len(indices)):
            sample.append(samples[i]*samples1[i])
    else:
        print("the indices of the 2 signals are not the same")
    return sample,indices

def multiply_signales_constant(indices,samples,constant):
    sample=[]
    for i in range(len(indices)):
        sample.append(samples[i]*constant)
    return sample,indices

def square_signales(indices, samples):
    sample=[]
    for i in range(len(indices)):
        sample.append(pow(samples[i],2))
    return sample,indices

def normalize_minus_to_one(indices, samples):
    sample = []
    for i in range(len(indices)):
        sample.append(2 * ((samples[i] - min(samples)) / (max(samples) - min(samples))) - 1)
    return sample, indices

def normalize_zero_to_one(indices, samples):
    sample=[]
    for i in range(len(indices)):
        sample.append( (samples[i]-min(samples))/ (max(samples)-min(samples)) )
    return sample,indices

def accumulate_signals(indices, samples):
    import numpy as np
    # y(n) = sum{k=-∞}->{n} (x[k])
    y = np.cumsum(samples)
    return indices, y

def AddSignalSamplesAreEqual(userFirstSignal,userSecondSignal,Your_indices,Your_samples):
    file_name=""
    if(userFirstSignal=='Signal1.txt' and userSecondSignal=='Signal2.txt'):
        file_name=file_path+"Signal1+signal2.txt" # write here path of signal1+signal2
    elif(userFirstSignal=='Signal1.txt' and userSecondSignal=='Signal3.txt'):
        file_name=file_path+"signal1+signal3.txt" # write here path of signal1+signal3
    expected_indices,expected_samples=ReadSignalFile(file_name)
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Addition Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Addition Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Addition Test case failed, your signal have different values from the expected one") 
            return
    print("Addition Test case passed successfully")


# In[ ]:


def MultiplySignalByConst(User_Const,Your_indices,Your_samples):
    if(User_Const==5):
        file_name="" # write here path of MultiplySignalByConstant-Signal1 - by 5.txt
    elif(User_Const==10):
        file_name="" # write here path of MultiplySignalByConstant-Signal2 - by 10.txt
        
    expected_indices,expected_samples=ReadSignalFile(file_name)      
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Multiply by "+User_Const.str()+ " Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Multiply by "+User_Const.str()+" Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Multiply by "+User_Const.str()+" Test case failed, your signal have different values from the expected one") 
            return
    print("Multiply by "+User_Const.str()+" Test case passed successfully")


# In[ ]:


#TaskName => choose it (string explain the name of task like (adding sig1+sig2,subtracting, .... etc.))
#output_file_name => output file path (output file given by TAs)
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

