import sys
sys.path.insert(0, './__util__')
from Constants import *
from LogClass import *
sys.path.insert(0, './__data__')
from Load import loadStopWords
sys.path.insert(0, './__preprocess__')
from Tokenize import tokenize
from Tokenize import stemming
import numpy as np
stopWords = None

def preprocess(dataset, algorithm):
    message = ""
    message+=PREPROCESS_BEGIN_MESSAGE+'\n'
    print (PREPROCESS_BEGIN_MESSAGE)
    check, stopWords, loadMessage = loadStopWords("/var/www/html/winifier/server/__server_python__/__preprocess__/stop_words/stanford_core_nlp_stopWords.txt")
    message+=loadMessage+'\n'
    if check:                
        tokenizeCheck, tokenList, tokenizeMessage = tokenize(dataset, algorithm)        
        message+=tokenizeMessage+'\n'
        if tokenizeCheck:
            removalCheck, pureTokens, removeStMessage = removeStopWords(tokenList, stopWords)
            message+=removeStMessage+'\n'
            if removalCheck:
                stemCheck, stemmedTokens, stemMessage = stemming(pureTokens)
                message+=stemMessage +'\n'
                if stemCheck:
                    labelListCheck, labelList, pointsList, labelPtMessage = getLabelsAndPoints(dataset)
                    message+=labelPtMessage+'\n'
                    if labelListCheck:
                        message+=PREPROCESS_SUCCESS_MESSAGE+'\n'
                        print(PREPROCESS_SUCCESS_MESSAGE)
                        with open(getPath()+"/__preprocess__/messages.log","a") as log:
                            log.write(message)
                        return True, stemmedTokens, pointsList, labelList
                    else:
                        message+=PREPROCESS_ERROR_MESSAGE+'\n'
                        print(PREPROCESS_ERROR_MESSAGE)
                        with open(getPath()+"/__preprocess__/messages.log","a") as log:
                            log.write(message)
                        return False, None, None, None
            else:
                message+=PREPROCESS_ERROR_MESSAGE
                print(PREPROCESS_ERROR_MESSAGE)
                with open(getPath()+"/__preprocess__/messages.log","a") as log:
                    log.write(message)
                return False, None, None, None
    


def removeStopWords(tokens, stopWords):
    message=""
    output=""
    descriptionList = []
    message+=STOPWORD_REMOVAL_BEGIN_MESSAGE+'\n'
    print (STOPWORD_REMOVAL_BEGIN_MESSAGE)
    try:
        for instance in tokens:
            pureTokens = np.array([])
            pureTokens = np.setdiff1d(instance, stopWords)
            descriptionList.append(pureTokens.tolist())
        message+=STOPWORD_REMOVAL_SUCCESS_MESSAGE+'\n'
        output+= "After Removing Stop Words \n"+str(descriptionList)+'\n'    
        print (STOPWORD_REMOVAL_SUCCESS_MESSAGE)
        with open(getPath()+"/__preprocess__/output.log","a") as log:
            log.write(output)
        return True, descriptionList, message
    except:
        message+=STOPWORD_REMOVAL_ERROR_MESSAGE+'\n'
        print (STOPWORD_REMOVAL_ERROR_MESSAGE)
        return False, None, message

def getLabelsAndPoints(dataset):
    message=""
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
        message+=LABELLIST_SUCCESS_MESSAGE+'\n'
        return True, labelList, pointsList, message
    except:
        message+=LABELLIST_ERROR_MESSAGE+'\n'
        print(LABELLIST_ERROR_MESSAGE)
        return false, None, None, message
