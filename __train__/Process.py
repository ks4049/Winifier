import sys
sys.path.insert(0, './__util__')
from Constants import *
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
    finalVocabDict={}
    trainingData = []
    testingData = []
    _slice_ = 1
    totalAccuracy = 0
    datasetSize = len(pureTokens)
    for _slice_ in range(1, folds + 1):
        finalVocabDict[_slice_]={}
        print("---------------"+str(_slice_)+"----------------")
        testLen = int(len(pointsList) / folds)
        lower = testLen * (_slice_ - 1)
        higher = testLen * _slice_
        trainingData = createTrainingCV(lower, higher, len(pureTokens), pureTokens, pointsList, labelList)
        testingData = createTestingCV(lower, higher, pureTokens, pointsList, labelList)
        vocabDict, positiveProb, negativeProb, featureSize, positiveCount, negativeCount = beginTrainingProcess(trainingData, algorithm)
        finalVocabDict[_slice_]["vocabSize"] = featureSize
        finalVocabDict[_slice_]["positiveCount"]= positiveCount
        finalVocabDict[_slice_]["negativeCount"]= negativeCount
        finalVocabDict[_slice_]["positiveProb"]= positiveProb
        finalVocabDict[_slice_]["negativeProb"]= negativeProb
        finalVocabDict[_slice_]["probability"]=vocabDict
        predictedValues = evaluate(testingData, vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm)
        totalAccuracy += formConfusionMatrix(testingData, predictedValues)
        _slice_ += 1
    print (float(totalAccuracy)/folds)
    createModel(algorithm, CV_TRAIN_TYPE, finalVocabDict, folds, datasetSize, None, None, None, None)
    return True

def percentage_split(algorithm, pureTokens, pointsList, labelList, trainingPercentage, testPercentage):
    trainingData = []
    testingData = []
    datasetSize = len(pureTokens)
    counter = int(len(pureTokens) * (float(trainingPercentage)/100))
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
        createModel(algorithm, PS_TRAIN_TYPE, vocabDict, trainingPercentage, datasetSize, positiveProb, negativeProb, positiveCount, negativeCount)
        print (totalAccuracy)
        return True
    except:
        print(PERCENTAGE_SPLIT_ERROR_MESSAGE)
        return False


def createModel(algorithm, trainType, wordDict, splitFold, datasetSize, positivePrior, negativePrior, positiveCount, negativeCount):
    print(CREATING_MODEL_MESSAGE)
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
        with open("./__model__/generated/"+str(algorithm)+"__"+str(trainType)+"__"+str(splitFold)+".json","w") as file:
            json.dump(modelDictionary,file)
        print(MODEL_CREATED_MESSAGE)
    except Exception as e:
        traceback.print_exc()
        print(MODEL_NOT_CREATED_MESSAGE)

def processModelData(modelData, testData):
    print(PROCESSING_MODEL_FILE)
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
            predictedValues =  evaluate(testData, vocabDict, positivePrior, negativePrior, positiveCount, negativeCount, featureSize, algorithm)
            totalAccuracy = formConfusionMatrix(testData, predictedValues) 
            print(totalAccuracy)
            return True            
        elif trainType==CV_TRAIN_TYPE:
            #process the model data and evaluate for every fold 
            numberOfFolds = int(modelData["numberOfFolds"])
            foldData = yaml.load(modelData["probability"])
            _slice_=1
            totalAccuracy=0
            for _slice_ in range(1, numberOfFolds+1):
                tempData = foldData[_slice_]
                positivePrior = float(tempData["positiveProb"])
                negativePrior = float(tempData["negativeProb"])
                positiveCount = int(tempData["positiveCount"])
                negativeCount = int(tempData["negativeCount"])
                featureSize = int(tempData["vocabSize"])
                vocabDict = tempData["probability"]
                predictedValues =evaluate(testData, vocabDict, positivePrior, negativePrior, positiveCount, negativeCount, featureSize, algorithm)
                totalAccuracy += formConfusionMatrix(testData, predictedValues)
                _slice_+=1
            print (float(totalAccuracy)/numberOfFolds)
            return True
        else:
            return false;              
    except Exception as e:
        traceback.print_exc()
        print(e)
        #print(MODEL_NOT_PROCESSED)
def makeTestData(pureTokens, pointsList, labelList):
    try: 
        testingData=[]
        for item in range(0,len(pureTokens)):
            testList = []
            testList.append(pureTokens[item])
            testList.append(pointsList[item])
            testList.append(labelList[item])
            testingData.append(testList)
        return testingData    
    except Exception as e:
        #print(TEST_DATA_NOT_FORMED)        
        print(e)
        pass
