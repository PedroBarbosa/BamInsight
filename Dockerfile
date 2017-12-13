FROM ubuntu:16.04

MAINTAINER Rui Luis <ruisergioluis@gmail.com>

#Update System
RUN apt-get update && apt install -y build-essential libz-dev curl wget python unzip python-setuptools libbz2-dev

#Install Required softwares to bamInsight
RUN wget https://github.com/arq5x/bedtools2/releases/download/v2.27.0/bedtools-2.27.0.tar.gz && \ 
	tar -xzvf bedtools-2.27.0.tar.gz && \
	cd bedtools2 && \
	make && \
	make install

RUN apt-get install -y liblzma-dev libcurl4-gnutls-dev python-dev

RUN wget https://github.com/rluis/BamInsight/archive/master.zip && \
	unzip master && \
	cd BamInsight-master && \
	python setup.py build && \
	python setup.py install 
	
