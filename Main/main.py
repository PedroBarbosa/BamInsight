import sys
import os
import inputs
import BAM_handling
import download_chr_file

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
    args.basename = inputs.defineBasenamesBAMs(args.name)

    # Checking Long Labels
    args.long_label = inputs.longLabelCopyFromBasename(args.long_label,args.basename)
    inputs.bamNLongLabelNumberConcordance(args.long_label,args.name)

    #Checking Short Labels
    args.short_label = inputs.shortLabelCopyFromLongLabel(args.short_label,args.long_label)
    inputs.LongLabelShortLabelNumberConcordance(args.short_label,args.long_label)

    sys.stdout.write(" CHECK!\n")

    # Checking FTP Server
    if inputs.isFTPServerGiven(args.host_FTP):
        sys.stdout.write("Checking FTP Server Connection:")
        inputs.checkConnectionFTP(args.host_FTP)
        sys.stdout.write(" CHECK!\n")

    return args

def createChrLengthFiles(genome):
    sys.stdout.write("Downloading Chr Sizes Files used by BamInsight:")
    with open("chrom.sizes", "w") as f:
        for e in download_chr_file.downlaod_chr_sizes(genome):
            f.write('{}\t{}\n'.format(e[0],e[1]))
        f.close()

    with open("short.chrom.sizes", "w") as f:
        for e in download_chr_file.downlaod_chr_short_sizes(genome):
            f.write('{}\t{}\n'.format(e[0],e[1]))
        f.close()
    sys.stdout.write(" CHECK!\n")


def splitBamFilePerStrands(BAMfile, Basenamefile, Flags_F, opposite_F, Flags_R, opposite_R):
    sys.stdout.write("Splitting BAM file " + Basenamefile + ":")
    NamesFilesPerStrand, ReadsPerStrand  = [],[]
    for mainEnum,Flags_Strand in enumerate([Flags_F,Flags_R]):
        if mainEnum == 0: Strand,oppositeFlag = ["F",opposite_F]
        if mainEnum == 1: Strand,oppositeFlag = ["R",opposite_R]

        outFiles =[]
        for enum,flag in enumerate(Flags_Strand):
            outFiles.append(Strand + str(enum) + "_" + Basenamefile)
            BAM_handling.createBamFlagFiltered(flag,oppositeFlag,Strand+str(enum)+"_"+Basenamefile,BAMfile)


        # Merge BAM Files
        if len(Flags_F) > 1:
            BAM_handling.mergeBamFiles(Strand+"_"+Basenamefile,outFiles)
        else:
            os.rename(Strand + str(0)+"_" + Basenamefile , Strand +"_" + Basenamefile)

        #Sort BAM Files
        BAM_handling.sortBamFile(Strand+"_"+Basenamefile)


        NamesFilesPerStrand.append(Strand+"_"+os.path.splitext(Basenamefile)[0]+"_sorted.bam")
        ReadsPerStrand.append(BAM_handling.countReads(Strand+"_"+os.path.splitext(Basenamefile)[0]+"_sorted.bam"))
    sys.stdout.write(" CHECK!\n")
    return NamesFilesPerStrand, ReadsPerStrand

def createBedGraph():
    pass

