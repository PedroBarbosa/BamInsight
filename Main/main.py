import sys
import inputs



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

def createBWFromBAM(BAMList, BasenameList, Flags_F = None, Flags_R = None):
    BAMList