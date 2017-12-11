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



#import ftplib

#sftp = ftplib.FTP('ftp://immftp01.fm.ul.pt','mcfonsecaftp','Lark699-evan') # Connect
##fp = open('todo.txt','rb') # file to send
##sftp.storbinary('STOR todo.txt', fp) # Send the file

#fp.close() # Close file and FTP
#sftp.quit()
#ftp://mcfonsecaftp:Lark699%2Devan@imm.fm.ul.pt:40021/

#sendFinalDirectory('a','b','c')