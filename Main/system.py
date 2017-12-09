##########################################################################
##                                                                      ##
##                      SYSTEM CONTROL SOFTWARE PAGE                    ##
##                                                                      ##
##########################################################################

# Modules Required from BamInsight
import main

def system():
    # accept the inputs and check their reliability
    args = main.argsNcheckers()

    # create files of chromossome sizes
    main.createChrLengthFiles(args.genome)

    # Handling BAM files
    for file,basename in zip(args.name, args.basename):
        main.splitBamFilePerStrands(file, basename, args.flags_forward, args.not_flags_forward,
                                    args.flags_reverse, args.not_flags_reverse)


system()
