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


import re
import requests
import time as t
import configparser

# Include my own modules
from functions.sendEmail import Mailer
from functions.functions import Utils
from functions.customLogging import CustomLogger


def monitor_websites():  

    for website in websites:     

        if verbose:
            logger.printInfo(f"Checking {website}...")

        try:
            wget = requests.get(website).text
        
        except Exception as e:
            wget = ""
            if verbose:
                logger.printError(f"Failed to get {website}! Error: {e}")

        # Check if the website returned any html
        if (not re.search("<html", wget)) or wget == "":
            
            if not website in downSites:
                downSites[website] = t.time()

            # Only send mail if it has been 2 minutes of downtime
            if len(downSites) > 1:
                if (t.time() - downSites[website] > 120):
                    downSites[website] = t.time()


                    if emailNotify:
                        if (lastEmailSites[website] == []) or (t.time() - lastEmailSites[website] > 3600):
                            if verbose:
                                logger.printWarn(f"{website} is not serving html! Attempting to send email...")

                            res = email.sendMail("Website Failure", f"{website} is not serving content!")

                            if res:
                                if verbose:
                                    logger.printInfo("Email sent successfully!")
                                lastEmailSites[website] = t.time()

                            elif verbose:
                                logger.printError("Email failed to send! Please check your email settings in cfg.ini")

                        elif verbose:
                            logger.printWarn(f"{website} not serving content, and email notifications for it are on cooldown!")
                        

                    elif verbose:
                        logger.printWarn(f"{website} is not serving any content! Email notifications disabled.")

        elif wget != "":
            if verbose:
                logger.printInfo(f"{website} is up and serving content!")

            if website in downSites:
                downSites[website] = None

                if emailNotify:
                    
                    if verbose:
                        logger.printWarn(f"{website} is back up from before! Attempting to send email...")

                    res = email.sendMail("Website Back Up", f"{website} is back up and serving content!")

                    if res == True:
                        if verbose:
                            logger.printInfo("Email sent successfully!")                        

                    elif verbose:
                        logger.printError("Email failed to send! Please check your email settings in cfg.ini. \n Error: \n {res}")                

                elif verbose:
                    logger.printWarn(f"{website} is back up! Email notifications disabled.")



if __name__ == "__main__":

    email = Mailer()
    logger = CustomLogger()
    util = Utils()

    util.checkCfg()

    # Parse cfg.ini file
    config = configparser.ConfigParser()
    config.read('./cfg/cfg.ini')

    # Check it was read correctly
    if config['websites']['website_list'] == "":
        logger.printError("No websites found in cfg.ini")
        exit()

    websites = config['websites']['website_list'].split(",")

    # Are we in verbose mode
    verbose = config['ui']['verbose'].lower() == "true"

    # Is email enabled
    emailNotify = config['email']['email_notify'].lower() == "true"

    # Remove any whitespace and update the list elements
    for i, website in enumerate(websites):
        websites[i] = website.strip()

        # If there's no http:// or https://, add https://
        if not re.search("http", websites[i]):
            websites[i] = f"https://{websites[i]}"

    # Keep track of the last time we sent an email per website
    lastEmailSites = {website: [] for website in websites}
    # Keep track of anything down, so we can notify if back up
    downSites = {}

    print("Done! \n \n ")

    if verbose:
        logger.printInfo("Verbose mode enabled. Running in verbose mode... (Check cfg.ini to disable verbose mode)")

    else:
        logger.printInfo("Verbose mode disabled. Running in quiet mode... (Check cfg.ini to enable verbose mode)")

    if emailNotify:
        logger.printInfo("Email notifications enabled. Running in email mode... (Check cfg.ini to disable email notifications)")

    else:
        logger.printInfo("Email notifications disabled. Running without them... (Check cfg.ini to enable email notifications)")

    print()
    # Start the main loop
    while True:
        monitor_websites()
        t.sleep(60)
