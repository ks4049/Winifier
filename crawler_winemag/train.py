from dictCount import *

def beginTrain(trainingData, positiveCount, negativeCount):
	positiveProb, negativeProb = getLabelProbability(positiveCount, negativeCount) #prior probabilities
	vocabList = makeVocabList(trainingData)
	wordDict = makeDict(trainingData, vocabList)
	print "length of vocabList"+str(len(vocabList))
	wordDict = computeProbability(wordDict, positiveCount, negativeCount, len(vocabList))
	return wordDict, positiveProb, negativeProb, len(vocabList)

def computeProbability(wordDict, positiveCount, negativeCount, featureSize):
	for key in wordDict:		
		wordDict[key]["positiveProb"]= float(wordDict[key]["positive"]+1)/(positiveCount+featureSize)		

		wordDict[key]["negativeProb"]= float(wordDict[key]["negative"]+1)/(negativeCount+featureSize)

		wordDict[key]["nPositiveProb"]= float(1-wordDict[key]["positiveProb"]);

		wordDict[key]["nNegativeProb"]= float(1-wordDict[key]["negativeProb"]);		
					
	return wordDict

def getLabelProbability(positiveCount, negativeCount):
	trainLen = positiveCount+negativeCount
	positiveProb = float(positiveCount)/trainLen		
	negativeProb = 1-positiveProb	
	return positiveProb, negativeProb

def makeVocabList(trainingData):	
	vocabList=set()
	for row in trainingData:
		for word in row[0]:
			if word not in vocabList:
				vocabList.add(word)
	return vocabList				