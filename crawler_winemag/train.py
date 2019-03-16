from dictCount import *

def beginTrain(trainingData):
	positiveProb, negativeProb = getLabelProbability(trainingData) #prior probabilities
	vocabList = makeVocabList(trainingData)
	wordDict = makeDict(trainingData, vocabList)
	wordDict = computeProbability(wordDict)
	return wordDict, positiveProb, negativeProb

def computeProbability(wordDict):
	for key in wordDict:
		oneCardinality = wordDict[key]["positive"]+wordDict[key]["negative"]
		zeroCardinality = wordDict[key]["nPositive"]+wordDict[key]["nNegative"]					

		# try:
		# 	wordDict[key]["positiveProb"] = float(wordDict[key]["positive"])/(wordDict[key]["positive"]+wordDict[key]["nPositive"])		
		# except:			
		wordDict[key]["positiveProb"]= float(wordDict[key]["positive"]+1)/(oneCardinality+wordDict[key]["positive"]+wordDict[key]["nPositive"])		

		# try:	
		# 	wordDict[key]["negativeProb"] = float(wordDict[key]["negative"])/(wordDict[key]["negative"]+wordDict[key]["nNegative"])		
		# except:
		wordDict[key]["negativeProb"]= float(wordDict[key]["negative"]+1)/(oneCardinality+wordDict[key]["negative"]+wordDict[key]["nNegative"])

		# try:		
		# 	wordDict[key]["nPositiveProb"] = float(wordDict[key]["nPositive"])/(wordDict[key]["positive"]+wordDict[key]["nPositive"])
		# except:
		wordDict[key]["nPositiveProb"]= float(wordDict[key]["nPositive"]+1)/(zeroCardinality+wordDict[key]["positive"]+wordDict[key]["nPositive"])

		# try:	
		# 	wordDict[key]["nNegativeProb"] = float(wordDict[key]["nNegative"])/(wordDict[key]["negative"]+wordDict[key]["nNegative"])
		# except:
		wordDict[key]["nNegativeProb"]= float(wordDict[key]["nNegative"]+1)/(zeroCardinality+wordDict[key]["negative"]+wordDict[key]["nNegative"])			


		# if wordDict[key]["positiveProb"]==0:
		# 	wordDict[key]["positiveProb"]= float(1)/(oneCardinality+wordDict[key]["positive"]+wordDict[key]["nPositive"])
		# if wordDict[key]["negativeProb"]==0:
		# 	wordDict[key]["negativeProb"]= float(1)/(oneCardinality+wordDict[key]["negative"]+wordDict[key]["nNegative"])
		# if wordDict[key]["nPositiveProb"]==0:
		# 	wordDict[key]["nPositiveProb"]= float(1)/(zeroCardinality+wordDict[key]["positive"]+wordDict[key]["nPositive"])
		# if wordDict[key]["nNegativeProb"]==0:
		# 	wordDict[key]["nNegativeProb"]= float(1)/(zeroCardinality+wordDict[key]["negative"]+wordDict[key]["nNegative"])			
	return wordDict

def getLabelProbability(trainingData):
	positiveCount=0
	negativeCount=0
	trainLen = len(trainingData)
	for row in trainingData:
		if row[2] in "Positive":
			positiveCount+=1
		else:	
			negativeCount+=1	
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