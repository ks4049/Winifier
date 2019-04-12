import sys
sys.path.insert(0, './__train__')
from Process import *
sys.path.insert(0, './__util__')
from Constants import *
from LogClass import *

def initialize(trainType, pureTokens, pointsList, labelList, trainPercentage, testPercentage, numberOfFolds):
    message=""
    print(B_TRAIN_BEGIN_MESSAGE)
    message+=B_TRAIN_BEGIN_MESSAGE+'\n'
    if trainType == PS_TRAIN_TYPE:
        trainCheck, algMessage = percentage_split(B_ALGORITHM, pureTokens, pointsList, labelList, trainPercentage, testPercentage)
    elif trainType == CV_TRAIN_TYPE:
        trainCheck, algMessage = cross_validation(B_ALGORITHM, pureTokens, pointsList, labelList, numberOfFolds)
    message+=algMessage+'\n' 
    with open(getPath()+"/__train__/messages.log","a") as log:
        log.write(message)  
    return True