#!/usr/bin/env python3
# coding: utf-8

from configparser import ConfigParser
import os

# mapping 下面的文件夹与样本RawData文件夹一致


def configParser(cfg):
    cfg = ConfigParser()
    cfg.read(cfg)
    projdir = cfg.get('workdir', 'projdir')
    rawdir = cfg.get('workdir', 'rawdir')
    QC = cfg.get('workdir', 'QC')
    mapping = cfg.get('workdir', 'mapping')
    variation = cfg.get('workdir', 'variation')
    genome = cfg.get('refgenome', 'genome')
    os.system('mkdir {0} {1} {2} {3}'.format(projdir, QC, mapping, variation))
    fq = sorted([os.path.join(rawdir, file) for file in os.listdir(rawdir)])
    return projdir, rawdir, QC, mapping, variation, genome, fq

projdir, rawdir, QC, mapping, variation, ref, fq = configParser(cfg)

############################ shell scripts to processing data ################
### QC scripts ###
qc_sh = '''#!/bin/bash
cd {rawdir}
RAWDIR={rawdir}
for i in `ls $RAWDIR`;do
    fastqc -t 4 -O {QC} $i
done

# if there are many fq files, use multiqc
fq_NUM=`ls -l| egrep "fq|fastq"| wc -l`
if [ "$fq_NUM" gt 2 ];then
    multiqc {QC}
fi
'''.format(QC=QC)

### mapping scripts ###
mapping_sh = '''#!/bin/bash
cd {mapping}
RAWDIR={rawdir}
GENOME={genome}
fq1=$1
fq2=$2
bam=$3
for i in `ls ${{RAWDIR}}`;do
    bwa mem -t 5 -M ${{fq1}} ${{fq2}} | samtools view -b -S -t ${{GENOME}}".fai" - > $bam
done
'''.format(genome=genome, rawdir=rawdir, mapping=mapping)

### bam processing ###
sort_bam_sh = '''
#!/bin/bash
cd {mapping}
for i in `ls *bam`; do (nohup samtools sort -@ 4 -m 2G ${i} -o ${i}".sort" 1>>sort.log 2>&1 &); done 
'''.format(mapping=mapping)

# 这个脚本中的名字需要更正
merge_bam_sh = '''
#!/bin/bash
cd {mapping}
samtools merge \
    -l 9 \
    -@ 12 \
    -h KPGP-00001_L1.bam \              
    KPGP-00001_samtools_merge.bam \
    KPGP-00001_L1.bam.sort \
    KPGP-00001_L2.bam.sort \
    KPGP-00001_L3.bam.sort \
    KPGP-00001_L4.bam.sort \
    KPGP-00001_L5.bam.sort \
    KPGP-00001_L6.bam.sort 
'''.format(mapping)

rm_dup_sh = '''

'''
### snp calling scripts ###
snp_indel_calling = '''

'''


######################## workflow control ##########################################
def qc(rawdir, QC):
    with open('{}/QC', 'wt', encoding='utf8') as f:
        f.write(qc_sh)


def bwaMapping(mapping, fq):
    with open('{}/bwa.sh'.format(mapping), 'wt', encoding='utf8') as bwa:
        bwa.write(mapping_sh)
    mapping_ = mapping+'/bwa.sh'
    pair_num = len(fq)/2
    signal = []
    raw_bam = []
    while fq:
        fq1 = fq.pop()
        fq2 = fq.pop()
        bam_ = mapping+'/'+fq1.split('.')[0]+'.bam'
        try:
            sign = os.popen('sh {mapping_} {fq1} {fq2} {bam} && echo done_and_continue'.format(mapping_=mapping_, fq1=fq1, fq2=fq2, bam=bam_))
            s = list(sign)
            raw_bam.append(bam_)
            for i in s:
                signal.append(i.strip())
        except:
            raise SystemExit('failed to bwa mapping!')
    # to confirm that all fq have been processed
    if signal.count('done_and_continue') == pair_num == len(raw_bam):
        return raw_bam
    else:
        raise SystemExit('''some *fq has not been processed, please Check!''')


def bamProcess(raw_bam, sort_bam_sh, merge_bam_sh, rm_dup_sh)：
    '''Sort bam, merge bam and mark duplicates.'''
    with open(mapping+'/sort_bam.sh', 'wt') as sb, open(mapping+'/merge_bam.sh', 'wt') as mb, open(mapping+'/rm_dup.sh', 'wt') as rd:
        sb.write(sort_bam_sh)
        mb.write(merge_bam_sh)
        rd.write(rm_dup.sh)


def callSnp():
    pass
