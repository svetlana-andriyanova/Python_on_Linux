import paramiko
from datetime import datetime


def upload_files(host, user, passwd, local_path, remote_path, port=22):
    print(f"Upload file {local_path} in catalog {remote_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()