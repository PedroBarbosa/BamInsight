import urllib2
import os
import ftplib


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

def returnDirectories(Path):
    if os.path.isfile(Path):
        return Path.split("/")[:-1]
    elif os.path.isdir(Path):
        return Path.split("/")


def isFTPDirectory(FTPHost,FTPUser,FTPPassword,FTPPort,FTPPath):
    ftp = ftplib.FTP()
    ftp.connect(FTPHost, FTPPort)
    ftp.login(FTPUser, FTPPassword)
    try:
        ftp.cwd(FTPPath)
        ftp.quit()
        return True
    except:
        ftp.quit()
        return False

def sendFiletoFTP(LOCALFile,FTPHost,FTPUser,FTPPassword,FTPPort,FTPPath="/"):
    #Connect to Server
    ftp = ftplib.FTP()
    ftp.connect(FTPHost, FTPPort)
    ftp.login(FTPUser, FTPPassword)

    #Ensure the same directory tree as in local
    mem=FTPPath
    for enum,dir in enumerate(returnDirectories(LOCALFile)):
        mem = os.path.join(mem,dir)
        if isFTPDirectory(FTPHost,FTPUser,FTPPassword,FTPPort,mem):
            ftp.cwd(mem)
        else:
            ftp.mkd(mem)
            ftp.cwd(mem)

    #Send the file
    file = open(LOCALFile,'rb')
    theFile = os.path.basename(LOCALFile)
    sendCommand = 'STOR ' + theFile
    ftp.storbinary(sendCommand, file)

    ftp.quit()



def sendDirectorytoFTP(DirName,FTPHost,FTPUser,FTPPassword,FTPPort,FTPPath="/"):
    allFiles=[]
    for root, directories, files in os.walk(DirName):
        for name in files:
            allFiles.append(os.path.join(root, name))
    for file in allFiles:
        sendFiletoFTP(file,FTPHost,FTPUser,FTPPassword,FTPPort,FTPPath)
