class LogClass:
    logPath=""
    def __init__(self,logPath):
        self.logPath = logPath

def getPath():
	return LogClass.logPath

def setPath(path):
	LogClass.logPath = path