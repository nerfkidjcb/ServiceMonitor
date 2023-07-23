# Utils for the project

import os 
import sys

# Include my own modules
sys.path.append('./functions/')
import customLogging as log

def checkCfg():
    """Check if the configuration file exists"""
    if not os.path.exists("./cfg/cfg.ini"):
        log.printError("No cfg.ini file found, please create one from the example file in the cfg folder.")
        log.printError("Aborting...")
        exit()
       
    return True