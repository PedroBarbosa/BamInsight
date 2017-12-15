import urllib2
import os

#Check if connection to FTP Server is possible.
def tryConnectionToFTP(FTPHOST,FTPUser="",FTPPassword = "",FTPPort = 40021):
    try:
        if FTPPassword != "":
            link = ':'
        else:
            link = ""
        FTP_url = 'ftp://' + FTPUser+link+FTPPassword +'@' + FTPHOST + ":" + str(FTPPort)
        server = urllib2.urlopen(FTP_url, timeout=1)
        server.close()
        return True
    except urllib2.URLError as err:
        return False


def sendDirectoryToFTPServer(directoryName,FTPHOST,FTPUser="",FTPPassword = "",FTPPath="",FTPPort = 40021):
    if FTPPassword != "":
        link = ':'
    else:
        link =""

    print str(FTPPort)
    os.system('find ' + directoryName + ' -type f -exec curl --ftp-create-dirs  -T {} ftp://' + FTPUser+link+FTPPassword +
              '@'+ FTPHOST + ":" + str(FTPPort) + '/' + FTPPath + '{} \;')
