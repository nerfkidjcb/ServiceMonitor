import paramiko
import configparser

# Parse cfg.ini file
config = configparser.ConfigParser()
config.read('./cfg/cfg.ini')

def monitor_remote_usage(hostname, port, username, password):
    # Establish SSH connection
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, port=port, username=username, password=password)

     # Execute the command remotely to get CPU usage
    stdin, stdout, stderr = ssh_client.exec_command("top -bn1 | grep 'Cpu(s)'")
    cpu_output = stdout.read().decode()
    cpu_usage = cpu_output.split()[1] + " % CPU"

    # Execute the command remotely to get RAM usage
    stdin, stdout, stderr = ssh_client.exec_command("free -m | awk 'NR==2{print $3}' | tr -d '\n'") # Runs free command then parses the number in the 3rd column of the 2nd row (used Mem) then removes newline
    ram_output = stdout.read().decode()
    ram_used = ram_output


    stdin, stdout, stderr = ssh_client.exec_command("free -m | awk 'NR==2{print $2}' | tr -d '\n'") 
    ram_output = stdout.read().decode()
    ram_total = ram_output

    ram_usage = ram_used + "/" + ram_total + " MB RAM"
    

    # Return CPU and RAM usage
    print(cpu_usage, ram_usage)

    # Close the SSH connection
    ssh_client.close()

if __name__ == '__main__':
    remote_address = config['ssh']['ssh_address']
    remote_username = config['ssh']['ssh_username']
    remote_password = config['ssh']['ssh_password']

    # Extract hostname and port from the remote_address
    remote_hostname, remote_port = remote_address.split(':')

    monitor_remote_usage(remote_hostname, remote_port, remote_username, remote_password)
