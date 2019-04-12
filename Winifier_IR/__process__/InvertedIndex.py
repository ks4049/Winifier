from __preprocess__.Preprocess import *
import numpy as np


vocabDict={}

def buildInvertedIndex(stemmedTokens, reviewID):
	for word in stemmedTokens:		
		if word not in vocabDict:
			vocabDict[word]=[reviewID]
		else:
			postingList = vocabDict[word]
			if reviewID not in postingList:
				postingList.append(reviewID)
				vocabDict[word] = postingList
	print(BUILD_INVERTED_INDEX_SUCCESS)

def printInvertedIndex():
	print("Inverted Index")
	print(vocabDict)

def searchPhrase(phraseQuery, boolOp):
	print(vocabDict)	
	preProcessCheck,stemmedTokens = preprocess(phraseQuery)
	if(preProcessCheck):
		if boolOp.lower()=="and":
			check, reviewsList = searchAnd(stemmedTokens)
		elif boolOp.lower()=="or":
			check, reviewsList = searchOr(stemmedTokens)
		if check:
			print("The phrase is present in the following reviews")
			print(reviewsList)			

def searchAnd(stemmedTokens):
	try:		
		term1 = stemmedTokens[0]
		if term1 in vocabDict:			
			resultList = np.array(vocabDict[term1])
			for counter in range(1,len(stemmedTokens)):
				if stemmedTokens[counter] in vocabDict:
					postingList2 = np.array(vocabDict[stemmedTokens[counter]])
					resultList =np.intersect1d(resultList, postingList2)
			print(BOOL_OPERATION_SUCCESS)				
			return True, list(resultList)												
		else:
			print(BOOL_OPERATION_ERROR)
			return False, None	
	except:
		print(BOOL_OPERATION_ERROR)
		return False, None

def searchOr(stemmedTokens):
	resultSet= set()
	try:
		for token in stemmedTokens:
			if token in vocabDict:
				postingList = vocabDict[token]
				for reviewID in postingList:
					resultSet.add(reviewID)
		if len(resultSet) > 0:					
			print(BOOL_OPERATION_SUCCESS)					
			return  True,list(resultSet)
		else:
			print(BOOL_OPERATION_ERROR)
			return False, None 	
	except:
		print(BOOL_OPERATION_ERROR)
		return False, None
