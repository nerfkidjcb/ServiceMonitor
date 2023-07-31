import time

class CustomLogger:
    
    def _getCurrentDateAndTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def printInfo(self, message):
        print("\033[94m" + self._getCurrentDateAndTime() + " [INFO] \033[0m" + message)

    def printWarn(self, message):
        print("\033[93m" + self._getCurrentDateAndTime() + " [WARN] \033[0m" + message)

    def printError(self, message):
        print("\033[91m" + self._getCurrentDateAndTime() + " [ERROR] \033[0m" + message)
