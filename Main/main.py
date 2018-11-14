import sys
import os
import inputs
import BAM_handling
import download_chr_file
import bedgraph_handling
import BigWig_handling
import FTPConnections
from Configs.configs import Configs

#This function call inputs fucntion, and then check the arguments given
def argsNcheckers():
    # Accept the arguments given by the user
    args = inputs.entry_inputs()

    # Checking if Genome is allowed
    sys.stdout.write("Checking if your Genome is allowed:")
    inputs.genomeCheck(args.genome)
    sys.stdout.write(" CHECK!\n")

    # Checking Bam Files
    sys.stdout.write("Checking Files Constraints:")
    inputs.bamNumberCheck(args.name)
    inputs.checkFilesSource(args.name)
    args.name = inputs.defineBAMsAbsolutePath(args.name)
    args.basename = inputs.defineBasenamesBAMs(args.name)

    # Checking Long Labels
    args.long_label = inputs.longLabelCopyFromBasename(args.long_label,args.basename)
    inputs.bamNLongLabelNumberConcordance(args.long_label,args.name)

    #Checking Short Labels
    args.short_label = inputs.shortLabelCopyFromLongLabel(args.short_label,args.long_label)
    inputs.LongLabelShortLabelNumberConcordance(args.short_label,args.long_label)

    #Checking Email
    inputs.checkEmail(args.email, args.create_dir)

    sys.stdout.write(" CHECK!\n")

    # Checking FTP Server
    if inputs.isFTPServerGiven(args.host_FTP):
        sys.stdout.write("Checking FTP Server Connection:")
        inputs.checkConnectionFTP(args.host_FTP,args.user_FTP,args.password_FTP,args.port_FTP)
        sys.stdout.write(" CHECK!\n")

    return args

def createChrLengthFiles(genome):
    sys.stdout.write("Downloading Chr Sizes Files used by BamInsight:")
    with open(Configs.FILE_CHROM_SIZES, "w") as f:
        for e in download_chr_file.downlaod_chr_sizes(genome):
            f.write('{}\t{}\n'.format(e[0],e[1]))
        f.close()
    Configs.FILE_CHROM_SIZES = os.path.abspath(Configs.FILE_CHROM_SIZES)

    with open(Configs.FILE_SHORT_CHROM_SIZES, "w") as f:
        for e in download_chr_file.downlaod_chr_short_sizes(genome):
            f.write('{}\t{}\n'.format(e[0],e[1]))
        f.close()
    Configs.FILE_SHORT_CHROM_SIZES = os.path.abspath(Configs.FILE_SHORT_CHROM_SIZES)
    sys.stdout.write(" CHECK!\n")


####################################


def createChrLengthFilesBAMFile(bamFile):
    sys.stdout.write("Downloading Chr Sizes Files used by BamInsight:")
    with open(Configs.FILE_CHROM_SIZES, "w") as f:
        for e in BAM_handling.chrLengthFromHeader(bamFile):
            f.write('{}\t{}\n'.format(e[0], e[1]))
        f.close()
    Configs.FILE_CHROM_SIZES = os.path.abspath(Configs.FILE_CHROM_SIZES)
    sys.stdout.write(" CHECK!\n")



def splitBamFilePerStrands(BAMfile, Basenamefile, Flags_F, opposite_F, Flags_R, opposite_R,cpus):
    sys.stdout.write("Splitting BAM file " + Basenamefile + ":")
    NamesFilesPerStrand, ReadsPerStrand  = [],[]
    for mainEnum,Flags_Strand in enumerate([Flags_F,Flags_R]):
        if mainEnum == 0: Strand,oppositeFlag = ["F",opposite_F]
        if mainEnum == 1: Strand,oppositeFlag = ["R",opposite_R]

        outFiles =[]
        for enum,flag in enumerate(Flags_Strand):
            outFiles.append(Strand + str(enum) + "_" + Basenamefile)
            BAM_handling.createBamFlagFiltered(flag,oppositeFlag,Strand+str(enum)+"_"+Basenamefile,BAMfile,cpus)


        # Merge BAM Files
        if len(Flags_F) > 1:
            BAM_handling.mergeBamFiles(Strand+"_"+Basenamefile,outFiles,cpus)
        else:
            os.rename(Strand + str(0)+"_" + Basenamefile , Strand +"_" + Basenamefile)

        #Sort BAM Files
        BAM_handling.sortBamFile(Strand+"_"+Basenamefile,cpus)

        #Create BAM index
        BAM_handling.indexBamFfile(Strand+"_"+os.path.basename(os.path.splitext(Basenamefile)[0]) + "_sorted.bam"   )

        NamesFilesPerStrand.append(Strand+"_"+os.path.splitext(Basenamefile)[0]+"_sorted.bam")
        ReadsPerStrand.append(BAM_handling.countReads(Strand+"_"+os.path.splitext(Basenamefile)[0]+"_sorted.bam",cpus))
    sys.stdout.write(" CHECK!\n")
    return NamesFilesPerStrand, ReadsPerStrand


def TreatOriginalBamFile(BamFile,Basename,cpus):
    sys.stdout.write("Preparing " + BamFile + " file:")
    BAM_handling.sortBamFile(BamFile,cpus)
    sys.stdout.write(" CHECK!\n")

    return [os.path.splitext(Basename)[0] + "_sorted.bam"], [BAM_handling.countReads(os.path.splitext(Basename)[0] + "_sorted.bam")]




def createBedGraph(NamesFilesPerStrand,ReadsPerStrand,cpus):
    namesToReturn = []
    for enum,StrandBamFile in enumerate(NamesFilesPerStrand):
        sys.stdout.write("Creating BedGraph file for " + StrandBamFile + ":")
        if enum == 0: strand = "+"
        if enum == 1: strand = "-"
        bedgraphFile = bedgraph_handling.createBedGraphFile(StrandBamFile,cpus)
        #bedgraph_handling.sortBedFile(bedgraphFile)
        bedgraph_handling.applySclaingFactor(bedgraphFile,ReadsPerStrand[enum],strand)
        #bedgraph_handling.writeHeader(bedgraphFile,os.path.splitext(StrandBamFile)[0])
        namesToReturn.append(bedgraphFile)
        sys.stdout.write(" CHECK!\n")
    return namesToReturn

#Input: The two Bedgraphs files names
def createBWFromBedGraph(bedgraphFiles):
    namesToReturn = []
    for file in bedgraphFiles:
        sys.stdout.write("Creating BigWig file for " + file + ":")
        BWFile = BigWig_handling.createBigWigFromBEdGraph(file, Configs.FILE_CHROM_SIZES)
        namesToReturn.append(BWFile)
        sys.stdout.write(" CHECK!\n")
    return namesToReturn

def mainSendDirectoryToFTPServer(dirName,FTPHost,FTPUser="",FTPPassword="",FTPPort=20041,FTPPath=""):
    if FTPHost != "":
        FTPConnections.sendDirectoryToFTPServer(dirName,FTPHost,FTPUser,FTPPassword,FTPPath,FTPPort)


def removeIntermediateFiles(path):
    for item in os.listdir(path):
        if item.endswith(".bam") or item.endswith(".bedgraph") or item.endswith(".bai"):
            os.remove(item)

