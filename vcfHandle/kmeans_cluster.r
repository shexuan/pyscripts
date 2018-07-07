#!/usr/bin/env Rscript
# coding:utf-8

suppressMessages(library('dplyr'))
suppressMessages(library('stats'))

args <- commandArgs()
file <- args[6]

vcf <- read.csv(file,sep='\t',stringsAsFactors=F)
vcf.no.NA <- dplyr::filter(vcf, FS!='NA' & 
                             MQ!='NA' &
                             MQRankSum!='NA' &
                             QD!='NA' &
                             ReadPosRankSum!='NA' &
                             SOR!='NA')

# split the vcf to two dataframe, hete and homo according to columns AF
vcf.no.NA.homo <- vcf.no.NA[vcf.no.NA$AF=='1.00',]
vcf.no.NA.hete <- vcf.no.NA[vcf.no.NA$AF=='0.500',]

# columns used for kmeans
major.info <- c('FS','MQ','MQRankSum','QD','ReadPosRankSum','SOR')

cls.homo <- kmeans(vcf.no.NA.homo[major.info],centers = 2)
cls.hete <- kmeans(vcf.no.NA.hete[major.info],centers = 2)

vcf.no.NA.hete$cluster.kmeans <- cls.hete$cluster
vcf.no.NA.homo$cluster.kmeans <- cls.homo$cluster

# the more number center assume positive, and the less assume fake
positive.hete <- as.numeric(names(table(cls.hete$cluster)))[which.max(table(cls.hete$cluster))]
positive.homo <- as.numeric(names(table(cls.homo$cluster)))[which.max(table(cls.homo$cluster))]

vcf.no.NA.homo.filter <- vcf.no.NA.homo[vcf.no.NA.homo$cluster.kmeans==positive.homo,]
vcf.no.NA.hete.filter <- vcf.no.NA.hete[vcf.no.NA.hete$cluster.kmeans==positive.hete,]

# merge hete and homo into a dataframe
vcf.filtered.merge <- rbind(vcf.no.NA.hete.filter,vcf.no.NA.homo.filter)
write.table(vcf.filtered.merge[seq(1,10)], file='kmeans.filtered.vcf', sep='\t',row.names = F, col.names = F, quote = F)



