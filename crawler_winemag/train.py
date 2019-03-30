from dictCount import *
import json

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


def beginTrain(trainingData, algorithm):
	vocabList, positiveCount, negativeCount = makeVocabList(trainingData)
	positiveProb, negativeProb = getLabelProbability(positiveCount, negativeCount) #prior probabilities
	if "Bernoulli" not in algorithm:
		positiveCount,negativeCount=0,0
		for row in trainingData:			
			if row[2] == "Positive":
				positiveCount+=len(row[0])
			else:	
				negativeCount+=len(row[0])	
	wordDict = makeDict(trainingData, vocabList)
	print "length of vocabList"+str(len(vocabList))

	wordDict = computeProbability(wordDict, positiveCount, negativeCount, len(vocabList), algorithm)
	with open("model.json","w") as file:
		json.dump(wordDict, file)
	return wordDict, positiveProb, negativeProb, len(vocabList), positiveCount, negativeCount

def computeProbability(wordDict, positiveCount, negativeCount, featureSize, algorithm):
	for key in wordDict:
		num, den = Fraction(wordDict[key]["positive"], positiveCount)		
		wordDict[key]["positiveProb"]= float(num+1)/(den+featureSize)

		num, den = Fraction(wordDict[key]["negative"], negativeCount)
		wordDict[key]["negativeProb"]= float(num+1)/(den+featureSize)
		if "Bernoulli" in algorithm:
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
		if row[2]=="Positive":
			positiveCount+=1
		else:
			negativeCount+=1			
		for word in row[0]:
			if word not in vocabList:
				vocabList.add(word)				
	return vocabList, positiveCount, negativeCount				