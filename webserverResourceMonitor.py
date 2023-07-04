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

    # Execute command to monitor CPU and RAM usage
    command = "python monitor_script.py"  # Replace with the filename of your monitor script
    stdin, stdout, stderr = ssh_client.exec_command(command)

    # Read and print the output
    output = stdout.read().decode('utf-8')
    print(output)

    # Close the SSH connection
    ssh_client.close()

if __name__ == '__main__':
    remote_address = config['ssh']['ssh_address']
    remote_username = config['ssh']['ssh_username']
    remote_password = config['ssh']['ssh_password']

    # Extract hostname and port from the remote_address
    remote_hostname, remote_port = remote_address.split(':')

    monitor_remote_usage(remote_hostname, remote_port, remote_username, remote_password)
