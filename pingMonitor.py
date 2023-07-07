import os
import re
import time as t
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import configparser

# Include email script
import sys
sys.path.append('./functions/')
import sendEmail as email

# Parse cfg.ini file
config = configparser.ConfigParser()
config.read('./cfg/cfg.ini')
domains = config['domains']['domain_list'].split(",")

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
        
        # Run shell but store the output
        os.system("ping " + domain + " > ping_output.txt")        

        with open("ping_output.txt", "r") as f:
            output = f.read()

        # Parse the output to get the average ping time
        match = re.search(r"Average = (\d+)ms", output)

        if match:
            ping_time = float(match.group(1))
            ping_times[domain].append(str(ping_time) + "|" + str(now))
            print(f"{domain} is up! Average ping time: {ping_time} ms")

        else: # If the ping failed there won't be an average time            

            # Graph a 0 ping time to see drop outs
            ping_times[domain].append(0 + "|" + str(now))
            if config['email']['email_notify'].lower() == "true": 

                print(f"{domain} is down! Attempting to send email...")
                if t.time() - lastEmailTime > 3600:
                    email.sendMail("Ping Failure", f"{domain} is unreachable!")
                lastEmailTime = t.time()
            else:
                print(f"{domain} is down! Email notifications disabled.")


    # Append ping time to rolling list
    for domain, times in ping_times.items():
        if len(times) > 1440: #1440 minutes in a day
            ping_times[domain, now] = times[-1440:]


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

ani = animation.FuncAnimation(fig, animate, interval=30000, cache_frame_data=False)
plt.show()
