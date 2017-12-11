import urllib2
import ftplib


#Check if connection to FTP Server is possible.
def tryConnectionToFTP(FTP_url):
    try:
        urllib2.urlopen(FTP_url, timeout=1)
        return True
    except urllib2.URLError as err:
        return False

#def sendFinalDirectory(ftpServer,user,password):
    #a_host = FTPHost.connect('ftp://immftp01.fm.ul.pt:40021/')
    #oc.login('mcfonsecaftp', 'Lark699-evan')


#sendFinalDirectory('a','b','c')