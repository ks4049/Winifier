import sys
from __util__.Constants import *
from __data__.Load import *
from __preprocess__.Preprocess import preprocess
from __train__.Bernoulli import initialize as B
from __train__.Multinomial import initialize as M
import datetime

def __init__(params):
    process = params[1]
    filePath = params[2]
    dataSetLimit = int(params[3])
    trainPercentage=None
    testPercentage=None
    numberOfFolds=None
    algorithmCheck = 0

    # Setup training options
    if process == PROCESS_TRAIN:
        algorithm = params[4]
        check, dataset = load(filePath, dataSetLimit)
        if check:
            trainType = params[5]
            if trainType == PS_TRAIN_TYPE:
                trainPercentage = int(params[6])
                testPercentage = 100-trainPercentage
                algorithmCheck = 1
            elif trainType == CV_TRAIN_TYPE:
                numberOfFolds = int(params[6])
                algorithmCheck = 1
            else:
                print (OPTIONS_ERROR_MESSAGE)

            # Train with algorithm provided to generate model file
            if algorithmCheck==1:
                if algorithm==B_ALGORITHM:
                    preProcessCheck, pureTokens, pointsList, labelList = preprocess(dataset, algorithm)
                    if(preProcessCheck):
                        B(trainType, pureTokens, pointsList, labelList, trainPercentage, testPercentage, numberOfFolds)
                elif algorithm==M_ALGORITHM:
                    preProcessCheck, pureTokens, pointsList, labelList = preprocess(dataset, algorithm)
                    if(preProcessCheck):
                        M(trainType, pureTokens, pointsList, labelList, trainPercentage, testPercentage, numberOfFolds)
                else:
                    print (OPTIONS_ALGORITHM_ERROR_MESSAGE)


    # Setup testing options
    elif process == PROCESS_TEST:
            # Load data from filePath provided
            if loadTestData(filePath, dataSetLimit):
                '''
                Load existing model file to test against.
                Model contains all parameters including
                algorithm (B/M) used to build model,
                and all supporting calculated probabilities.
                '''
                modelFilePath = params[4]
                if loadModel(modelFilePath):
                    '''
                    Run test data against model and evaluate results
                    '''
                    pass

startTime = datetime.datetime.now()
__init__(sys.argv)
endTime = datetime.datetime.now()
print ("Time taken for process "+str(endTime-startTime))
