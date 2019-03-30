import csv
import re
import json
import nltk
from nltk.stem.porter import *
import numpy as np
from numpy import genfromtxt
from train import beginTrain
from test import *
import math
import datetime
from train import Fraction
'''
file = open("winemag-data_first150k.csv")
reader = csv.reader(file)
'''
print Fraction(5,35)
print Fraction(28,70)
print Fraction(70,15)
csv = genfromtxt('data_temp_tab.txt',delimiter='~',dtype='<S')
j=0
#print(rat)

for i in range(0,len(csv)):
	if csv[i,1].item().decode()!="???":
		csv[i,1].item().decode()

descriptionList = []
pointsList = []
labelList = []
trainingData = []
testData = []

stopWords = np.array([])
stemmedTokens=[]
vocabList = set()
negativeProb=20
positiveProb=15
vocabDict = {}


def tokenize(str, algorithm):
	data = re.sub("[,.!?;:*()/%'\"]",'',str)
	data =data.lower().split(" ")
	if "Bernoulli" in algorithm:
		dataX = set()
		for item in data:
			dataX.add(item)
		dataX = list(dataX)
	else:
		dataX = data
	return np.array(dataX)        

def createTraining():
	trainLen = (int)(0.9*len(descriptionList))
	for i in range(0, trainLen):
		trainingList =[]
		trainingList.append(descriptionList[i])
		trainingList.append(pointsList[i])
		trainingList.append(labelList[i])
		trainingData.append(trainingList)

def createTest():	
	testLen = (int)(math.ceil(0.1*len(descriptionList)))
	for i in range(len(descriptionList)-testLen, len(descriptionList)):
		testList =[]
		testList.append(descriptionList[i])
		testList.append(pointsList[i])
		testList.append(labelList[i])
		testData.append(testList)	
		
def getStopWords():
	tempStopWords=""
	with open("stanford_core_nlp_stopWords.txt", "r") as sw:		
		sw = sw.readlines()	
		for word in sw:
			tempStopWords+=word
	tempStopWords = re.sub("['\"]",'\n',tempStopWords)
	stopList = tempStopWords.split("\n")
	return np.array(stopList)

def removeStopWords(tokens):
	pureTokens = np.array([])
	pureTokens = np.setdiff1d(tokens, stopWords)
	return pureTokens.tolist()



stemmer = PorterStemmer()
i=0

positiveCount=0
negativeCount=0
startTime = datetime.datetime.now()
algorithm = "Multinominal"
#readerList = np.array(list(reader))
stopWords = getStopWords()  #Getting stop words
for row in csv:
	if i ==0:		
		i=1
		continue
	if('???' not in row[1]):
		#Tokenization			
		tokenList = tokenize(row[1], algorithm) 
		#Removal of Stop Words
		pureTokens =removeStopWords(tokenList)  
		#Stemming
	 	stemmedTokens = [stemmer.stem(pureToken.decode('UTF-8')) for pureToken in pureTokens]
	 	stemmedTokens = [item.encode('ascii','ignore') for item in stemmedTokens]
		descriptionList.append(stemmedTokens)
		pointsList.append(row[0])
		np.append(pointsList, row[0])
		if int(row[0]) > 86:		
			labelList.append("Positive")
		else:	
			labelList.append("Negative")

		if i==20000:
			break
		i+=1
#descriptionList = descriptionList.tolist()
#pointsList = pointsList.tolist()
#labelList = labelList.tolist()

createTraining()
createTest()
vocabDict, positiveProb, negativeProb, featureSize, positiveCount, negativeCount = beginTrain(trainingData, algorithm)
predictedValues = getResult(testData,vocabDict, positiveProb, negativeProb, positiveCount, negativeCount, featureSize, algorithm)
print json.dumps(predictedValues)
formConfusionMatrix(testData, predictedValues)
endTime = datetime.datetime.now()
print
print "Time taken"
print endTime-startTime


