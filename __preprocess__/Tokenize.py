import sys
sys.path.insert(0, './__util__')
from Constants import *
from LogClass import *
import re
import numpy as np
from nltk.stem.porter import *

def tokenize(dataset, algorithm):
    message=""
    output=""
    message+=TOKENIZATION_BEGIN_MESSAGE+'\n'
    tokenList = []
    print(TOKENIZATION_BEGIN_MESSAGE)
    try:
        for row in dataset:
            if UNDEFINED_INSTANCE not in str(row[0]):
                data = re.sub(TOKENIZATION_REGEX, EMPTY_STRING, str(row[0]))
                data = data.lower().split(SPACE_STRING)
                dataInstance = None
                if algorithm == B_ALGORITHM:
                    dataInstance = set()
                    for item in data:
                        dataInstance.add(item)
                    dataInstance = list(dataInstance)
                elif algorithm == M_ALGORITHM:
                    dataInstance = data
                tokenList.append(dataInstance)                
        output+="After Tokenization\n"+str(tokenList)+'\n'        
        message+=TOKENIZATION_SUCCESSFUL_MESSAGE+'\n'                   
        print(TOKENIZATION_SUCCESSFUL_MESSAGE)       
        with open(getPath()+"/__preprocess__/output.log","a") as log:
            log.write(output)                     
        return True, np.array(tokenList), message
    except Exception as e:
        print(e)
        message+=TOKENIZATION_ERROR_MESSAGE+'\n'        
        print(TOKENIZATION_ERROR_MESSAGE)
        return False, None, message

def stemming(pureTokens):
    try:
        output=""
        stemmer = PorterStemmer()
        stemmedList=[]
        for row in pureTokens:
            stemmedTokens = [stemmer.stem(pureToken) for pureToken in row]
            stemmedTokens = [item.encode('ascii', 'ignore') for item in stemmedTokens]
            stemmedList.append(stemmedTokens) 
        output+="After Stemming\n"+str(stemmedList)+'\n'
        print(STEMMING_SUCCESS_MESSAGE)
        with open(getPath()+"/__preprocess__/output.log","a") as log:
            log.write(output)
        return True, stemmedList, STEMMING_SUCCESS_MESSAGE
    except:
        print(STEMMING_FAILED_MESSAGE)        
        return False, None, STEMMING_FAILED_MESSAGE
