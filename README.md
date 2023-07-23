# Service Monitor - Version 1.2!
A repo for scripts that run on a local machine that will look out for systems of your choosing.
<br><br><br>

## Dependencies
### Make sure you have these Python modules installed by running `pip install -r requirements.txt`
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
- `requests`

<br><br><br>
## Configuration and Setup
Take a look at `cfg/example_cfg.ini` and create your own `cfg.ini` file in the same directory with matching fields
<br><br>
Currently, you can choose a two custom options: <br>
- `graphs`  Show graphical data <br>
- `verbose`  Print data to console in real time with severity (recommended)<br><br>

Other configuration options are commented in the example file

<br><br><br>


## Scripts
### Script 1: `monitorPing.py` [FUNCTIONING]
Indefinitely pings domains/hosts within the `domains_list` in config and graphs the ping for each domain in real time. Upon a missing response, a notification email is sent. Emails, graphs and console outputs can be configured. 

<br>

### Script 2: `resourceMonitor.py` [FUNCTIONING]
Using the `paramiko` library to ssh and run resource monitoring commands on a host. This script goes on to graph the CPU and RAM usage in real time for the chosen host

<br>

### Script 3: `websiteMonitor.py` [FUNCTIONING]
Using the `requests` library, this script will check that the configured domains/hosts are serving some html content. Similar to pingMonitor, but will check for a web page response, as opposed to a ping from the name server.

<br><br>
# Roadmap
- Enable specification of intervals in `/cfg/cfg.ini`
- Only silence duplicate emails from the same website in `websiteMonitor.py` so that if multiple websites go down, more than one of them gets emailed
- Configure email notification for a service going back up after being flagged as down
- Looking at monitoring the run queue of a host
- Open to suggestions!
