def makeDict(trainingData, vocabList):
	vocabDict = initializeDict(vocabList)
	for row in trainingData:						
		for word in row[0]:
			if word in vocabDict:			
				if row[2]=="Positive":
					vocabDict[word]["positive"]+=1
				else:
					vocabDict[word]["negative"]+=1				
	return vocabDict							
					
def initializeDict(vocabList):	
	vocabDict={}	
	for word in vocabList:		
		initialDict = {
		"positive":0,
		"negative":0,		
		}
		vocabDict[word]=initialDict
	return vocabDict













