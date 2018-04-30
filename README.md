# BamInsight

![GitHub package](https://img.shields.io/badge/BamInsight-v1.0-green.svg)
[![Language](http://img.shields.io/badge/Language-Python-yellow.svg)](https://www.python.org/)
[![BSD license](https://img.shields.io/badge/License-BSD_3_Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![DockerHub](https://img.shields.io/badge/Docker-maintained-blue.svg)](https://hub.docker.com/r/rluis/baminsight/)

A Useful bioinformatic tool to quickly vizualize your data in Genome Browser UCSC. We don't want to reinvent the wheel. We just want to simplify it.


Table of Contents
=================

* [Installation](#installation)
    * [Classical Installation](Classical Installation)
    * [Docker Image Usage](###Docker Image)
* [Usage](#Usage)
    * [Baminsight Stranded Mode](###Baminsight Stranded Mode)
    * [Baminsight Original Mode](###Baminsight Original Mode)
* [Contact](#Contact)
  
## Installation


###Classical Installation 

Type the following commands to install BamInsight:

```
python setup.py build
python setup.py install 
```

Please ensure you have installed the python packages refered below:

* [Pandas](https://pandas.pydata.org/)
* [Pybedtools](https://daler.github.io/pybedtools/)
* [PyBigWig](https://github.com/deeptools/pyBigWig)
* [Pysam](https://github.com/pysam-developers/pysam/blob/master/doc/index.rst)
* [Setuptools](https://pypi.org/project/setuptools/)

###Docker Image

Use of our docker image can be a more user-friendly way to have a bamInsight experience:

```
(sudo) docker pull rluis/baminsight
```

There are already inside all the necessary packages to run the software. 

#Usage

Visualization of NGSs reads of some genes is a good
form to understand the dataset you have on hands 
(<cite>[A survey of best practices for RNA-seq data analysis][1]</cite>).

One of the most popular genome viewer is <cite>[UCSC Genome Browser][2]</cite>. 
It is very flexible it terms of data input and allow link share of sessions, which facititates 
the brainstorm and let a interesting interface between dry and wet lab researchers. 

However, from the moment you have the bam file ready, to the point where you visualize 
typical bam coverage, It takes some time, which sometimes discourage some bioinformaticians,
pushing on some mistakes that could be visualize directly in a genome viewer.

Some files can directly be loaded to <cite>[UCSC Genome Browser][2]</cite> (file size < 500 Mb). However, in the majority
of the times, It is necessary to prepare side files to be interpreted by Genome Browser. 

In that way, We decided to create BamInsight Software. A software that makes by you the annoying 
part from a bam file to visualize your dataset in UCSC genome Browser, dealing with all intermediate 
files and bridging the gap existing right now.

###Baminsight Stranded Mode

If your dataset is Stranded (RNA-seq fr-firstranded, fr-secondsetranded, or other), 
you should use this baminsight mode to visualize on genome browser one track with forward and reverse
reads coverage, representing plus and minus (also known as Watson and Crick) strands, respectively.

Example Command:
 ```
baminsight stranded hg38 ruisergiolusi@gmail.com Rnaseq_rep1_HelaS3.bam -FF 83,163 -FR 99,147 -add_bam -FTPHOST yourftp.hostname.com 
-FTPUser ftpusername -FTPPassword ultrasecretpassword -FTPPort 21 -FTPPath  /path/to/be/allocated/baminsight/output 
-long_label HelaS3_Rep1 -short_label HeLa1  
```

Picture below sum-up this mode.

![alt text](workflow_Stranded.png)

Fistly, there is three positional arguments for baminsight:

* **mode** - (original or **stranded**) (_stranded in this mode_)
* **genome** - (example - hg38 or mm10, etc) (_genome necessary files are downloaded during 
baminsight execution. So even less known assembled genomes work in baminsight ;)_)
* **email** - (your email - It is used to input your data in UCSC Genome Browser)

Every command in stranded mode has to begin as:
```
baminsight stranded (genome) (email) ...

baminsight stranded hg38 ruisergiolusi@gmail.com ...
or
baminsight stranded mm10 ruisergiolusi@gmail.com ...
```
You have to give to bamInsight one (or more) bam file(s), and the flags according to your dataset's
strandness. <cite>[A endless book of doubts can be arise of this topic][3]</cite>, but the following 
table can resume it:

| Strandeness Type  | Flags to use |
| ------------- | ------------- |
| fr-firststrand   | -FF 83,163 -FR 99,147 |
| fr-secondstranded   | -FF 99,147 -FR 83,163  |
| fr-unstranded   |    USE Baminisht Original MODE (described below) |

If you don't know your dataset strandness, run <cite>[infer_experiment.py][4]</cite> from RSeQC. 

```
[FR-FIRSTRAND]
baminsight stranded (genome) (email) --names bamfile1.bam bamfile2.bam -FF 83,163 -FR 99,147 

baminsight stranded hg38 ruisergiolusi@gmail.com Rnaseq_rep1_HelaS3.bam Rnaseq_rep2_HelaS3.bam -FF 83,163 -FR 99,147 

[FR-SECONDSTRAND]
baminsight stranded (genome) (email) --names bamfile1.bam bamfile2.bam -FF 99,147 -FR 83,163  

baminsight stranded hg38 ruisergiolusi@gmail.com Rnaseq_rep1_HelaS3.bam Rnaseq_rep2_HelaS3.bam -FF 99,147 -FR 83,163 
```

It is possible to directly visualize the bam reads in <cite>[UCSC Genome Browser][2]</cite>. For that just 
add to bamInsight the argument _-addbam_ .

```
baminsight stranded hg38 ruisergiolusi@gmail.com Rnaseq_rep1_HelaS3.bam Rnaseq_rep2_HelaS3.bam -FF 83,163 -FR 99,147 -add_bam
```

Finally, It is possible to directly send the final directory containing bigWig and auxiliary files,
to your own FTP server. It is the last step before you visualize your dataset in the genome viewer.
For that you just need to define FTP host name, username, password, port and path just as indicated
below:

 ```
baminsight stranded hg38 ruisergiolusi@gmail.com Rnaseq_rep1_HelaS3.bam -FF 83,163 -FR 99,147 -add_bam -FTPHOST yourftp.hostname.com 
-FTPUser ftpusername -FTPPassword ultraSecretPassword -FTPPort 21 -FTPPath  /path/to/be/allocated/baminsight/output
```

If you want to re-define the names of the final tracks please use the _-long_label_ or/and _-short_label_ arguments.
Otherwise, tracks names will be equal as bam file names.



#### Upload Output Files to UCSC Genome Browser 

Baminsight work reach the end. Now is just follow the next few steps to upload the all
files generated in bamInsight, to  <cite>[UCSC Genome Browser][2]</cite>.


#####STEP 1

**1** - On a web browser open <cite>[UCSC Genome Browser][2]</cite> website - https://genome-euro.ucsc.edu/.

**2** - Click on _**My Data**_ > _**MySessions**_ .
 

![alt text](BG1_explained.png)

#####STEP 2

**3** - Create a UCSC account. If you have have just Login.

![alt text](GB2_explained.png)

#####STEP 3

**4** - Click on _**Track Hubs**_

![alt text](GB3_explained.png)

#####STEP 4

**5** - Select _**My Hubs**_.

**6** - Paste the link on _**URL**_ formed as:

```
ftp://<user>:<password>@<ftphostname>:<ftpPort><ftpPath>/hub.txt
ftp://ftpusername:ultraSecretPassword@yourftp.hostname.com:21/path/to/be/allocated/baminsight/output/hub.txt
```

End the process clicking on Add Hub.

**7** - Visualize your track in clicking on _**Genome Browser**_

![alt text](GB4_explained.png)


###Baminsight Original Mode

_**bamInsight Original**_ Mode only differ from _**Stranded Mode**_ in the first part of the process.
while Stranded mode divide the given bam file in forward and reverse reads, this mode keep 
the file as the _Original_, as can be seen in the next picture. 

![alt text](workflow_Original.png)

Then, It is presented a example command:

 ```
baminsight original hg38 ruisergiolusi@gmail.com Chipseq_rep1_HelaS3.bam -add_bam -FTPHOST yourftp.hostname.com 
-FTPUser ftpusername -FTPPassword ultrasecretpassword -FTPPort 21 -FTPPath  /path/to/be/allocated/baminsight/output 
-long_label HelaS3_Rep1 -short_label HeLa1  
```

#Contact
I hope bamInsight could be so useful for you, than It is for me, in your bioinformatic daily tasks. 
For more information, or in case of any doubt please open a new issue in github or send 
me a [mail us](mailto:ruisergioluis@gmail.com).


[1]:https://genomebiology.biomedcentral.com/articles/10.1186/s13059-016-0881-8
[2]:https://genome-euro.ucsc.edu/
[3]:https://www.biostars.org/p/169942/
[4]:https://github.com/dnanexus/rseqc/blob/master/rseqc/scripts/infer_experiment.py 
