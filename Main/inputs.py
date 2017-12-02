import argparse
import os
import copy
import sys


#All alguemnts that can be specified. Python module argparse is necessary here.
def entry_inputs():
    parser = argparse.ArgumentParser(description='Make Final directory to upload to Genome browser UCSC, From: \
    1) Bam file; or 2) Bigwigs files')

    #BASIC ARGUMENTS
    parser.add_argument('genome',  help='The Genome reference of your organism')


    basic_arg = parser.add_argument_group('Basic Arguments')
    basic_arg.add_argument('--names', metavar='name1 name2',dest='name',  nargs='+', help='Name .bam files, separeted by whitespaces')
    parser.add_argument('--basenames', dest='basename', nargs='+', help=argparse.SUPPRESS)
    basic_arg.add_argument('--P', metavar='--Path',dest='path',  help='The path where the script expect to find the input file(s) (default: current directory)', default=os.getcwd())
    basic_arg.add_argument('-L', metavar='--Length',dest='data_sets_length', nargs='+', help='If you pretend to normalize the datasets, you have to input the datasets length separeted by whitespaces in the same order of files name (ONLY HAVE TO DEFINE IT IF NOT RUN THE FIRST PHASE )  Normalization is done by:  (reads_in_region*100 000 000)/dataset_length', default=[])

    #SAMTOOLS ARGUMENTS
    samtools_arg = parser.add_argument_group('Samtools Arguments')
    samtools_arg.add_argument('-FF', metavar='--FLAGS_Forward', dest='flags_forward', type=int, nargs='+', help='The pretended flags to select the wanted forward reads with:  samtools view -f <flag> file.bam (default: 83 and 163)  ', default= [83,163])
    samtools_arg.add_argument('-notFF', dest='not_flags_forward',  action='store_true', default= False, help='If used, revert the flags in -FF, like:  samtools view -F <flag> file.bam (default: Not used ) ')
    samtools_arg.add_argument('-FR', metavar='--FLAGS_Reverse', dest='flags_reverse', type=int, nargs='+', help='The pretended flags to select the wanted reverse reads with:  samtools view -f <flag> file.bam (default: 99  and 147)  ', default= [99,147])
    samtools_arg.add_argument('-notFR', dest='not_flags_reverse',  action='store_true', default= False, help='If used, revert the flags in -FR, like:  samtools view -F <flag> file.bam (default: Not used ) ')

    #BIG WIGS ARGUMENTS
    bigwig_args = parser.add_argument_group('Big Wig Arguments')
    bigwig_args.add_argument('--F_Sorted_bam',dest='F_Sorted_bam', nargs='+'  , help='The Forward reads in bam file format sorted by coordinates (It\'s only applicable if you already have the reads splited in forward and reverse bam files)' )
    bigwig_args.add_argument('--R_Sorted_bam',dest='R_Sorted_bam', nargs='+' ,help='The Reverse reads in bam file format sorted by coordinates (It\'s only applicable if you already have the reads splited in forward and reverse bam files)')
    parser.add_argument('--F_nameBW', dest='F_nameBW', nargs='+', help=argparse.SUPPRESS)
    parser.add_argument('--R_nameBW', dest='R_nameBW', nargs='+', help=argparse.SUPPRESS)

    #FINAL DIRECTORY ARGUMENTS
    final_dir_args= parser.add_argument_group('Final Directory Arguments')
    final_dir_args.add_argument('-long_label', dest='long_label', nargs='+', help='To define the long label to be present in UCSC upload files (default: bam file name, if given; Otherwise, this parameter need to be defined', default=[] )
    final_dir_args.add_argument('-short_label', dest='short_label', nargs='+', help= 'To define the short label to be present in UCSC ulpoad files (default: equal to -long_label)', default=[])
    final_dir_args.add_argument('-add_bam', dest='add_bam', action='store_true', default= False, help='If you want to incorporate the bam file in the final directory, to load the reads in genome browser')


    #FTP SERVER ARGUMENTS
    ftp_server_args = parser.add_argument_group('FTP Server Arguments')
    ftp_server_args.add_argument('-HOST_FTP_SERVER', dest='host_FTP', help="If you want to send the final directory with all contents to be loaded by UCSC Genome Browser to your FTP Server, you have to define here the host name, with user and password if applicable.")
    ftp_server_args.add_argument('-FTP_Path', dest='ftp_path', default="" , help='The path in your ftp server to upload the final directory')

    #Script Run Phases
    run_phases_args = parser.add_argument_group('Run Phases Options Arguments')
    run_phases_args.add_argument('-no_create_dir', dest='create_dir', action='store_false', default= True, help='If you only want the .bw files you have to add this argument to the command line')
    run_phases_args.add_argument('-no_upload_ftp',dest='upload_ftp', action='store_false', default= True, help='If you don\'t want to upload the final directory to the ftp server, please add this argument to the command line')
    run_phases_args.add_argument('-keep_final_dir', dest='keep_final_dir', action='store_true', default= False, help = 'If you want to keep the final dir in your computer/server/cluster after send it to the ftp server please add this argument to the command line')

    #Version
    parser.add_argument('-v', action='version', version='BAMtoGenomeBrowser 1.0')

    return parser.parse_args()


def inputs_treatment(args):
    check_soft_constrains_inputs(args)
    args = def_soft_inputs(args)
    return args


## Checks Contrains to the rigth functionality of the software
def check_soft_constrains_inputs(args):
    define_entry_phase(args)
    not_normalized(args)

## Accept information given and try to predict another
def def_soft_inputs(args):
    args = entry_bam_splited(args)
    args = def_basenames(args)
    args = def_long_label(args)
    args = def_short_label(args)
    return args

def define_entry_phase(args):
    if number_bam_files(args) == 0 and (args.F_Sorted_bam == None or args.R_Sorted_bam == None):
        raise ValueError("\n\nNone bam file was given!\n\nPlease define --F_Sorted_bam and --R_Sorted_bam\nOtherwise, give bam file(s) as: --names file1.bam  file2.bam ..")

def entry_bam_splited(args):
    if number_bam_files(args) == 0:
        args.F_Sorted_bam = bam_files_to_sorted_strand_bam(args.name, 'F_')
        args.R_Sorted_bam = bam_files_to_sorted_strand_bam(args.name, 'R_')
    return args

def def_basenames(args):
    args.basename = copy.deepcopy(args.name)
    for enum,n in enumerate(args.name):
        args.basename[enum] = os.path.basename(n)
    return args

def not_normalized(args):
    if number_bam_files(args) == 0 and len(args.data_sets_length) == 0:
        sys.stdout.write('ATENTION: NO DATASETS NORMALIZATION WILL BE DONE!\n\nIf you want it, please define the -L variable!\nExit, and then press -h to more info.\n')

#Checks for final directory
def def_long_label(args):
    if len(args.long_label) == 0:
        if number_bam_files(args) != 0:
            for name in args.basename:
                args.long_label.append(get_prefix_file_name(name))
        else:
            raise ValueError (" Please define the -long_label argument")
    return args

def def_short_label(args):
    if len(args.short_label) == 0:
        args.short_label = copy.deepcopy(args.long_label)
    return args

#############################################
#USEFUL FUCTIONS                            #
#############################################

def number_bam_files(args):
    if args.name != None:
        return len(args.name)
    else:
        return 0

def get_prefix_file_name(file_name):
    splited_name = file_name.split('.')
    return splited_name[0]

def bam_files_to_sorted_strand_bam(names_list, F_or_R):
    all_prefix = []
    for name in names_list:
        all_prefix.append(F_or_R + get_prefix_file_name(name) + '_SORTED.bam')
    return all_prefix

