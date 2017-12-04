import urllib2

#Check if connection to FTP Server is possible.
def tryConnectionToFTP(FTP_url):
    try:
        urllib2.urlopen(FTP_url, timeout=1)
        return True
    except urllib2.URLError as err:
        return False
