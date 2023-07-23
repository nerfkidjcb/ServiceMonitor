### Welcome
print(" ___________________________________________________________________________")
print("/                                                                           \ ")
print("|   ____                  _            __  __             _ _               |")
print("|  / ___|  ___ _ ____   _(_) ___ ___  |  \/  | ___  _ __ (_) |_ ___  _ __   |")
print("|  \___ \ / _ \ '__\ \ / / |/ __/ _ \ | |\/| |/ _ \| '_ \| | __/ _ \| '__|  |")
print("|   ___) |  __/ |   \ V /| | (_|  __/ | |  | | (_) | | | | | || (_) | |     |")
print("|  |____/ \___|_|    \_/ |_|\___\___| |_|  |_|\___/|_| |_|_|\__\___/|_|     |")
print("|                                                                           |")
print("\________________________________________________________________________ '\ ")
print("                                                                     ()    \\ ")
print("                                                                       O    \\  .")
print("                                                                         o  |\\/|")
print("                                                                            / ' '\ ")
print("                                                                            . .   . ")
print("                                                                           /    ) |")
print("                                                                          '  _.'  |")
print("                                                                          '-'/    \ ")
print()
print("Welcome to the Website Monitor tool! Please make sure you are running the latest version from GitHub.")
print()
print("Initialising...")
print()

import os
import platform
import re
import time as t
from datetime import datetime
import configparser

# Include my own modules
import sys
sys.path.append('./functions/')
import sendEmail as email
import functions as util

# Include logging script
import customLogging as log

util.checkCfg()

# Parse cfg.ini file
config = configparser.ConfigParser()
config.read('./cfg/cfg.ini')

# check it was read correctly
if config['websites']['website_list'] == "":
    log.printError("No websites found in cfg.ini")
    exit()

websites = config['websites']['website_list'].split(",")

# Are we in verbose mode
verbose = config['ui']['verbose'].lower() == "true"

# Is email enabled
emailNotify = config['email']['email_notify'].lower() == "true"


def monitor_websites():
    return


print("Done! \n \n ")

if verbose:
    log.printInfo("Verbose mode enabled. Running in verbose mode... (Check cfg.ini to disable verbose mode)")

else:
    log.printInfo("Verbose mode disabled. Running in quiet mode... (Check cfg.ini to enable verbose mode)")

if emailNotify:
    log.printInfo("Email notifications enabled. Running in email mode... (Check cfg.ini to disable email notifications)")

else:
    log.printInfo("Email notifications disabled. Running without them... (Check cfg.ini to enable email notifications)")

    
# Start the main loop
while True:
    monitor_websites()
    t.sleep(60)
