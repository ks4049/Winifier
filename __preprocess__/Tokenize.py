import sys
sys.path.insert(0, './__util__')
from Constants import *
import re
import numpy as np
from nltk.stem.porter import *

def tokenize(dataset, algorithm):
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
                stemCheck, stemmedTokens = stemming(dataInstance)
                if not stemCheck:
                    return False, None
                else:
                    tokenList.append(stemmedTokens)
        print(TOKENIZATION_SUCCESSFUL_MESSAGE)
        return True, np.array(tokenList)
    except:
        print(TOKENIZATION_ERROR_MESSAGE)
        return False, None

def stemming(pureTokens):
    try:
        stemmer = PorterStemmer()
        stemmedTokens = [stemmer.stem(pureToken) for pureToken in pureTokens]
        stemmedTokens = [item.encode('ascii', 'ignore') for item in stemmedTokens]
        return True, stemmedTokens
    except:
        print(STEMMING_FAILED_MESSAGE)
        return False, None
