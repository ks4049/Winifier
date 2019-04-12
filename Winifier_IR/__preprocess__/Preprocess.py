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

def preprocess(rowData):
    message = ""
    message+=PREPROCESS_BEGIN_MESSAGE+'\n'
    print (PREPROCESS_BEGIN_MESSAGE)
    check, stopWords, loadMessage = loadStopWords("./__preprocess__/stop_words/stanford_core_nlp_stopWords.txt")
    message+=loadMessage+'\n'
    if check:                
        tokenizeCheck, tokenList, tokenizeMessage = tokenize(rowData)        
        message+=tokenizeMessage+'\n'
        if tokenizeCheck:
            removalCheck, pureTokens, removeStMessage = removeStopWords(tokenList, stopWords)
            message+=removeStMessage+'\n'
            if removalCheck:
                stemCheck, stemmedTokens, stemMessage = stemming(pureTokens)
                message+=stemMessage +'\n'
                if stemCheck:                   
                    message+=PREPROCESS_SUCCESS_MESSAGE+'\n'
                    print(PREPROCESS_SUCCESS_MESSAGE)
                    with open(getPath()+"/__preprocess__/messages.log","a") as log:
                        log.write(message)
                    return True, stemmedTokens
                else:
                    message+=PREPROCESS_ERROR_MESSAGE+'\n'
                    print(PREPROCESS_ERROR_MESSAGE)
                    with open(getPath()+"/__preprocess__/messages.log","a") as log:
                        log.write(message)
                    return False, None
            else:
                message+=PREPROCESS_ERROR_MESSAGE
                print(PREPROCESS_ERROR_MESSAGE)
                with open(getPath()+"/__preprocess__/messages.log","a") as log:
                    log.write(message)
                return False, None
    


def removeStopWords(tokens, stopWords):
    message=""
    output=""
    descriptionList = []
    message+=STOPWORD_REMOVAL_BEGIN_MESSAGE+'\n'
    print (STOPWORD_REMOVAL_BEGIN_MESSAGE)
    try:        
        pureTokens = np.array([])
        pureTokens = np.setdiff1d(tokens, stopWords)
        descriptionList=pureTokens.tolist()
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

