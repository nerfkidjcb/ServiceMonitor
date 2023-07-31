# Utils for the project

import os 
import sys

class Utils:

    def __init__(self):        
        # Include my own modules
        from functions.customLogging import CustomLogger
        self.logger = CustomLogger()

    def checkCfg(self):
        """Check if the configuration file exists"""
        if not os.path.exists("./cfg/cfg.ini"):
            self.logger.printError("No cfg.ini file found, please create one from the example file in the cfg folder.")
            self.logger.printError("Aborting...")
            exit()
        
        return True