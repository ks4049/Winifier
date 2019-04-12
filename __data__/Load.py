import sys
sys.path.insert(0, './__util__')
from Constants import *
from LogClass import *
sys.path.insert(0, './__model__')
from Validate import modelParser
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
            dataset = GFT(filePath,delimiter=delimiter,dtype='<S', max_rows=limit, encoding='UTF-8')
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

def loadTestData(filePath, limit, delimiter="~"):
    message=""
    message+=LOADING_DATASET_MESSAGE+'\n'
    message+=filePath+'\n'
    print(LOADING_DATASET_MESSAGE)
    try:
        if limit == -1:
            testDataset = GFT(filePath,delimiter=delimiter,dtype='<S')
        else:
            testDataset = GFT(filePath,delimiter=delimiter,dtype='<S', max_rows=limit)
        for item in range(0,limit):
            if testDataset[item,1].item().decode()!="???":
                testDataset[item,1].item().decode()    
        print (LOADING_DATASET_SUCCESSFUL_MESSAGE)
        print (str(len(testDataset))+" Records Loaded")
        message+=LOADING_DATASET_SUCCESSFUL_MESSAGE+'\n'
        message+=str(len(testDataset))+" Records Loaded"+'\n'
        with open(getPath()+"/__data__/messages.log","a") as log:
            log.write(message)
        return True, testDataset
    except:
        print (TEST_DATA_LOAD_ERROR_MESSAGE)
        message+=TEST_DATA_LOAD_ERROR_MESSAGE+'\n'
        with open(getPath()+"/__data__/messages.log","a") as log:
            log.write(message)
        return False, None

def loadModel(filePath):
    message=""
    print (LOADING_MODEL_MESSAGE)
    message+=LOADING_MODEL_MESSAGE+'\n'
    try:
        with open(filePath, "r") as modelData:
            model = json.load(modelData)
            check, algorithm = modelParser(model)
            if check:
                print (LOADING_MODEL_SUCCESSFUL_MESSAGE)
                message+=LOADING_MODEL_SUCCESSFUL_MESSAGE+'\n'
                with open(getPath()+"/__data__/messages.log","a") as log:
                    log.write(message)
                return True, model, algorithm                
            else:
                print (MODEL_LOAD_ERROR_MESSAGE)
                with open(getPath()+"/__data__/messages.log","a") as log:
                    log.write(message)                
                return False, None, None
    except:
        print (MODEL_LOAD_ERROR_MESSAGE)
        with open(getPath()+"/__data__/messages.log","a") as log:
            log.write(message)
        return False, None, None

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
