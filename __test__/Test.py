import math
import sys
sys.path.insert(0, './__util__')
from Constants import *

def evaluate(testData, vocabDict, positivePrior, negativePrior, positiveCount, negativeCount, featureSize, algorithm):
	message=""
	try:
		testOutput = {}
		counter=0
		for row in testData:
			actualPos = 0
			actualNeg = 0
			# pass through the dictionary
			for key in vocabDict:
				label = None
				if key in row[0]:
					positiveProb= vocabDict[key]["positiveProb"]
					actualPos += math.log10(positiveProb)
					negativeProb = vocabDict[key]["negativeProb"]
					actualNeg += math.log10(negativeProb)
				elif B_ALGORITHM in algorithm:
					nPositiveProb = vocabDict[key]["nPositiveProb"]
					actualPos += math.log10(nPositiveProb)
					nNegativeProb = vocabDict[key]["nNegativeProb"]
					actualNeg += math.log10(nNegativeProb)
			# handling new words			
			for word in row[0]:
				if word not in vocabDict:
					positiveProb = float(1)/(positiveCount+featureSize)
					actualPos+=math.log10(positiveProb)
					negativeProb = float(1)/(negativeCount+featureSize)
					actualNeg+=math.log10(negativeProb)
			actualPos+=math.log10(positivePrior)
			actualNeg+=math.log10(negativePrior)
			if(actualPos>actualNeg):
				label = POSITIVE_LABEL
			else:
				label = NEGATIVE_LABEL
			testOutput[counter] = {
			"positive": actualPos,
			"negative": actualNeg,
			"label":label
			}
			counter+=1
		print(EVALUATION_TEST_DATA_SUCESS)
		message+=EVALUATION_TEST_DATA_SUCESS+'\n'	
		return testOutput, message
	except:
		message+=DISTRIBUTION_INVALID+'\n'
		print(DISTRIBUTION_INVALID)
		return None, message

def formConfusionMatrix(testData, predictedValues):
	confusionDict = initializeConfusionDict()
	for key in predictedValues:
		tempList = testData[int(key)]
		if tempList[2]==predictedValues[key]["label"]:
			if tempList[2]==POSITIVE_LABEL:
				confusionDict["true"]["positive"]+=1
			else:
				confusionDict["true"]["negative"]+=1
		else:
			if predictedValues[key]["label"]==POSITIVE_LABEL:
				confusionDict["false"]["positive"]+=1
			else:
				confusionDict["false"]["negative"]+=1
	print (confusionDict)
	return float(confusionDict["true"]["positive"]+confusionDict["true"]["negative"])/(confusionDict["true"]["positive"]+confusionDict["true"]["negative"]+confusionDict["false"]["positive"]+confusionDict["false"]["negative"]), confusionDict

def initializeConfusionDict():
	confusionDict = {"true": {"positive":0, "negative":0}, "false": {"positive":0, "negative":0}}
	return confusionDict
