def makeDict(trainingData, vocabList):
	vocabDict = initializeDict(vocabList)
	for row in trainingData:		
		#Updating the keys in dictionary
		for key in vocabDict:			
			if row[2]=="Positive":					
				vocabDict[key]["nPositive"]+=1
			else:
				vocabDict[key]["nNegative"]+=1			
		for word in row[0]:
			if word in vocabDict:			
				if row[2]=="Positive":
					vocabDict[word]["positive"]+=1
					vocabDict[word]["nPositive"]-=1
				else:
					vocabDict[word]["negative"]+=1
					vocabDict[word]["nNegative"]-=1		
	return vocabDict							
					
def initializeDict(vocabList):	
	vocabDict={}	
	for word in vocabList:		
		initialDict = {
		"positive":0,
		"negative":0,
		"nPositive":0,
		"nNegative":0
		}
		vocabDict[word]=initialDict
	return vocabDict













