import os

def createMainDirectory(long_label,create_dirArg):
    if not create_dirArg:
        try:
            os.makedirs(long_label)
            os.chdir(long_label)
        except:
            os.chdir(long_label)

def createGenomeDirectory(genome,create_dirArg):
    if not create_dirArg:
        try:
            os.makedirs(genome)
            os.chdir(genome)
        except:
            os.chdir(genome)



def writeGenomesFile(genome,create_dirArg):
    if not create_dirArg:
        with open('genomes.txt', 'w') as f:
            f.write('genome ' + genome + '\ntrackDb ' + genome + '/trackDb.txt')
            f.close()

def writeHub(long_label,short_label,email,create_dirArg):
    if not create_dirArg:
        with open('hub.txt', 'w') as f:
            f.write('hub ' + long_label + '\nshortLabel ' + short_label + \
                    '\nlongLabel ' + long_label + '\ngenomesFile genomes.txt\nemail '+email)
            f.close()

def writeTrackDBforStranded(long_label, short_label,BWFile_F,BWFile_R,create_dirArg):
    if not create_dirArg:
        with open('trackDb.txt', 'w') as f:
            f.write('track ' + long_label + '\ncontainer multiWig\nshortLabel ' + short_label + '\nlongLabel ' + \
                    long_label + '\ntype bigWig 0 60000\nviewLimits -10000:10000\nvisibility full \
                        \nmaxHeightPixels 160:120:11\naggregate solidOverlay\nshowSubtrackColorOnUi on\nwindowingFunction maximum \
                        \nalwaysZero on\npriority 1.4\nconfigurable on\nautoScale on\n\ntrack ' + long_label + '_F\nbigDataUrl ' + BWFile_F + \
                    '\nshortLabel ' + short_label + ' F\nlongLabel ' + long_label + ' Forward\nparent ' + long_label + '\ntype bigWig' + \
                    '\ncolor 0,0,255\n\ntrack ' + long_label + '_R\nbigDataUrl ' + BWFile_R + '\nshortLabel ' + short_label + ' R' + \
                    '\nlongLabel ' + long_label + ' Reverse\nparent ' + long_label + '\ntype bigWig\ncolor 255,0,0')
        f.close()

def writeTrackDBforOriginal(long_label, short_label,BWFile,create_dirArg):
    if not create_dirArg:
        with open('trackDb.txt', 'w') as f:
            f.write('track ' + short_label  + '\ntype bigWig 0 60000\nshortLabel ' + short_label + '\nlongLabel ' + \
                    long_label + '\nviewLimits -10000:10000\nvisibility full \
                        \nmaxHeightPixels 160:120:11\nwindowingFunction maximum \
                        \nalwaysZero on\npriority 1.4\nautoScale on\nbigDataUrl '+ BWFile + '\ncolor 0,120,0')
        f.close()
