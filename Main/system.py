##########################################################################
##                                                                      ##
##                      SYSTEM CONTROL SOFTWARE PAGE                    ##
##                                                                      ##
##########################################################################

# Modules Required from BamInsight
import main
import UCSCFiles

def system():
    # accept the inputs and check their reliability
    args = main.argsNcheckers()

    # create files of chromossome sizes
    main.createChrLengthFiles(args.genome)

    #Create Directory for each dataset
    for long_label,short_label in zip(args.long_label,args.short_label):
        UCSCFiles.createMainDirectory(long_label,args.create_dir)
        UCSCFiles.writeGenomesFile(args.genome,args.create_dir)
        UCSCFiles.writeHub(long_label,short_label,args.email,args.create_dir)
        UCSCFiles.createGenomeDirectory(args.genome,args.create_dir)

        # Handling BAM files
        for file,basename in zip(args.name, args.basename):
            NamesFilesPerStrand, ReadsPerStrand =main.splitBamFilePerStrands(file, basename, args.flags_forward, args.not_flags_forward,
                                        args.flags_reverse, args.not_flags_reverse)

            BedGraphsCreated = main.createBedGraph(NamesFilesPerStrand, ReadsPerStrand)

            main.createBWFromBedGraph(BedGraphsCreated)

system()
