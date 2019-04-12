import sys
sys.path.insert(0, './__util__')
from Constants import *
from LogClass import * 
sys.path.insert(0, './__train__')
from Train import *
sys.path.insert(0, './__test__')
from Test import *
import traceback
import yaml


def createTrainingCV(lower, higher, totalSize, descriptionList, pointsList, labelList):
    trainingData = []
    for i in range(0, lower):
        trainingList =[]
        trainingList.append(descriptionList[i])
        trainingList.append(pointsList[i])
        trainingList.append(labelList[i])
        trainingData.append(trainingList)

    for i in range(higher, totalSize):
        trainingList =[]
        trainingList.append(descriptionList[i])
        trainingList.append(pointsList[i])
        trainingList.append(labelList[i])
        trainingData.append(trainingList)
    return trainingData

def createTestingCV(lower, higher, descriptionList, pointsList, labelList):
    testData = []
    for i in range(lower, higher):
        testList =[]
        testList.append(descriptionList[i])
        testList.append(pointsList[i])
        testList.append(labelList[i])
        testData.append(testList)
    return testData

def cross_validation(algorithm, pureTokens, pointsList, labelList, folds):
    message=""
    output=""
    finalVocabDict={}
    trainingData = []
    testingData = []
    _slice_ = 1
    totalAccuracy = 0
    datasetSize = len(pureTokens)
    print(CROSS_VALIDATION_BEGIN_MESSAGE)
    try:
        for _slice_ in range(1, folds + 1):
            finalVocabDict[_slice_]={}
            output+="---------------"+str(_slice_)+"----------------"+'\n'
            print("---------------"+str(_slice_)+"----------------")
            testLen = int(len(pointsList) / folds)
            lower = testLen * (_slice_ - 1)
            higher = testLen * _slice_
            trainingData = createTrainingCV(lower, higher, len(pureTokens), pureTokens, pointsList, labelList)
            testingData = createTestingCV(lower, higher, pureTokens, pointsList, labelList)
            vocabDict, positiveProb, negativeProb, featureSize, positiveCount, negativeCount, trainMessage, trainOutput = beginTrainingProcess(trainingData, algorithm)
            message+=trainMessage+'\n'
            output+="After training on slice\n"+str(trainOutput)+'\n'   
            finalVocabDict[_slice_]["vocabSize"] = featureSize
            finalVocabDict[_slice_]["positiveCount"]= positiveCount
            finalVocabDict[_slice_]["negativeCount"]= negativeCount
            finalVocabDict[_slice_]["positiveProb"]= positiveProb
            finalVocabDict[_slice_]["negativeProb"]= negativeProb
            finalVocabDict[_slice_]["probability"]=vocabDict
            predictedValues, evalMessage = evaluate(testingData, vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm)
            message+=evalMessage+'\n'
            output+="After Testing\n"+str(predictedValues)+'\n'
            accuracy, confusionMatrix= formConfusionMatrix(testingData, predictedValues)
            output+="Confusion Matrix\n"+str(confusionMatrix)+'\n'
            output+="Slice "+str(_slice_)+" accuracy\n"+str(accuracy)+'\n'
            totalAccuracy+=accuracy
            _slice_ += 1
        print(CROSS_VALIDATION_SUCCESS_MESSAGE)  
        message+=CROSS_VALIDATION_SUCCESS_MESSAGE+'\n'  
        print (float(totalAccuracy)/folds)
        modelMessage=createModel(algorithm, CV_TRAIN_TYPE, finalVocabDict, folds, datasetSize, None, None, None, None)
        message+=modelMessage+'\n'
        with open(getPath()+"/__train__/output.log","a") as log:
            log.write(output)
        return True, message
    except:
        message+=CROSS_VALIDATION_ERROR_MESSAGE+'\n'
        print(CROSS_VALIDATION_ERROR_MESSAGE)
        return False, message    

def percentage_split(algorithm, pureTokens, pointsList, labelList, trainingPercentage, testPercentage):
    message=""
    output=""
    trainingData = []
    testingData = []
    datasetSize = len(pureTokens)
    counter = int(len(pureTokens) * (float(trainingPercentage)/100))
    message+=PERCENTAGE_SPLIT_BEGIN_MESSAGE
    print(PERCENTAGE_SPLIT_BEGIN_MESSAGE)
    # splitting data to get training set
    try:
        for item in range(0,counter):
            trainingList = []
            trainingList.append(pureTokens[item])
            trainingList.append(pointsList[item])
            trainingList.append(labelList[item])
            trainingData.append(trainingList)
        output+="Train Dataset\n"+str(trainingData)+'\n'    
        # splitting data to get test set
        for item in range(counter,len(pureTokens)):
            testList = []
            testList.append(pureTokens[item])
            testList.append(pointsList[item])
            testList.append(labelList[item])
            testingData.append(testList)
        output+="TestDataset\n"+str(testingData)+'\n'
        vocabDict, positiveProb, negativeProb, featureSize, positiveCount, negativeCount, trainMessage, trainOutput = beginTrainingProcess(trainingData, algorithm)
        message+=trainMessage+'\n'
        output+="After Training\n"+str(trainOutput)+'\n'
        output+="Vocab Dictionary\n"+str(vocabDict)+'\n'
        message+=TRAINING_SUCCESS_MESSAGE+'\n'
        print(TRAINING_SUCCESS_MESSAGE)
        predictedValues, evalMessage = evaluate(testingData,vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm)
        message+=evalMessage+'\n'
        output+="After Testing\n"+str(predictedValues)+'\n'
        totalAccuracy, confusionMatrix = formConfusionMatrix(testingData, predictedValues)
        output+="Confusion Matrix\n"+str(confusionMatrix)+'\n'
        output+="Model Accuracy\n"+str(totalAccuracy)+'\n'
        modelMessage=createModel(algorithm, PS_TRAIN_TYPE, vocabDict, trainingPercentage, datasetSize, positiveProb, negativeProb, positiveCount, negativeCount)
        message+=modelMessage+'\n'
        print (totalAccuracy)
        with open(getPath()+"/__train__/output.log","a") as log:
            log.write(output)
        return True, message
    except:
        message+=PERCENTAGE_SPLIT_ERROR_MESSAGE
        print(PERCENTAGE_SPLIT_ERROR_MESSAGE)
        return False, message


def createModel(algorithm, trainType, wordDict, splitFold, datasetSize, positivePrior, negativePrior, positiveCount, negativeCount):
    message=""
    print(CREATING_MODEL_MESSAGE)
    message+=CREATING_MODEL_MESSAGE+'\n'
    try:
        modelDictionary={
        "algorithm":str(algorithm),
        "trainType":str(trainType),
        "trainDatasetSize": str(datasetSize),
        }
        if trainType==PS_TRAIN_TYPE:
            modelDictionary["percentageSplit"]=str(splitFold)
            modelDictionary["vocabSize"]=str(len(wordDict))
            modelDictionary["positiveCount"]= str(positiveCount)
            modelDictionary["negativeCount"]= str(negativeCount)
            modelDictionary["positivePrior"] = str(positivePrior)
            modelDictionary["negativePrior"] = str(negativePrior)            
        else:
            modelDictionary["numberOfFolds"] = str(splitFold) 
        modelDictionary["probability"]=str(wordDict)           
        with open(getPath()+"/__model__/generated/"+str(algorithm)+"__"+str(trainType)+"__"+str(splitFold)+".json","w") as file:
            json.dump(modelDictionary,file)
        message+=MODEL_CREATED_MESSAGE+'\n'    
        print(MODEL_CREATED_MESSAGE)
        return message        
    except:
        message+=MODEL_NOT_CREATED_MESSAGE        
        print(MODEL_NOT_CREATED_MESSAGE)
        return message

def processModelData(modelData, testData):
    message=""
    output=""
    print(PROCESSING_MODEL_FILE)
    message+=PROCESSING_MODEL_FILE+'\n'
    try:
        #print(modelData)
        algorithm = modelData["algorithm"]
        trainType = modelData["trainType"]
        if trainType == PS_TRAIN_TYPE:
            vocabDict = yaml.load(modelData["probability"])
            positivePrior = float(modelData["positivePrior"])
            negativePrior = float(modelData["negativePrior"])
            positiveCount = int(modelData["positiveCount"])
            negativeCount = int(modelData["negativeCount"])
            featureSize = int(modelData["vocabSize"]) 
            predictedValues, evalMessage =  evaluate(testData, vocabDict, positivePrior, negativePrior, positiveCount, negativeCount, featureSize, algorithm)
            message+=evalMessage+'\n'
            output+="Predictions after testing\n"+str(predictedValues)+'\n'
            totalAccuracy, confusionMatrix = formConfusionMatrix(testData, predictedValues)
            output+="Confusion Matrix\n"+str(confusionMatrix)+'\n'
            output+="Model Accuracy\n"+str(totalAccuracy)+'\n' 
            print(totalAccuracy)
            message+=MODEL_PROCESSING_SUCCESS+'\n'
            print(MODEL_PROCESSING_SUCCESS)
            with open(getPath()+"/__test__/output.log","a") as log:
                log.write(output)            
            return True, message            
        elif trainType==CV_TRAIN_TYPE:
            #process the model data and evaluate for every fold             
            numberOfFolds = int(modelData["numberOfFolds"])
            foldData = yaml.load(modelData["probability"])
            _slice_=1
            totalAccuracy=0
            for _slice_ in range(1, numberOfFolds+1):
                output+="---------------"+str(_slice_)+"----------------"+'\n'
                print("---------------"+str(_slice_)+"----------------")
                tempData = foldData[_slice_]
                positivePrior = float(tempData["positiveProb"])
                negativePrior = float(tempData["negativeProb"])
                positiveCount = int(tempData["positiveCount"])
                negativeCount = int(tempData["negativeCount"])
                featureSize = int(tempData["vocabSize"])
                vocabDict = tempData["probability"]
                predictedValues, evalMessage =evaluate(testData, vocabDict, positivePrior, negativePrior, positiveCount, negativeCount, featureSize, algorithm)
                message+=evalMessage+'\n'
                output+="Predictions for fold "+str(_slice_)+"\n"+str(predictedValues)+'\n'
                accuracy, confusionMatrix= formConfusionMatrix(testData, predictedValues)
                totalAccuracy+=accuracy   
                output+="Confusion Matrix\n"+str(confusionMatrix)+'\n'             
                output+="Accuracy on fold "+str(_slice_)+'\n'+str(accuracy)+'\n'               
                _slice_+=1
            print(float(totalAccuracy)/numberOfFolds)
            output+="Model Accuracy\n"+str(float(totalAccuracy)/numberOfFolds)+'\n'
            message+=MODEL_PROCESSING_SUCCESS+'\n'            
            print(MODEL_PROCESSING_SUCCESS)
            with open(getPath()+"/__test__/output.log","a") as log:
                log.write(output)            
            return True, message
        else:
            message+=MODEL_PROCESSING_ERROR+'\n'
            print(MODEL_PROCESSING_ERROR)            
            return false, message;              
    except:
        message+=MODEL_PROCESSING_ERROR
        print(MODEL_PROCESSING_ERROR)
        return false, message
        
def makeTestData(pureTokens, pointsList, labelList):
    output=""
    message=""
    try: 
        testingData=[]
        for item in range(0,len(pureTokens)):
            testList = []
            testList.append(pureTokens[item])
            testList.append(pointsList[item])
            testList.append(labelList[item])
            testingData.append(testList)
        output+="Testing Data to be evaluated\n"+str(testingData)+'\n'
        message+=TEST_DATA_FORMED+'\n'
        with open(getPath()+"/__test__/output.log","a") as log:
            log.write(output)
        with open(getPath()+"/__test__/messages.log","a") as log:
            log.write(message)    
        return testingData    
    except:
        print(TEST_DATA_NOT_FORMED) 
        message+=TEST_DATA_NOT_FORMED+'\n'
        with open(getPath()+"/__test__/messages.log","a") as log:
            log.write(message)      
