import json
import sys
sys.path.insert(0, './__util__')
from Constants import *
sys.path.insert(0, './__train__')
from Dictionary import *

def computeHCF(x, y):
    # choose the smaller number
    if x > y:
        smaller = y
    else:
        smaller = x
    for i in range(1, smaller+1):
        if((x % i == 0) and (y % i == 0)):
            hcf = i
    return hcf

def Fraction(num, den):
	if(num==0):
		return num, den
	elif(num != den):
		return num/computeHCF(num, den), den/computeHCF(num ,den)
	else:
		return 1,1

def beginTrainingProcess(trainingData, algorithm):
	message=""
	output=""
	try:
		message+=BEGIN_TRAINING_MESSAGE+'\n'
		print (BEGIN_TRAINING_MESSAGE)
		vocabList, positiveCount, negativeCount = makeVocabList(trainingData)
		positiveProb, negativeProb = getLabelProbability(positiveCount, negativeCount) #prior probabilities
		if algorithm == M_ALGORITHM:
			positiveCount,negativeCount=0,0
			for row in trainingData:
				if row[2] == POSITIVE_LABEL:
					positiveCount+=len(row[0])
				else:
					negativeCount+=len(row[0])
		output+="Vocabulary\n"+str(vocabList)+'\n'
		wordDict = makeDict(trainingData, vocabList)
		message+="Vocabulary List Size: "+str(len(vocabList))+'\n'
		print ("Vocabulary List Size: "+str(len(vocabList)))
		wordDict = computeProbability(wordDict, positiveCount, negativeCount, len(vocabList), algorithm)
		return wordDict, positiveProb, negativeProb, len(vocabList), positiveCount, negativeCount, message, output
	except:
		message+=TRAINING_ERROR_MESSAGE+'\n'
		print(TRAINING_ERROR_MESSAGE)
		return None, None, None, None, None, None, message, output

def computeProbability(wordDict, positiveCount, negativeCount, featureSize, algorithm):
	for key in wordDict:
		num, den = Fraction(wordDict[key]["positive"], positiveCount)
		wordDict[key]["positiveProb"]= float(num+1)/(den+featureSize)

		num, den = Fraction(wordDict[key]["negative"], negativeCount)
		wordDict[key]["negativeProb"]= float(num+1)/(den+featureSize)
		if B_ALGORITHM in algorithm:
			wordDict[key]["nPositiveProb"]= float(1-wordDict[key]["positiveProb"]);
			wordDict[key]["nNegativeProb"]= float(1-wordDict[key]["negativeProb"]);
	return wordDict

def getLabelProbability(positiveCount, negativeCount):
	trainLen = positiveCount+negativeCount
	positiveProb = float(positiveCount)/trainLen
	negativeProb = 1-positiveProb
	return positiveProb, negativeProb

def makeVocabList(trainingData):
	vocabList = set()
	positiveCount,negativeCount=0,0
	for row in trainingData:
		if row[2]==POSITIVE_LABEL:
			positiveCount+=1
		else:
			negativeCount+=1
		for word in row[0]:
			if word not in vocabList:
				vocabList.add(word)
	return vocabList, positiveCount, negativeCount
