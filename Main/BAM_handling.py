import pysam
import os

#Create BAM file according with given flag
def createBamFlagFiltered(flag, oposite_flag, outputFile, inputFile,cpus):
    if oposite_flag:
        flag_type="F"
    else:
        flag_type="f"
    reads = pysam.view("-hb"+flag_type+ str(flag), "-@",cpus,inputFile)
    #Write in File
    open(outputFile, "w").write(reads)

#Merge two or more BAM files
def mergeBamFiles(outputFile, inputList,cpus):
    pysam.merge("-f",outputFile, "-@",cpus ,*inputList)

# Sort a BAM file
def sortBamFile(inputFile,cpus):
    pysam.sort("-o", os.path.basename(os.path.splitext(inputFile)[0]) +"_sorted.bam", "-@", cpus, inputFile)

# Create BAM index
def indexBamFfile(inputFile):
    pysam.index(inputFile)

#Count the reads present in the BAM file
def countReads(inputFile, cpus):
    return int(pysam.view("-c", "-@",cpus, inputFile).replace("\n",""))

def chrLengthFromHeader(inputFile):
    header = pysam.view('-H', inputFile)
    return [[x.split("\t")[1].replace("SN:", ""), x.split("\t")[2].replace("LN:", "")] for x in header.split("\n") if "@SQ" in x]
