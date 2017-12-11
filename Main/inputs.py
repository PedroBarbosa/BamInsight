import argparse
import os
import copy
import download_chr_file
import FTPConnections
import re
from Configs.configs import Configs

#All arguemnts that can be specified on BamInsight. Python module argparse is necessary here.
def entry_inputs():
    parser = argparse.ArgumentParser(description=Configs.ARG_GLOBAL_DESCRIPTION)

    #BASIC ARGUMENTS
    parser.add_argument('genome',  help = Configs.ARG_GENOME)


    basic_arg = parser.add_argument_group('Basic Arguments')
    basic_arg.add_argument('--names', metavar='name1 name2',dest='name',  nargs='+', help = Configs.ARG_NAMES, default= [])
    parser.add_argument('--basenames', dest='basename', nargs='+', help=argparse.SUPPRESS)

    #SAMTOOLS ARGUMENTS
    samtools_arg = parser.add_argument_group('Samtools Arguments')
    samtools_arg.add_argument('-FF', metavar='--FLAGS_Forward', dest='flags_forward', type=int, nargs='+', help=Configs.ARG_FORWARD_FLAG, default= [83,163])
    samtools_arg.add_argument('-notFF', dest='not_flags_forward',  action='store_true', default= False, help=Configs.ARG_NOT_FORWARD_FLAG)
    samtools_arg.add_argument('-FR', metavar='--FLAGS_Reverse', dest='flags_reverse', type=int, nargs='+', help=Configs.ARG_REVERSE_FLAG, default= [99,147])
    samtools_arg.add_argument('-notFR', dest='not_flags_reverse',  action='store_true', default= False, help=Configs.ARG_NOT_REVERSE_FLAG)

    #FINAL DIRECTORY ARGUMENTS
    final_dir_args= parser.add_argument_group('Final Directory Arguments')
    final_dir_args.add_argument('-long_label', dest='long_label', nargs='+', help = Configs.ARG_LONG_LABEL, default=[] )
    final_dir_args.add_argument('-short_label', dest='short_label', nargs='+', help = Configs.ARG_SHORT_LBAEL, default=[])
    final_dir_args.add_argument('--email', dest='email', default = "", help=Configs.ARG_EMAIL)
    final_dir_args.add_argument('-add_bam', dest='add_bam', action='store_true', default= False, help = Configs.ARG_ADD_BAM)


    #FTP SERVER ARGUMENTS
    ftp_server_args = parser.add_argument_group('FTP Server Arguments')
    ftp_server_args.add_argument('-HOST_FTP_SERVER', dest='host_FTP', help=Configs.ARG_FTP_SERVER)
    ftp_server_args.add_argument('-FTP_Path', dest='ftp_path', default="" , help=Configs.ARG_FTP_PATH)

    #Global Software Options
    run_phases_args = parser.add_argument_group('Global Software Options')
    run_phases_args.add_argument('-no_create_dir', dest='create_dir', action='store_true', default= False, help=Configs.ARG_NO_CREATE_DIR)
    run_phases_args.add_argument('-keep_final_dir', dest='keep_final_dir', action='store_true', default= False, help = Configs.ARG_KEEP_FINAL_DIR)

    #Version
    parser.add_argument('-v', action='version', version=Configs.ARG_BAMINSIGHT_VERSION)

    return parser.parse_args()


######################################################################################################################
#                                                                                                                    #
#                       Functions to control the inputs given by the user !                                          #
#                               All constraints of inputs should be define and verified here                          #
#                                                                                                                    #
######################################################################################################################

##################################################################
# Genome Parameter                                               #
##################################################################
def genomeCheck(genome):
    if genome not in download_chr_file.availableGenomes():
        raise ValueError(Configs.ERR_LACK_GENOME + str(genome))


##################################################################
# Bam Files                                                      #
##################################################################

#Verify if the BAMList has one bam file, at least
def bamNumberCheck(BAMList):
    if len(BAMList) == 0:
        raise ValueError(Configs.ERR_ZERO_BAM)

# Check if the bam files exist
def checkFilesSource(BAMList):
    for file in BAMList:
        if not os.path.isfile(file):
            raise ValueError(Configs.ERR_BAM_NOT_EXIST)

#Define basenames (without the path, like: filename.bam)
def defineBasenamesBAMs(BAMList):
    for file in BAMList:
        basenameBAMLIST = []
        basenameBAMLIST.append(os.path.basename(file))
    return basenameBAMLIST



##################################################################
# Long Label                                                     #
##################################################################
#It can be useful one day
def checklongLabelSource(LongLabelList, BAMList):
    if len(LongLabelList) == 0 and len(BAMList) == 0:
        raise ValueError(Configs.ERR_Long_Label_ZERO_BAMLIST_ZERO)

#Check if Long Label List has some string inside. If none string is presented inside, make a deep copy of BasenameList
def longLabelCopyFromBasename(LongLabelList,BasenameList):
    listToReturn = []
    if len(LongLabelList) == 0:
        BasenameList = copy.copy(BasenameList)
        for e in BasenameList:
            listToReturn.append(os.path.splitext(e)[0])
        return listToReturn
    else:
        return LongLabelList

#Check if number of Long Labels and Bam Files given is the same
def bamNLongLabelNumberConcordance(LongLabelList,BAMList):
    if len(LongLabelList) != len(BAMList):
        raise ValueError(Configs.ERR_DIFFERENT_NUMBER_BAM_LONG_LABEL)


###################################################################
# Short Label                                                     #
###################################################################
#Check if Short Label List has some string inside. If none string is presented inside, make a deep copy of Long Label List
def shortLabelCopyFromLongLabel(ShortLabelList, LongLabelList):
    if len(ShortLabelList) == 0:
        return copy.copy(LongLabelList)
    else:
        return ShortLabelList

#Check if number of Short Labels List and Long Labels List given is the same
def LongLabelShortLabelNumberConcordance(ShortLabelList,LongLabelList):
    if len(LongLabelList) != len(ShortLabelList):
        raise ValueError(Configs.ERR_DIFFERENT_NUMBER_LONG_SHORT_LABELS)

###################################################################
# Flags                                                           #
###################################################################

#For now none constraint is defined. In the future, Flags Arguments will be replaced by strandness type of datasets, like:
# fr-firstrand; fr-secondstrand;
# pair-end single-end
# etc

###################################################################
# Final Directory                                                 #
###################################################################

def checkEmail(email,create_dir):
    if not create_dir:
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise ValueError(Configs.ERR_VALID_MAIL)


###################################################################
# FTP Server
###################################################################

def isFTPServerGiven(FTPServer):
    if FTPServer != None:
        return True

def checkConnectionFTP(FTP_server):
    if not FTPConnections.tryConnectionToFTP(FTP_server):
        raise ValueError(Configs.ERR_FTP_CONNECTION_FAILURE)

###################################################################
# Software Running Constraints
###################################################################


