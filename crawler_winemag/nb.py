import csv
import re
import json
#import nltk
#from nltk.stem.porter import *
#import numpy as np
from train import beginTrain
from test import *
import math
import datetime

file =open("winemag-data_first150k.csv")
reader = csv.reader(file)
descriptionList =[]
pointsList = []
labelList =[]
trainingData = []
testData = []

stopWords = []
stemmedTokens=[]
vocabList = set()
negativeProb=20
positiveProb=15
vocabDict = {}


def tokenize(str):
	dataX = set()
	data = re.sub('[,.!?;:*()/%]','',str)
	data =data.lower().split(" ")
	for item in data:
		dataX.add(item)
	return dataX	           

def createTraining():
	trainLen = (int)(0.8*len(descriptionList))
	for i in range(trainLen):
		trainList =[]
		trainList.append(descriptionList[i])
		trainList.append(pointsList[i])
		trainList.append(labelList[i])
		trainingData.append(trainList)	

def createTest():	
	testLen = (int)(math.ceil(0.2*len(descriptionList)))
	for i in range(len(descriptionList)-testLen, len(descriptionList)):
		testList =[]
		testList.append(descriptionList[i])
		testList.append(pointsList[i])
		testList.append(labelList[i])
		testData.append(testList)	
		
def getStopWords():
	with open("stanford_core_nlp_stopWords.txt") as sw:
		for word in sw:
			stopWords.append(word)

def removeStopWords(tokens):
	pureTokens = []
	for item in tokens:
		if item not in stopWords:
			pureTokens.append(item)

	return pureTokens




#stemmer = PorterStemmer()
i=0

positiveCount=0
negativeCount=0
startTime = datetime.datetime.now()
readerList = list(reader)
for row in readerList:
	if i ==0:		
		i=1
		continue			
	tokenList = tokenize(row[2]) #Tokenization
	getStopWords()  #Getting stop words
	pureTokens =removeStopWords(tokenList)  #Removal of Stop Words
	# try:
	# 	stemmedTokens = [stemmer.stem(pureToken.decode('UTF-8')) for pureToken in pureTokens]
	# 	stemmedTokens = [item.encode('ascii','ignore') for item in stemmedTokens]
	# except Exception as e:
	# 	print e	
	descriptionList.append(pureTokens)
	pointsList.append(row[4])
	if int(row[4]) > 90:		
		positiveCount+=1
		labelList.append("Positive")
	else:	
		negativeCount+=1	
		labelList.append("Negative")
	if i==1000:
		break
	i+=1		
									
createTraining()
createTest()
vocabDict, positiveProb, negativeProb, featureSize = beginTrain(trainingData, positiveCount, negativeCount)
predictedValues = getResult(testData,vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize)
print json.dumps(predictedValues)
formConfusionMatrix(testData, predictedValues)
endTime = datetime.datetime.now()
print
print "Time taken"
print endTime-startTime




