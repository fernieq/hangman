#!/usr/bin/env python
# coding: utf-8

# # Gaussian generative models for handwritten digit classification

# For this project, we will be using the *entire* `MNIST` dataset. The code below defines some helper functions that will load `MNIST` onto your computer.

# In[5]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt 
import gzip, os, sys
import numpy as np
from scipy.stats import multivariate_normal

if sys.version_info[0] == 2:
    from urllib import urlretrieve
else:
    from urllib.request import urlretrieve


# In[6]:


# Function that downloads a specified MNIST data file from Yann Le Cun's website
def download(filename, source='http://yann.lecun.com/exdb/mnist/'):
    print("Downloading %s" % filename)
    urlretrieve(source + filename, filename)

# Invokes download() if necessary, then reads in images
def load_mnist_images(filename):
    if not os.path.exists(filename):
        download(filename)
    with gzip.open(filename, 'rb') as f:
        data = np.frombuffer(f.read(), np.uint8, offset=16)
    data = data.reshape(-1,784)
    return data

def load_mnist_labels(filename):
    if not os.path.exists(filename):
        download(filename)
    with gzip.open(filename, 'rb') as f:
        data = np.frombuffer(f.read(), np.uint8, offset=8)
    return data


# Now load in the training set and test set

# In[7]:


## Load the training set
train_data = load_mnist_images('train-images-idx3-ubyte.gz')
train_labels = load_mnist_labels('train-labels-idx1-ubyte.gz')

## Load the testing set
test_data = load_mnist_images('t10k-images-idx3-ubyte.gz')
test_labels = load_mnist_labels('t10k-labels-idx1-ubyte.gz')


# The function **displaychar** shows a single MNIST digit. To do this, it first has to reshape the 784-dimensional vector into a 28x28 image.

# In[8]:


def displaychar(image):
    plt.imshow(np.reshape(image, (28,28)), cmap=plt.cm.gray)
    plt.axis('off')
    plt.show()


# In[5]:


displaychar(train_data[58])


# The training set consists of 60,000 images. Thus `train_data` should be a 60000x784 array while `train_labels` should be 60000x1. Let's check.

# In[9]:


train_data.shape, train_labels.shape


# In[13]:


from collections import defaultdict

train = train_data[:50000]
trainY = train_labels[:50000]
valid = train_data[50000:]
validY = train_labels[50000:]

def calcMean():
    nums = defaultdict(list)
    for i in range(len(trainY)):
        if trainY[i] not in nums.keys():
            nums[trainY[i]] = [train[i]]
        else:
            nums[trainY[i]].append(train[i])
            
    m = []
    for i in range(10):
        m.append(np.array(nums[i]).mean(axis=0))
    return m

mean = calcMean()
        


# In[18]:


def calcCov():
    nums = defaultdict(list)
    for i in range(len(trainY)):
        if trainY[i] not in nums.keys():
            nums[trainY[i]] = [train[i]]
        else:
            nums[trainY[i]].append(train[i])
            
    s = []
    for i in range(10):
        s.append(np.cov(np.transpose(nums[i])))
    return s

Sigma = calcCov()


# In[22]:


def createGaussians(c):
    g = []
    for i in range(10):
        g.append(multivariate_normal(mean[i], Sigma[i] + c * np.identity(784)))
    return g

gaussians = createGaussians(1000)


# In[25]:


def calcPi():
    nums = defaultdict(list)
    for i in range(len(trainY)):
        if trainY[i] not in nums.keys():
            nums[trainY[i]] = [train[i]]
        else:
            nums[trainY[i]].append(train[i])
            
    p = []
    for i in range(10):
        p.append(len(nums[i]) / 50000)
        
    return p

pi = calcPi()


# In[37]:


import math

def predict(x):
    p = []
    for i in range(10):
        p.append(math.log(pi[i]) + gaussians[i].logpdf(x))
    return np.argmax(p)


# In[38]:


from random import randint

def test():
    
    predictions = []
    for i in range(len(test_data)):
        predictions.append(predict(test_data[i]))
        
    numCorrect = 0
    numTotal = 0
    misclass = []
    
    for i in range(len(test_labels)):
        if(predictions[i] == test_labels[i]):
            numCorrect += 1
        else:
            misclass.append(i)
        numTotal += 1
        
    print("Accuracy is %d / %d" % (numCorrect, numTotal))
    
    return misclass


# In[39]:


misclassified = test()


# In[55]:


for i in range(5):
    print(misclassified[randint(0,len(misclassified))])


# In[59]:


m = [4427, 18, 4211, 3732, 9839]

def findPosterior():
    for i in range(5):
        m1 = m[i]
        pt = test_data[m1]
        prob = []
        for i in range(10):
            prob.append(gaussians[i].logpdf(pt))
        print(prob)
        print(predict(pt))

findPosterior()


# In[ ]:





# In[ ]:




