class Configs:


    ARG_BAMINSIGHT_VERSION = '1.1.2' #version 1.0 has a big difference for the one before, allowing stranded
                                              #and not stranded Data.

    ####################################################################################
    #### Strings presents in help of software, when you run "baminsight -h" command ####
    ####################################################################################

    # BASIC ARGUMENTS
    ARG_GLOBAL_DESCRIPTION = 'A wrapper tool which help in the uploading process to Genome Browser!'
    ARG_SUB_COMMAND = 'Define the Sub command to be used. It can only be Stranded or Original. stranded - When your data is stranded and you pretend to plot It in that way. original - For unstranded data. The software doesn\'t divide reads per strand'
    ARG_GENOME = 'Genome reference of your organism; Ex: hg38'
    ARG_NAMES = 'Path to .bam files, separeted by whitespaces'
    ARG_CPUS = 'Number of cpus/processors to use.'
    # SAMTOOLS ARGUMENTS
    ARG_FORWARD_FLAG = 'The pretended flags to select the wanted forward reads with:  samtools view -f <flag> file.bam (default: 83 and 163)'
    ARG_NOT_FORWARD_FLAG = 'If used, revert the flags in -FF, like:  samtools view -F <flag> file.bam (default: Not used )'
    ARG_REVERSE_FLAG = 'The pretended flags to select the wanted reverse reads with:  samtools view -f <flag> file.bam (default: 99  and 147)'
    ARG_NOT_REVERSE_FLAG = 'If used, revert the flags in -FR, like:  samtools view -F <flag> file.bam (default: Not used )'

    # FINAL DIRECTORY ARGUMENTS
    ARG_LONG_LABEL = 'To define the long label to be present in UCSC upload files (default: BAM file name, if given; Otherwise, this parameter need to be defined)'
    ARG_SHORT_LBAEL = 'To define the short label to be present in UCSC ulpoad files (default: equal to -long_label)'
    ARG_EMAIL = 'It is necessary to input your email to link to your sample. It is mandatory'
    ARG_ADD_BAM = 'If you want to include the BAM file in the final directory, to load the reads in genome browser'

    # FTP SERVER ARGUMENTS
    ARG_FTP_HOST = 'If you want to send the final directory created to your FTP server, you have to input here the host name.'
    ARG_FTP_USER = 'If FTP Server has is protected by user/password login you should define this variable with your user name to login'
    ARG_FTP_PASSWORD = 'If FTP Server has is protected by user/password login you should define this variable with your password to login'
    ARG_FTP_PORT = 'Default port of access is 40021. If your FTP server is diferent please input it here.'
    ARG_FTP_PATH = 'The path in your ftp server to upload the final directory'

    # Global Software Options
    ARG_NO_CREATE_DIR = 'If you only want the .bw files you have to add this argument to the command line'
    ARG_KEEP_FINAL_DIR = 'If you want to keep the final dir in your computer after send it to the ftp server, please add this argument to the command line'


    ####################################################################################
    ####                     Strings returned when a error is raised                ####
    ####################################################################################

    #Genome
    ERR_LACK_GENOME = 'Genome defined in input is not acceptable => '

    #Bam Files
    ERR_ZERO_BAM = 'You have to provide one BAM file at least.'
    ERR_BAM_NOT_EXIST = 'At least, One of yours BAM files doesn\'t exist'

    #Long and Short Label Strings
    ERR_Long_Label_ZERO_BAMLIST_ZERO = 'You didin\'t give any Long Label string and none BAM Files was given too'
    ERR_DIFFERENT_NUMBER_BAM_LONG_LABEL = 'Number of Long Label and BAM Files given is different.'
    ERR_DIFFERENT_NUMBER_LONG_SHORT_LABELS = 'Number of Long and Short Labels is different.'

    #Final DIrectory
    ERR_VALID_MAIL = 'Please define a valid email.'

    # FTP Connection Failure
    ERR_FTP_CONNECTION_FAILURE = 'Error in FTP Server Connection. Verify the FTP name given'

    #####################################################################################################
    #                                       Names of Created Files                                      #
    #####################################################################################################

    FILE_CHROM_SIZES = "chrom.sizes"
    FILE_SHORT_CHROM_SIZES = "short.chrom.sizes"