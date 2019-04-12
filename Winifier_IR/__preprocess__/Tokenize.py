import sys
sys.path.insert(0, './__util__')
from Constants import *
from LogClass import *
import re
import numpy as np
from nltk.stem.porter import *

def tokenize(rowData):
    message=""
    output=""
    message+=TOKENIZATION_BEGIN_MESSAGE+'\n'
    tokenList = []
    print(TOKENIZATION_BEGIN_MESSAGE)
    try:     
        if UNDEFINED_INSTANCE not in str(rowData):
            data = re.sub(TOKENIZATION_REGEX, EMPTY_STRING, str(rowData))
            tokenList = data.lower().split(SPACE_STRING)            
            output+="After Tokenization\n"+str(tokenList)+'\n'        
            message+=TOKENIZATION_SUCCESSFUL_MESSAGE+'\n'                   
            print(TOKENIZATION_SUCCESSFUL_MESSAGE)       
            with open(getPath()+"/__preprocess__/output.log","a") as log:
                log.write(output)                     
            return True, np.array(tokenList), message        
    except:        
        message+=TOKENIZATION_ERROR_MESSAGE+'\n'        
        print(TOKENIZATION_ERROR_MESSAGE)
        return False, None, message

def stemming(pureTokens):
    try:
        output=""
        stemmer = PorterStemmer()
        stemmedTokens = [stemmer.stem(pureToken) for pureToken in pureTokens]
        stemmedTokens = [item.encode('ascii', 'ignore') for item in stemmedTokens]
        output+="After Stemming\n"+str(stemmedTokens)+'\n'
        print(STEMMING_SUCCESS_MESSAGE)
        with open(getPath()+"/__preprocess__/output.log","a") as log:
            log.write(output)
        return True, stemmedTokens, STEMMING_SUCCESS_MESSAGE
    except Exception as e:
        print(e)
        print(STEMMING_FAILED_MESSAGE)        
        return False, None, STEMMING_FAILED_MESSAGE
