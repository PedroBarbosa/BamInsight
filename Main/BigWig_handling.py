import pyBigWig
import pandas
import os

#Input:Read a bedgraph file and Chromossomal Size File
#Output:BigWig File
def createBigWigFromBEdGraph(bedgraphFile,chrSizesFile):
    basefile = os.path.splitext(bedgraphFile)[0]
    #Open a new BigWigFile
    bw = pyBigWig.open(basefile + ".bw", "w")
    bw.addHeader(prepareBigWigHeader(chrSizesFile))
    chr, start, end, cov = prepareVeluesToBigWig(bedgraphFile)
    bw.addEntries(chr,start,ends=end,values=cov)
    return basefile + ".bw"

def prepareBigWigHeader(chrSizesFile):
    with open(chrSizesFile) as f:
        allChr = map(lambda s: s.strip(), f.readlines())
    tuples = [tuple([s[0], int(s[1])]) for s in [tuple(x.split("\t")) for x in allChr]]
    tuples.sort(key=lambda x: x[0])
    return tuples


def prepareVeluesToBigWig(bedgraphFile):
    bedgraph = pandas.read_csv(bedgraphFile,sep="\t")
    bedgraph.columns = ["chr","start","end","cov"]
    chr = bedgraph["chr"].tolist()
    start = bedgraph["start"].tolist()
    end = bedgraph["end"].tolist()
    cov = bedgraph["cov"].tolist()
    return chr,start,end,cov


