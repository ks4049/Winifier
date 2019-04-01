import sys
sys.path.insert(0, './__util__')
from Constants import *
sys.path.insert(0, './__train__')
from Train import *
sys.path.insert(0, './__test__')
from Test import *

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
    finalVocabDict={}
    trainingData = []
    testingData = []
    _slice_ = 1
    totalAccuracy = 0
    datasetSize = len(pureTokens)
    for _slice_ in range(1, folds + 1):
        print("---------------"+str(_slice_)+"----------------")
        testLen = int(len(pointsList) / folds)
        lower = testLen * (_slice_ - 1)
        higher = testLen * _slice_
        trainingData = createTrainingCV(lower, higher, len(pureTokens), pureTokens, pointsList, labelList)
        testingData = createTestingCV(lower, higher, pureTokens, pointsList, labelList)
        vocabDict, positiveProb, negativeProb, featureSize, positiveCount, negativeCount = beginTrainingProcess(trainingData, algorithm)
        finalVocabDict[_slice_]=vocabDict
        predictedValues = evaluate(testingData, vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm)
        totalAccuracy += formConfusionMatrix(testingData, predictedValues)
        _slice_ += 1
    print (float(totalAccuracy) / folds)
    createModel(algorithm, CV_TRAIN_TYPE, finalVocabDict, folds, datasetSize)
    return True

def percentage_split(algorithm, pureTokens, pointsList, labelList, trainingPercentage, testPercentage):
    trainingData = []
    testingData = []
    datasetSize = len(pureTokens)
    counter = int(len(pureTokens) * float(trainingPercentage)/100)
    print(PERCENTAGE_SPLIT_BEGIN_MESSAGE)
    # splitting data to get training set
    try:
        for item in range(0,counter):
            trainingList = []
            trainingList.append(pureTokens[item])
            trainingList.append(pointsList[item])
            trainingList.append(labelList[item])
            trainingData.append(trainingList)

        # splitting data to get test set
        for item in range(counter,len(pureTokens)):
            testList = []
            testList.append(pureTokens[item])
            testList.append(pointsList[item])
            testList.append(labelList[item])
            testingData.append(testList)

        vocabDict, positiveProb, negativeProb, featureSize, positiveCount, negativeCount = beginTrainingProcess(trainingData, algorithm)
        print(TRAINING_SUCCESS_MESSAGE)
        predictedValues = evaluate(testingData,vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm)
        totalAccuracy = formConfusionMatrix(testingData, predictedValues)
        createModel(algorithm, PS_TRAIN_TYPE, vocabDict, trainingPercentage, datasetSize)
        print (totalAccuracy)
        return True
    except:
        print(PERCENTAGE_SPLIT_ERROR_MESSAGE)
        return False


def createModel(algorithm, trainType, wordDict, splitFold, datasetSize):
    print(CREATING_MODEL_MESSAGE)
    try:
        modelDictionary={
        "algorithm":str(algorithm),
        "trainType":str(trainType),
        "trainDatasetSize": str(datasetSize),
        }
        if trainType==PS_TRAIN_TYPE:
            modelDictionary["percentageSplit"]=str(splitFold)
            modelDictionary["vocabSize"]=str(len(wordDict)),

        else:
            modelDictionary["numberOfFolds"] = str(splitFold)
        modelDictionary["probability"]=str(wordDict)
        with open("./__model__/generated/"+str(algorithm)+"__"+str(trainType)+"__"+str(splitFold)+".json","w") as file:
            json.dump(modelDictionary, file)
        print(MODEL_CREATED_MESSAGE)
    except:
        print(MODEL_NOT_CREATED_MESSAGE)
