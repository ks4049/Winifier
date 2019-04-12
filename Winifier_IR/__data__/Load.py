import sys
sys.path.insert(0, './__util__')
from Constants import *
from LogClass import *
from numpy import genfromtxt as GFT
import json
import re
import numpy as np

dataset = None
testDataset = None
model = None

def load(filePath, limit, delimiter="~"):
    message=""
    message+=LOADING_DATASET_MESSAGE+'\n'
    message+=filePath+'\n'
    print (LOADING_DATASET_MESSAGE)
    try:
        if limit == -1:
            dataset = GFT(filePath,delimiter=delimiter,dtype='<S')
        else:
            dataset = GFT(filePath,delimiter=delimiter,dtype='<S', max_rows=limit)
        for item in range(0,limit):
        	if dataset[item,1].item().decode()!="???":
        		dataset[item,1].item().decode()
        print (LOADING_DATASET_SUCCESSFUL_MESSAGE)
        message+=LOADING_DATASET_SUCCESSFUL_MESSAGE+'\n'
        print (str(len(dataset))+" Records Loaded")
        message+= str(len(dataset))+" Records Loaded"+'\n'
        with open(getPath()+"/__data__/messages.log","a") as log:
            log.write(message)
        return True, dataset
    except:
        message+=TRAIN_DATA_LOAD_ERROR_MESSAGE+'\n'
        print (TRAIN_DATA_LOAD_ERROR_MESSAGE)
        with open(getPath()+"/__data__/messages.log","a") as log:
            log.write(message)
        return False, None


def loadStopWords(filePath):
    message=""
    message+=LOADING_STOPWORDS_MESSAGE+'\n'
    print(LOADING_STOPWORDS_MESSAGE)
    tStopWords = ""
    try:
        with open(filePath, "r") as sw:
            sw = sw.readlines()
            for word in sw:
                tStopWords += word
        tStopWords = re.sub("['\"]", '\n', tStopWords)
        stopList = tStopWords.split("\n")
        print(LOADING_STOPWORDS_SUCCESSFUL_MESSAGE)
        message+=LOADING_STOPWORDS_SUCCESSFUL_MESSAGE+'\n'       
        return True, np.array(stopList), message
    except:
        message+=LOADING_STOPWORDS_ERROR_MESSAGE+'\n'
        print(LOADING_STOPWORDS_ERROR_MESSAGE)
        return False, None, message
