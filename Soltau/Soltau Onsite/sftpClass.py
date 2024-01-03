import pysftp
from urllib.parse import urlparse
import os
from settings import Settings
from logger import jobslogger
from utils import utils
import asyncio

from stations import CommonError

# hostname = 'sftp1.itksp.net'
# username = 'SVC-GS-052ROBO01@ad.itksp.net'
# password = '<RAR,L&3WPG6-Q#b17'


class Sftp:
    def __init__(self):
        """Constructor Method"""
        # Set connection object to None (initial value)
        self.connection = None
        self.hostname = Settings.hostname
        self.username = Settings.username
        self.password = Settings.password
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None
        self.port = 22
        
    async def connect(self):
        """Connects to the sftp server and returns the sftp connection object"""
        try:
            # Get the sftp connection object
            self.connection = pysftp.Connection(
                host=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port,
                cnopts=self.cnopts
            )
        except Exception as err:
            raise Exception(err)
        finally:
            print(f"Connected to {self.hostname} as {self.username}.")

    async def disconnect(self):
        """Closes the sftp connection"""
        self.connection.close()
        print(f"Disconnected from host {self.hostname}")

    def listdir(self, remote_path):
        """lists all the files and directories in the specified path and returns them"""
        for obj in self.connection.listdir(remote_path):
            yield obj

    def listdir_attr(self, remote_path):
        """lists all the files and directories (with their attributes) in the specified path and returns them"""
        for attr in self.connection.listdir_attr(remote_path):
            yield attr

    def download(self, remote_path, target_local_path):
        """
        Downloads the file from remote sftp server to local.
        Also, by default extracts the file to the specified target_local_path
        """
        try:
            print(
                f"downloading from {self.hostname} as {self.username} [(remote path : {remote_path});(local path: {target_local_path})]"
            )

            # Create the target directory if it does not exist
            path, _ = os.path.split(target_local_path)
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except Exception as err:
                    raise Exception(err)

            # Download from remote sftp server to local
            self.connection.get(remote_path, target_local_path)
            print("download completed")

        except Exception as err:
            raise Exception(err)

    async def upload(self, source_local_path, remote_path):
        """
        Uploads the source files from local to the sftp server.
        """

        try:
            jobslogger.info("SFTP uploading, {0}, {1}".format(source_local_path,remote_path)) 
            await self.connect()            
            self.connection.put(source_local_path, remote_path)            
            await self.disconnect()
            jobslogger.info("SFTP uploading success") 
        except Exception as err:
            raise Exception(err)

    async def moveCSVToSFTPServer(self):
        local_path = "C:\\Diabots\\Soltau Onsite\\CSV\\"
        # remote_path = "704048881353.csv"

        # iterate on all files to move them to destination folder
        allfiles = os.listdir(local_path)
        for fname in allfiles:
            src_path = os.path.join(local_path, fname)
            fileStatus = await utils.isFileReady(src_path,0.01,500)
            if fileStatus:
                await self.upload(src_path, fname)
                os.remove(src_path)
            else:
                raise CommonError("Unexpected error occurred. Please check logs!")

sftpCommunication = Sftp()

async def main():
    sftp = Sftp()
    await sftp.moveCSVToSFTPServer()

if __name__ == '__main__':
    asyncio.run(main())

    

    # Lists files with attributes of SFTP
    # path = "/"
    # print(f"List of files with attributes at location {path}:")
    # for file in sftp.listdir_attr(path):
    #     print(file.filename, file.st_mode, file.st_size, file.st_atime, file.st_mtime)

    # Upload files to SFTP location from local
    # local_path = "C:\\Diabots\\Soltau Onsite\\CSV\\266012664703.csv"
    # remote_path = "266012664703.csv"
    # sftp.upload(local_path, remote_path)

    # Lists files of SFTP location after upload
    # print(f"List of files at location {path}:")
    # print([f for f in sftp.listdir(path)])

    # # Download files from SFTP
    # sftp.download(
    #     remote_path, os.path.join(remote_path, local_path + '.backup')
    # )

    # Disconnect from SFTP
    # sftp.disconnect()
