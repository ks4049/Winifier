import json
import sys, traceback
import yaml
sys.path.insert(0, './__util__')
from Constants import *

def modelParser(model):
	print(MODEL_PARSE_BEGIN_MESSAGE)
	data = None
	try:
		data = model

		algorithm = data["algorithm"]
		if algorithm == B_ALGORITHM:
			pass
		elif algorithm == M_ALGORITHM:
			pass
		else:
			print(MODEL_PARSE_ERROR_MESSAGE)
			return False, None
		trainType = str(data["trainType"])
		if trainType == PS_TRAIN_TYPE:
			percentageSplit = int(data["percentageSplit"])
			if ((percentageSplit > 0) and (percentageSplit < 100)):
				pass
			else:
				print(MODEL_PARSE_ERROR_MESSAGE)
				return False, None
		elif trainType == CV_TRAIN_TYPE:
			numOfFolds = int(data["numberOfFolds"])
			if numOfFolds > 0:
				pass
			else:
				print(MODEL_PARSE_ERROR_MESSAGE)
				return False, None
		if trainType==PS_TRAIN_TYPE:		
			vocabSize = int(data["vocabSize"])
			if vocabSize > 0:
				pass	
			else:	
				print(MODEL_PARSE_ERROR_MESSAGE)
				return False, None

		trainDatasetSize = int(data["trainDatasetSize"])
		if trainDatasetSize > 0:
			pass
		else:
			print(MODEL_PARSE_ERROR_MESSAGE)
			return False, None

		
		wordDict = yaml.load(data["probability"])		

		if not wordDict:
			print(MODEL_PARSE_ERROR_MESSAGE)
			return False, None

		print(MODEL_PARSE_SUCCESS_MESSAGE)
		return True, algorithm
	except Exception as e:
		print(e)
		print(MODEL_PARSE_ERROR_MESSAGE)
		return False
