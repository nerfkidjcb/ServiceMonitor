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
print("Welcome to the Ping Monitor tool!")
print("Initialising...")

from math import fabs
import os
import platform
import re
import time as t
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
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
if config['domains']['domain_list'] == "":
    log.printError("No domains found in cfg.ini")
    exit()

domains = config['domains']['domain_list'].split(",")

# Are we in verbose mode
verbose = config['ui']['verbose'].lower() == "true"

# Are we in GUI mode
makeGraphs = config['ui']['graphs'].lower() == "true"

if makeGraphs:
    # Set up the plot
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)



# Hold a list of ping times for each domain over the last 500 pings
ping_times = {domain: [] for domain in domains}

# Keep track of the last time we sent an email so we don't spam
lastEmailTime = 0

def animate(i):    
    global lastEmailTime
    # Even though this will make some requests slightly different times we need to 
    # plot them together
    now = datetime.now()
    now = now.strftime("%H:%M")

    for domain in domains:
        
        if platform.system().lower() == "windows":
    
            # Run shell but store the output
            os.system("ping " + domain + " > win_ping_output.txt")        
    
            with open("win_ping_output.txt", "r") as f:
                output = f.read()
    
            # Parse the output to get the average ping time
            res = re.search(r"Average = (\d+)ms", output)
            if res:
                ping_time = res.group(1)

            else:
                ping_time = False

        else:
            # We on linux
            command = f"ping -c 4 {domain}"
            ping_output = os.popen(command).read()

            # Extract ping times using regular expression
            time_pattern = r"time=([\d.]+)"
            res_ping_times = re.findall(time_pattern, ping_output)

            if len(res_ping_times) != 0:              
                # Calculate average time
                ping_time = int(sum(float(time) for time in res_ping_times) / len(ping_times))
                
            else:
                ping_time = False

        if ping_time:
            ping_times[domain].append(str(ping_time) + "|" + str(now))

            if verbose:
                log.printInfo(f"{domain} is up! Average ping time: {ping_time} ms")

        else: # If the ping failed there won't be an average time            

            # Graph a 0 ping time to see drop outs
            ping_times[domain].append(str(0) + "|" + str(now))

            if config['email']['email_notify'].lower() == "true": 

                if verbose:
                    log.printWarn(f"{domain} is down! Attempting to send email...")

                if t.time() - lastEmailTime > 3600:
                    email.sendMail("Ping Failure", f"{domain} is unreachable!")
                lastEmailTime = t.time()

            else:
                if verbose:
                    log.printWarn(f"{domain} is down! Email notifications disabled.")


    # Append ping time to rolling list
    for domain, times in ping_times.items():
        if len(times) > 1440: #1440 minutes in a day
            ping_times[domain, now] = times[-1440:]


    if makeGraphs:
        # Clear the current plot
        ax1.clear()

        for domain, times in ping_times.items():
            # Plot the two columns in times against each other
            dates = [datetime.strptime(time.split("|")[1], "%H:%M") for time in times]
            ping_numbers = [float(time.split("|")[0]) for time in times]     

            ax1.plot(dates, ping_numbers, label=domain)

        # Set the x-axis locator and formatter
        locator = mdates.MinuteLocator(interval=15)  # Display 15-minute intervals
        formatter = mdates.DateFormatter('%H:%M')  # Format the x-axis labels as HH:MM
        ax1.xaxis.set_major_locator(locator)
        ax1.xaxis.set_major_formatter(formatter)

        ax1.set_xlabel("Time")
        ax1.set_ylabel("Ping Time (ms)")
        ax1.legend()

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')


print("Done! \n \n ")

if verbose:
    log.printInfo("Verbose mode enabled. Running in verbose mode... (Check cfg.ini to disable verbose mode)")

else:
    log.printInfo("Verbose mode disabled. Running in quiet mode... (Check cfg.ini to enable verbose mode)")

    
if makeGraphs:
    log.printInfo("Graphs enabled. Running in GUI mode... (Check cfg.ini to disable graphs)")
    print()
    ani = animation.FuncAnimation(fig, animate, interval=30000, cache_frame_data=False)
    plt.show()

else:
    log.printInfo("Graphs disabled. Running in CLI mode... (Check cfg.ini to enable graphs)")
    print()
    while True:
        animate(0)
        t.sleep(30)
