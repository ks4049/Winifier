import sys
sys.path.insert(0, './__train__')
from Process import *
sys.path.insert(0, './__util__')
from Constants import *

def initialize(trainType, pureTokens, pointsList, labelList, trainPercentage, testPercentage, numberOfFolds):
    print (B_TRAIN_BEGIN_MESSAGE)
    if trainType == PS_TRAIN_TYPE:
        trainCheck = percentage_split(B_ALGORITHM, pureTokens, pointsList, labelList, trainPercentage, testPercentage)
    elif trainType == CV_TRAIN_TYPE:
        trainCheck = cross_validation(B_ALGORITHM, trainPercentage, testPercentage)
    return True
