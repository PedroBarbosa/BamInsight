import pysam
import os

#Create BAM file according with given flag
def createBamFlagFiltered(flag, oposite_flag, outputFile, inputFile):
    if oposite_flag:
        flag_type="F"
    else:
        flag_type="f"
    reads = pysam.view("-hb"+flag_type+ str(flag), inputFile)
    #Write in File
    open(outputFile, "w").write(reads)

#Merge two or more BAM files
def mergeBamFiles(outputFile, inputList):
    pysam.merge("-f",outputFile, *inputList)

# Sort a BAM file
def sortBamFile(inputFile):
    pysam.sort("-o", os.path.basename(os.path.splitext(inputFile)[0]) +"_sorted.bam", inputFile)

#Count the reads present in the BAM file
def countReads(inputFile):
    return int(pysam.view("-c", inputFile).replace("\n",""))

def getHeader(inputBamFile):
    return pysam.view('-H', inputBamFile)