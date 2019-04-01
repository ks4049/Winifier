import sys
sys.path.insert(0, './__util__')
from Constants import *
sys.path.insert(0, './__data__')
from Load import loadStopWords
sys.path.insert(0, './__preprocess__')
from Tokenize import tokenize
import numpy as np

stopWords = None

def preprocess(dataset, algorithm):
    print (PREPROCESS_BEGIN_MESSAGE)
    check, stopWords = loadStopWords("./__preprocess__/stop_words/stanford_core_nlp_stopWords.txt")
    if check:
        tokenizeCheck, tokenList = tokenize(dataset, algorithm)
        if tokenizeCheck:
            removalCheck, pureTokens = removeStopWords(tokenList)
            if removalCheck:
                labelListCheck, labelList, pointsList = getLabelsAndPoints(dataset)
                if labelListCheck:
                    print(PREPROCESS_SUCCESS_MESSAGE)
                    return True, pureTokens, pointsList, labelList
                else:
                    print(PREPROCESS_ERROR_MESSAGE)
                    return False, None, None, None
            else:
                print(PREPROCESS_ERROR_MESSAGE)
                return False, None, None, None

def removeStopWords(tokens):
    descriptionList = []
    print (STOPWORD_REMOVAL_BEGIN_MESSAGE)
    try:
        for instance in tokens:
            pureTokens = np.array([])
            pureTokens = np.setdiff1d(instance, stopWords)
            descriptionList.append(pureTokens.tolist())
        print (STOPWORD_REMOVAL_SUCCESS_MESSAGE)
        return True, descriptionList
    except:
        print (STOPWORD_REMOVAL_ERROR_MESSAGE)
        return False, None

def getLabelsAndPoints(dataset):
    pointsList = []
    labelList = []
    try:
        for row in dataset:
            if UNDEFINED_INSTANCE not in str(row[0]):
                pointsList.append(row[1])
                if int(row[1]) > 88:
                    labelList.append(POSITIVE_LABEL)
                else :
                    labelList.append(NEGATIVE_LABEL)
        print(LABELLIST_SUCCESS_MESSAGE)
        return True, labelList, pointsList
    except:
        print(LABELLIST_ERROR_MESSAGE)
        return false, None, None
