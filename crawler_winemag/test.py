import math

def getResult(testData, vocabDict, positivePrior, negativePrior):
	testOutput = {}
	i=0			
	for row in testData:
		for key in vocabDict:
			actualPos = 1
			actualNeg = 1
			label = None
			if key in row[0]:
				positiveProb= vocabDict[key]["positiveProb"]
				actualPos += math.log10(positiveProb)
				negativeProb = vocabDict[key]["negativeProb"]
				actualNeg += math.log10(negativeProb)
			else:
				nPositiveProb = vocabDict[key]["nPositiveProb"]
				actualPos += math.log10(nPositiveProb)
				nNegativeProb = vocabDict[key]["nNegativeProb"]		
				actualNeg += math.log10(nNegativeProb)			
			try:
				actualPos+=math.log10(positivePrior)				
			except:
				pass			
			try:
				actualNeg+=math.log10(negativePrior)					
			except:
				pass							
		actualPos = actualPos/(actualPos+actualNeg)
		actualNeg = actualNeg/(actualPos+actualNeg)			
		if(actualPos>actualNeg):
			label = "positive"
		else:
			label = "negative"
		testOutput[i] = {
		"positive": actualPos,
		"negative": actualNeg,
		"label":label
		}		
		i+=1
	return testOutput


