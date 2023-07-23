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
import requests
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

# Keep track of the last time we sent an email so we don't spam
lastEmailTime = 0


def monitor_websites():  

    for website in websites:
        # Remove any whitespace
        website = website.strip()

        # If theres no http:// or https://, add it
        if not (re.search("https", website) or re.search("http", website)):
            website = "https://" + website
        

        if verbose:
            log.printInfo(f"Checking {website}...")

        # request the website
        try:
            wget = requests.get(website).text
        
        except:
            log.printError(f"Failed to connect to {website}! Skipping...")
            wget = ""

        # check if the website returned any html
        if (not re.search("<html", wget)) or wget == "":
            if emailNotify:
                if t.time() - lastEmailTime > 3600:
                    if verbose:
                        log.printWarn(f"{website} is not servings html! Attempting to send email...")

                    res = email.sendMail("Website Failure", f"{website} is unreachable!")

                    if res:
                        if verbose:
                            log.printInfo("Email sent successfully!")
                        lastEmailTime = t.time()

                    elif verbose:
                        log.printError("Email failed to send! Please check your email settings in cfg.ini")

                elif verbose:
                    log.printWarn("Email notifications are on cooldown!")

                

            elif verbose:
                log.printWarn(f"{website} is not serving any content! Email notifications disabled.")

        elif wget != "":
            if verbose:
                log.printInfo(f"{website} is up and serving content!")



print("Done! \n \n ")

if verbose:
    log.printInfo("Verbose mode enabled. Running in verbose mode... (Check cfg.ini to disable verbose mode)")

else:
    log.printInfo("Verbose mode disabled. Running in quiet mode... (Check cfg.ini to enable verbose mode)")

if emailNotify:
    log.printInfo("Email notifications enabled. Running in email mode... (Check cfg.ini to disable email notifications)")

else:
    log.printInfo("Email notifications disabled. Running without them... (Check cfg.ini to enable email notifications)")

print()
# Start the main loop
while True:
    monitor_websites()
    t.sleep(60)
