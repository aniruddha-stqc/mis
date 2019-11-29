import paramiko
import csv
import datetime
from tkinter import filedialog, Tk


# Read the CSV file containing: IP address, username, password. It is assumed that the CSV file contains a header row
# with the column names in the following order: "ip","username",password"
csv_data = csv.DictReader(open(file="credentials.csv", mode="rt"))

# Hide blank root window
Tk().withdraw()

# Ask back up download local folder path from user
target_directory = filedialog.askdirectory(initialdir="/root/Downloads", title="Select Download Folder")
# Destroy tkinter instance
Tk().destroy()

# Read system credential rows one at a time
for credential_list in csv_data:
    # A high-level representation of a session with an SSH server. This class wraps Transport, Channel, and SFTPClient
    # to take care of most aspects of authenticating and opening channels.
    client = paramiko.SSHClient()
    # Load host keys from a system (read-only) file.
    client.load_system_host_keys()
    # Interface for defining the policy that SSHClient should use when the SSH server’s hostname is not in either the
    # system host keys or the application’s keys.
    client.set_missing_host_key_policy(policy=paramiko.AutoAddPolicy())

    try:
        # Connect to an SSH server and authenticate to it. The server’s host key is checked against the system host keys
        # (see load_system_host_keys) and any local host keys (load_host_keys). If the server’s hostname is not found in
        # either set of host keys, the missing host key policy is used (see set_missing_host_key_policy).
        client.connect(hostname=credential_list['ip'], username=credential_list['username'], password=credential_list['password'])

        # Create file name as per the current date
        archive_file = "misappbackup_" + datetime.datetime.now().strftime("%Y%m%d") + ".tar.gz"

        # Execute remote command to create a archive of the required files
        client.exec_command( command="tar czf " + archive_file + " /var/www ")

        # Download the back up file from remote machine to local machine
        client.open_sftp().get(remotepath="/root/" + archive_file, localpath= target_directory + "/" + archive_file)

        # Remove the back up file from remote machine as it is no more required
        client.exec_command(command="rm -r " + archive_file)

        # Close this SSHClient and its underlying Transport.
        client.close()

        print("Downloaded successfully to:", target_directory + "/" + archive_file)

    except Exception as e:
        # Print any exception information
        print("Exception Occurred: ", e.args)

