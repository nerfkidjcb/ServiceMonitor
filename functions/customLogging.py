import time

def getCurrentDateAndTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def printInfo(message):
    print("\033[94m" + getCurrentDateAndTime() + " [INFO] \033[0m" + message)

def printWarn(message):
    print("\033[93m" + getCurrentDateAndTime() + " [WARN] \033[0m" + message)

def printError(message):
    print("\033[91m" + getCurrentDateAndTime() + " [ERROR] \033[0m" + message)