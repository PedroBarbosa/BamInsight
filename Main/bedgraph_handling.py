import os
import pandas
from deeptools import bamCoverage

#Create a BedGraph File From Bam file using GenomeCoverage of bedtools
#Input: BamFIle SORTED
#Output: Name of bedgraph file created
"""
def createBedGraphFile(bamFileSorted):
    basenameNoExtension = os.path.splitext(os.path.basename(bamFileSorted))[0]
    fullPath = os.path.abspath(bamFileSorted)
    with open(bamFileSorted + ".bedgraph", "w") as f:
        bamFile = pybedtools.example_bedtool(fullPath)

        f.write(str(pybedtools.BedTool.genome_coverage(bamFile, bg=True, split=True)))
        f.close()

    os.rename(basenameNoExtension + ".bam.bedgraph", basenameNoExtension + ".bedgraph")
    return basenameNoExtension + ".bedgraph"


def sortBedFile(bedFile):
    fullPath = os.path.abspath(bedFile)
    totalLines = []
    with open(fullPath, "r") as f:
        for line in f.readlines():
            totalLines.append([line.split("\t")[0],line.split("\t")[1],line.split("\t")[2],line.split("\t")[3]])
    totalLines = sorted(totalLines, key=lambda x : [x[0],x[1],x[2]])
    with open('xxx.bedgrapth','w') as w:
        for x in totalLines:
            print x
            print str(x)
            w.write(str(x))
    #bedFileSorted = pybedtools.BedTool.sort(pybedtools.example_bedtool(fullPath))
    #with open(bedFile, 'w') as f:
    #    f.write(str(bedFileSorted))
"""

def scalingFunction(cov_n,lenghtDataset,Strand):
    if Strand == "+": factor = 1
    if Strand == "-": factor = -1
    #for Pandas
    return cov_n * 100000000 / lenghtDataset * factor
    # "for cycle" appropriated return
    #return str(float(float(cov_n) * 100000000 / int(lenghtDataset)) * factor) + "\n"

def createBedGraphFile(bamFileSorted,cpus):
    basenameNoExtension = os.path.splitext(os.path.basename(bamFileSorted))[0]
    inputNameBAM = os.path.abspath(bamFileSorted)
    outNameBW = basenameNoExtension + ".bedgraph"

    args_bamCoverage = "-b {} -o {} --numberOfProcessors {} --binSize 1000 " \
                       "--outFileFormat bedgraph".format(inputNameBAM, outNameBW, cpus).split()

    bamCoverage.main(args_bamCoverage)
    return basenameNoExtension + ".bedgraph"


def applySclaingFactor(BedgraphFile,lenghtDataset,Strand):
    Bfile = pandas.read_table(BedgraphFile, header= None)
    Bfile.columns = ["chr","start","end","cov"]
    Bfile[["cov"]] = Bfile[["cov"]].apply(scalingFunction, args= (lenghtDataset,Strand))
    Bfile.to_csv(BedgraphFile,sep="\t",header=False,index=False)


def writeHeader(bedFile,bamFileSorted):
    firstLine = """track type=bedGraph name=""" + bamFileSorted + \
    """ description="Forward strand reads for """ + bamFileSorted + \
    """" visibility=full color=0,0,255\n"""
    with open(bedFile, 'r') as original: data = original.read()
    with open(bedFile, 'w') as modified: modified.write(firstLine + data)

