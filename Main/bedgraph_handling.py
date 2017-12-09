import pybedtools
import os

def createBedGraphFile(bamFileSorted):
    basenameNoExtension = os.path.splitext(os.path.basename(bamFileSorted))
    with open(bamFileSorted + ".bedgraph", "w") as f:
        f.write("""echo track type=bedGraph name=""" + bamFileSorted + \
    """ description="Forward strand reads for """ + bamFileSorted + \
    """" visibility=full color=0,0,255""")

        bamFile = pybedtools.example_bedtool(bamFileSorted)
        f.write(str(pybedtools.BedTool.genome_coverage(bamFile, bg=True, split=True)))

        f.close()


createBedGraphFile("/home/ruiluis/PycharmProjects/BamInsight/Main/F_wgEncodeUwRepliSeqK562G1AlnRep1_sorted.bam")
