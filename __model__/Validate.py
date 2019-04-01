import json
import sys, traceback
sys.path.insert(0, './__util__')
from Constants import *

def modelParser(model):
	print(MODEL_PARSE_BEGIN_MESSAGE)
	data = None
	try:
		data = model

		algorithm = str(data["algorithm"])
		if algorithm == B_ALGORITHM:
			pass
		elif algorithm == M_ALGORITHM:
			pass
		else:
			print(MODEL_PARSE_ERROR_MESSAGE)
			return False

		vocabSize = int(data["vocabSize"][0])
		if vocabSize > 0:
			pass
		else:
			print(MODEL_PARSE_ERROR_MESSAGE)
			return False

		trainDatasetSize = int(data["trainDatasetSize"])
		if trainDatasetSize > 0:
			pass
		else:
			print(MODEL_PARSE_ERROR_MESSAGE)
			return False

		trainType = str(data["trainType"])
		if trainType == PS_TRAIN_TYPE:
			percentageSplit = int(str(data["percentageSplit"]))
			if ((percentageSplit > 0) and (percentageSplit < 100)):
				pass
			else:
				print(MODEL_PARSE_ERROR_MESSAGE)
				return False
		elif trainType == CV_TRAIN_TYPE:
			numOfFolds = int(str(data["numOfFolds"]))
			if numOfFolds > 0:
				pass
			else:
				print(MODEL_PARSE_ERROR_MESSAGE)
				return False

		wordDict = data["probability"]

		if not wordDict:
			print(MODEL_PARSE_ERROR_MESSAGE)
			return False

		print(MODEL_PARSE_SUCCESS_MESSAGE)
		return True
	except:
		print(MODEL_PARSE_ERROR_MESSAGE)
		return False
