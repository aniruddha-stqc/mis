import paramiko
import csv
import datetime
from tkinter import filedialog, Tk


# Read the CSV file containing: IP address, username, password
csv_data = csv.reader(open("credentials.csv", "rt"))

# Hide blank root window
Tk().withdraw()
# Ask back up download local folder path
target_directory = filedialog.askdirectory(initialdir="/root/Downloads", title="Select Download Folder")
# Destroy tkinter instance
Tk().destroy()

# Read system credential rows one at a time
for system_credentials in csv_data:
    # A high-level representation of a session with an SSH server. This class wraps Transport, Channel, and SFTPClient
    # to take care of most aspects of authenticating and opening channels.
    client = paramiko.SSHClient()
    # Load host keys from a system (read-only) file.
    client.load_system_host_keys()
    # Interface for defining the policy that SSHClient should use when the SSH server’s hostname is not in either the
    # system host keys or the application’s keys.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to an SSH server and authenticate to it. The server’s host key is checked against the system host keys
        # (see load_system_host_keys) and any local host keys (load_host_keys). If the server’s hostname is not found in
        # either set of host keys, the missing host key policy is used (see set_missing_host_key_policy).
        client.connect(hostname=system_credentials[0], username=system_credentials[1], password=system_credentials[2])

        # Create file name as per the current date
        archive_file = "misappbackup_" + datetime.datetime.now().strftime("%Y%m%d") + ".tar.gz"

        client.exec_command( "tar czf " + archive_file + " /var/www ")

        # Download the back up file from remote machine to local machine
        client.open_sftp().get(remotepath="/root/" + archive_file, localpath= target_directory + "/" + archive_file)

        # Remove the back up file from remote machine
        client.exec_command("rm -r " + archive_file)
        # Close this SSHClient and its underlying Transport.
        client.close()
    except Exception as e:
        # Print any exception information
        print(e.args)

