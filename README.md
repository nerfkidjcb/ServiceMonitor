# Service Monitor - Version 0.1
A repo for scripts that run on a local machine that will look out for systems of your choosing.
<br><br><br>

# Dependencies
### Make sure you have these Python modules installed by running `pip install requirements.txt`
- `matplotlib` - For plotting, of course
- `paramiko` - For ssh connections
  
### These libraries are also used, but should already be included in your Python installation:
- `os`
- `re`
- `time`
- `sys`
- `datetime`
- `smtplib`
- `configparser`

<br><br><br>
# Configuration
Take a look at `cfg/example_cfg.ini` and create your own `cfg.ini` file in the same directory with matching fields

<br><br><br>


# Scripts
## Script 1: `monitorPing.py` [IN-REVIEW]
Indefinitely pings domains within the `domains_list` in config and graphs the ping for each domain in real time. Upon a missing response, a notification email is sent

<br>

## Script 2: `webserverResourceMonitor.py` [IN-PROGRESS]
Using the `paramiko` library to ssh and run resource monitoring commands on a host of your choice. Will graph the cpu usage and display RAM usage updating every 5 minutes
