import sys
sys.path.insert(0, './__util__')
from Constants import *
sys.path.insert(0, './__train__')
from Train import *
sys.path.insert(0, './__test__')
from Test import *

def cross_validation(folds):
    return True

def percentage_split(algorithm, pureTokens, pointsList, labelList, trainingPercentage, testPercentage):
    trainingData = []
    testingData = []
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
        predictedValues = evaluate(testingData,vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm)
        totalAccuracy = formConfusionMatrix(testingData, predictedValues)
        print (totalAccuracy)
        return True
    except Exception as e:
        print(e)
        print(PERCENTAGE_SPLIT_ERROR_MESSAGE)
        return False

'''
def createModel(algorithm, trainType, wordDict, folds, trainingPercentage):
    print(CREATING_MODEL_MESSAGE)
    try:
        modelDictionary={
        "algorithm":algorithm,
        "trainType":trainType,
        "values":wordDict
        }
        with open(algorithm+"--"+trainType+".json","w") as file:
            json.dump(wordDict, file)
'''
