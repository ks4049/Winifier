import sys
sys.path.insert(0, './__test__')
from Test import *
from Process import *

 
def cross_validation(folds, testingData, vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm):
    _slice_ = 1
    for _slice_ in range (1, folds+1):
        print("---------------"+str(_slice_)+"----------------")
        predictedValues = evaluate(testingData, vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm)
        totalAccuracy += formConfusionMatrix(testingData, predictedValues)
        _slice_ += 1
    print (float(totalAccuracy) / folds)

def percentage_split(testingData,vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm):
    predictedValues = evaluate(testingData,vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm)
    totalAccuracy = formConfusionMatrix(testingData, predictedValues)
    print(totalAccuracy)

