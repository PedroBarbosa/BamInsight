import urllib2
import zlib

#This function download and treat the values of genomes size
def downlaod_chr_sizes(genome):
    list_to_retrun = []

    response = urllib2.urlopen("ftp://hgdownload.cse.ucsc.edu/goldenPath/"+ genome + "/database/chromInfo.txt.gz")
    html = response.read()
    decompressed_data = zlib.decompress(html, 16+zlib.MAX_WBITS)
    list_downloaded = [[x for x in ss.split('\t') ] for ss in decompressed_data.split("\n")]
    all_elements_list = [x for x in  list_downloaded if x!=['']]
    for x in all_elements_list:
        list_to_retrun.append([x[0],int(x[1])])
    return list_to_retrun


def downlaod_chr_short_sizes(genome):
    return filter(lambda x: "_"  not in x[0] , downlaod_chr_sizes(genome))

def availableGenomes():
    return filter(lambda item: item not in ['.', '..', '10april2003'], [ss.split()[8] for ss in urllib2.urlopen("ftp://hgdownload.cse.ucsc.edu/goldenPath/").read().split("\n") if ss != ''])

