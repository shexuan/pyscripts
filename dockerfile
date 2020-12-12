# first docker images for bioinformation based on ubuntu 16.04
# date: 2017.10.4
# version: 0.1

FROM ubuntu:16.04
#COPY sources.list /etc/apt/sources.list
COPY .condarc /root/.condarc
COPY Anaconda3-5.0.0.1-Linux-x86_64.sh /opt/Anaconda3-5.0.0.1-Linux-x86_64.sh
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    rm /bin/sh && ln -s /bin/bash /bin/sh && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y \
        dialog \
        wget \
        bzip2 && \
    apt-get clean && apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    #wget --quiet https://repo.continuum.io/archive/Anaconda3-5.0.0.1-Linux-x86_64.sh && \
    /bin/bash /opt/Anaconda3-5.0.0.1-Linux-x86_64.sh -b -p /opt/anaconda3 && \
    rm /opt/Anaconda3-5.0.0.1-Linux-x86_64.sh && \
    echo "export PATH=/opt/anaconda3/bin:$PATH" >> /root/.bashrc && /bin/bash -c "source /root/.bashrc" && \
    /opt/anaconda3/bin/conda install bwa && \
    /opt/anaconda3/bin/conda install fastqc && \
    /opt/anaconda3/bin/conda install samtools && \
    /opt/anaconda3/bin/conda install sra-tools && \
    /opt/anaconda3/bin/conda install bcftools && \
    /opt/anaconda3/bin/conda install picard && \
    /opt/anaconda3/bin/conda install trinity && \
    /opt/anaconda3/bin/conda install trimmomatic && \
    /opt/anaconda3/bin/conda install trinotate && \
    /opt/anaconda3/bin/conda install vcftools && \
    /opt/anaconda3/bin/conda install gatk && \
    /opt/anaconda3/bin/conda install bowtie2 && \
    /opt/anaconda3/bin/conda clean --all