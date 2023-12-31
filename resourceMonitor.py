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
print("Welcome to the Resource Monitor tool! Please make sure you are running the latest version from GitHub.")
print("Initialising...")

import paramiko
import time as t
import configparser
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from datetime import datetime

# Include my own modules
from functions.customLogging import CustomLogger
from functions.functions import Utils


def connect_to_host(hostname, port, username, password):
    # Establish SSH connection
    if verbose:
        logger.printInfo("Attempting connection to host...")
        
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh_client.connect(hostname, port=port, username=username, password=password, timeout=20)
        
    except TimeoutError as e:
        
        logger.printError("Connection timed out: " + str(e))
        logger.printError("Aborting, please check your SSH credentials in cfg.ini and your host's configuration")
        return False
        

    # Check if the connection was successful
    if ssh_client.get_transport().is_active() == False:
        logger.printError("SSH connection failed, please check your credentials in cfg.ini and your host's settings")
        return False
    
    return ssh_client



def read_usage(ssh_client):
    # Execute the command remotely to get CPU usage
    stdin, stdout, stderr = ssh_client.exec_command("top -bn1 | grep 'Cpu(s)'")
    cpu_output = stdout.read().decode()
    cpu_usage = float(cpu_output.split()[1])

    # Execute the command remotely to get RAM usage
    stdin, stdout, stderr = ssh_client.exec_command("free -m | awk 'NR==2{print $3}' | tr -d '\n'") # Runs free command then parses the number in the 3rd column of the 2nd row (used Mem) then removes newline
    ram_output = stdout.read().decode()
    ram_used = int(ram_output)


    stdin, stdout, stderr = ssh_client.exec_command("free -m | awk 'NR==2{print $2}' | tr -d '\n'") 
    ram_output = stdout.read().decode()
    ram_total = ram_output

    ram_usage = str(round((ram_used / int(ram_total)) * 100, 2))
    
    string_usage = str(cpu_usage) + "% CPU  | " + ram_usage + "% RAM"

    return string_usage, cpu_usage, ram_usage



def update_graph():
    # Set the x-axis locator and formatter
    locator = mdates.MinuteLocator(interval=30)  # Display 30-minute intervals
    formatter = mdates.DateFormatter('%H:%M')  # Format the x-axis labels as HH:MM

    # Plot the data
    ax1.clear()
    ax1.plot(time_list, cpu_usage_list, label="CPU Usage (%)", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)
    ax1.legend(loc="upper left")

    # Plot the data on the second axes
    ax2.clear()
    ax2.plot(time_list, ram_usage_list, label="RAM Usage (MB)", color="green")
    ax2.legend(loc="upper right")

    # Set the x-axis label, y-axis label, and plot title
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Resource Usage")
    ax1.set_title("Resource Usage Monitor for " + config['ssh']['host_nickname'])

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')



def monitor_remote_usage(hostname, port, username, password):
    now = datetime.now()
    now = now.strftime("%H:%M")

    ssh_client = connect_to_host(hostname, port, username, password)

    if ssh_client == False:
        # Skip on, we don't want this to shut off if we cant connect once
        return
    
    usage, cpu_used, ram_used = read_usage(ssh_client)
    ssh_client.close()

    # Return CPU and RAM usage
    if verbose:
        logger.printInfo(usage)    

    # Append the usage to a rolling list if the length is less than 288 (24 hours in 5 minute intervals)
    if len(cpu_usage_list) < 288:
        cpu_usage_list.append(cpu_used)
        ram_usage_list.append(ram_used)
        time_list.append(now)

    else:
        # Clear out the first element
        cpu_usage_list.pop(0)
        ram_usage_list.pop(0)
        time_list.pop(0)
        cpu_usage_list.append(cpu_used)
        ram_usage_list.append(ram_used)
        time_list.append(now)
  
    

def animate(i):
    monitor_remote_usage(remote_hostname, remote_port, remote_username, remote_password)
    update_graph()



if __name__ == '__main__':    

    logger = CustomLogger()
    util = Utils()

    util.checkCfg()

    # Parse cfg.ini file
    config = configparser.ConfigParser()
    config.read('./cfg/cfg.ini')

    # Are we in verbose mode
    verbose = config['ui']['verbose'].lower() == "true"

    # Are we in GUI mode
    makeGraphs = config['ui']['graphs'].lower() == "true"

    if makeGraphs:
        # Set up the plot
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        # Create a twin axes
        ax2 = ax1.twinx()

    cpu_usage_list = []
    ram_usage_list = []
    time_list = []

    remote_address = config['ssh']['ssh_address']
    remote_username = config['ssh']['ssh_username']
    remote_password = config['ssh']['ssh_password']

    # Extract hostname and port from the remote_address
    remote_hostname, remote_port = remote_address.split(':')
    
    print("Done! \n \n")

    if verbose:
        logger.printInfo("Verbose mode enabled. Running in verbose mode... (Check cfg.ini to disable verbose mode)")

    else :
        logger.printInfo("Verbose mode disabled. Running in quiet mode... (Check cfg.ini to enable verbose mode)")


    if makeGraphs:
        logger.printInfo("Graphs enabled. Running in GUI mode... (Check cfg.ini to disable graphs)")
        print()
        ani = animation.FuncAnimation(fig, animate, interval=60000, cache_frame_data=False)
        plt.show()

    else:
        logger.printInfo("Graphs disabled. Running in CLI mode... (Check cfg.ini to enable graphs)")
        print()
        while True:
            monitor_remote_usage(remote_hostname, remote_port, remote_username, remote_password)
            t.sleep(60)
    
