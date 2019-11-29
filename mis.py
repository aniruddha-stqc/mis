import paramiko
import csv
import datetime

# Read the CSV file
csv_data = csv.reader(open('credentials.csv', 'rt'))

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

        (stdin, stdout, stderr) = client.exec_command( "tar czf " + archive_file + " --absolute-names /var/www ")

        for line in stdout.readlines():
            print(line)

        client.open_sftp().get(remotepath="/root/" + archive_file, localpath="/media/root/anurag/" + archive_file)

    except Exception as e:
        # Print any exception information
        print(e.args)

# Close this SSHClient and its underlying Transport.
client.close()