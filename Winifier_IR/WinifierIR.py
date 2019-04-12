import sys
from __data__.Load import *
from __preprocess__.Preprocess import preprocess
from __util__.Constants import *
from __process__.InvertedIndex import *

def __init__(params):
	setPath(".")	
	filePath = params[1]
	limit = int(params[2])
	check, data = load(filePath,limit)
	counter=0  
	if check:  
		for row in data:
			if UNDEFINED_INSTANCE not in str(row[0]):
				preProcessCheck,stemmedTokens= preprocess(row[0])
				if preProcessCheck:
					buildCheck = buildInvertedIndex(stemmedTokens,counter)
					counter+=1
				else:
					print(PREPROCESS_ERROR_MESSAGE)
					break
			else:
			 	counter+=1
			print(SEPARATOR)
		printInvertedIndex()	
		phraseQuery = params[3]
		booleanOperation= params[4]
		searchPhrase(phraseQuery, booleanOperation)	
	else:
		print("Loading Error")


__init__(sys.argv)
