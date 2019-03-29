import csv
import re
import json
#import nltk
#from nltk.stem.porter import *
import numpy as np
from numpy import genfromtxt
from train import beginTrain
from test import *
import math
import datetime
'''
file = open("winemag-data_first150k.csv")
reader = csv.reader(file)
'''

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


def tokenize(str):
	dataX = set()
	data = re.sub("[,.!?;:*()/%'\"]",'',str)
	data =data.lower().split(" ")
	for item in data:
		dataX.add(item)
	dataX = list(dataX)
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
	print(type(stopWords))
	with open("stanford_core_nlp_stopWords.txt") as sw:
		for word in sw:
			np.append(stopWords,word)
	return stopWords

def removeStopWords(tokens):
	pureTokens = np.array([])
	pureTokens = np.delete(tokens, stopWords)
	return pureTokens.tolist()


#stemmer = PorterStemmer()
i=0

positiveCount=0
negativeCount=0
startTime = datetime.datetime.now()
#readerList = np.array(list(reader))
for row in csv:
	if i ==0:		
		i=1
		continue
	if('???' not in row[1]):			
		tokenList = tokenize(row[1]) #Tokenization
		stopWords = getStopWords()  #Getting stop words
		#print(tokenList)
		pureTokens =removeStopWords(tokenList)  #Removal of Stop Words
		# try:
		# 	stemmedTokens = [stemmer.stem(pureToken.decode('UTF-8')) for pureToken in pureTokens]
		# 	stemmedTokens = [item.encode('ascii','ignore') for item in stemmedTokens]
		# except Exception as e:
		# 	print e	
		descriptionList.append(pureTokens)
		pointsList.append(row[0])
		np.append(pointsList, row[0])
		if int(row[0]) > 86:		
			positiveCount+=1
			labelList.append("Positive")
		else:	
			negativeCount+=1	
			labelList.append("Negative")

		#if i==50000:
		#	break
		i+=1
		print i		
#descriptionList = descriptionList.tolist()
#pointsList = pointsList.tolist()
#labelList = labelList.tolist()



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


