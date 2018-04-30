import pyBigWig
import pandas
import os
import BAM_handling

#Input:Read a bedgraph file and Bam File Given
#Output:BigWig File
def createBigWigFromBEdGraph(bedgraphFile,bamFile):
    basefile = os.path.splitext(bedgraphFile)[0]
    #Open a new BigWigFile
    bw = pyBigWig.open(basefile + ".bw", "w")
    bw.addHeader(prepareBigWigHeader(bamFile))
    chr, start, end, cov = prepareVeluesToBigWig(bedgraphFile)
    bw.addEntries(chr,start,ends=end,values=cov)
    return basefile + ".bw"

def prepareBigWigHeader(bamFile):
    header = BAM_handling.getHeader(bamFile)
    tuples = [(y.split("\t")[1].strip("SN:"),int(y.split("\t")[2].strip("LN:"))) for y in [x for x in header.split("\n")if x.startswith("@SQ")]]
    return sorted(tuples, key=lambda tup: tup[0])


def prepareVeluesToBigWig(bedgraphFile):
    bedgraph = pandas.read_csv(bedgraphFile,sep="\t")
    bedgraph.columns = ["chr","start","end","cov"]
    chr = bedgraph["chr"].tolist()
    start = bedgraph["start"].tolist()
    end = bedgraph["end"].tolist()
    cov = bedgraph["cov"].tolist()
    return chr,start,end,cov


