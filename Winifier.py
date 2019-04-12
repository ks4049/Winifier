import sys
from __util__.Constants import *
from __util__.LogClass import *
from __data__.Load import *
from __preprocess__.Preprocess import preprocess
from __train__.Bernoulli import initialize as B
from __train__.Multinomial import initialize as M
import datetime
from __train__.Process import processModelData
from __train__.Process import makeTestData

def __init__(params):
    projectName = params[1]
    logPath = "/var/www/html/winifier/server/projects/"+projectName
    setPath(logPath)
    process = params[2]
    filePath = params[3]
    dataSetLimit = int(params[4])
    trainPercentage=None
    testPercentage=None
    numberOfFolds=None
    algorithmCheck = 0
    testData=None
    # Setup training options
    if process == PROCESS_TRAIN:
        algorithm = params[5]
        check, dataset = load(filePath, dataSetLimit)
        if check:
            trainType = params[6]
            if trainType == PS_TRAIN_TYPE:
                trainPercentage = int(params[7])
                testPercentage = 100-trainPercentage
                algorithmCheck = 1
            elif trainType == CV_TRAIN_TYPE:
                numberOfFolds = int(params[7])
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
        makeSeparatorForTrainLogs()        

    # Setup testing options
    elif process == PROCESS_TEST:
        # Load data from filePath provided
        message=""
        check, testData = loadTestData(filePath, dataSetLimit)
        if check:
            '''
            Load existing model file to test against.
            Model contains all parameters including
            algorithm (B/M) used to build model,
            and all supporting calculated probabilities.
            '''
            modelFilePath = params[5]
            checkModel, modelData, algorithm = loadModel(modelFilePath)
            if checkModel:
                '''
                Run test data against model and evaluate results
                '''      
                preProcessCheck, pureTokens, pointsList, labelList = preprocess(testData, algorithm)                                                                                      
                if(preProcessCheck):
                    #print("testdatalen "+str(len(pureTokens)))                        
                    testData = makeTestData(pureTokens, pointsList, labelList) 
                    check, processMessage = processModelData(modelData, testData)
                    message+=processMessage+'\n'
                    if check:
                        message+=MODEL_EVALUATION_SUCCESS_MESSAGE+'\n'                                               
                        print(MODEL_EVALUATION_SUCCESS_MESSAGE)
                    else:
                        message+=MODEL_EVALUATION_ERROR_MESSAGE+'\n'
                        print(MODEL_EVALUATION_ERROR_MESSAGE) 
                else:
                    message+=PREPROCESS_ERROR_MESSAGE+'\n'
                    print(PREPROCESS_ERROR_MESSAGE)
                with open(getPath()+"/__test__/messages.log","a") as log:
                    log.write(message)    
        makeSeparatorForTestLogs()
                    
def makeSeparatorForTrainLogs():
    with open(getPath()+"/__data__/messages.log","a") as log:
        log.write(SEPARATOR)
    with open(getPath()+"/__preprocess__/messages.log","a") as log:
        log.write(SEPARATOR)
    with open(getPath()+"/__preprocess__/output.log","a") as log:
        log.write(SEPARATOR)
    with open(getPath()+"/__train__/messages.log","a") as log:
        log.write(SEPARATOR)
    with open(getPath()+"/__train__/output.log","a") as log:
        log.write(SEPARATOR)      

def makeSeparatorForTestLogs():
    with open(getPath()+"/__data__/messages.log","a") as log:
        log.write(SEPARATOR)
    with open(getPath()+"/__preprocess__/messages.log","a") as log:        
        log.write(SEPARATOR)
    with open(getPath()+"/__preprocess__/output.log","a") as log:
        log.write(SEPARATOR)        
    with open(getPath()+"/__test__/messages.log","a") as log:
        log.write(SEPARATOR)
    with open(getPath()+"/__test__/output.log","a") as log:
        log.write(SEPARATOR)       

startTime = datetime.datetime.now()
__init__(sys.argv)
endTime = datetime.datetime.now()

print ("Time taken for process "+str(endTime-startTime))
