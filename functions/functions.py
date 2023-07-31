# Utils for the project

import os 
import sys

# Include my own modules
sys.path.append('./functions/')
from customLogging import CustomLogger
logger = CustomLogger()

def checkCfg():
    """Check if the configuration file exists"""
    if not os.path.exists("./cfg/cfg.ini"):
        logger.printError("No cfg.ini file found, please create one from the example file in the cfg folder.")
        logger.printError("Aborting...")
        exit()
       
    return True