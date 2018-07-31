<<<<<<< HEAD
#!/usr/bin/env Rscript
# coding:utf-8

suppressMessages(library('dplyr'))
suppressMessages(library('stats'))
suppressMessages(library('mclust'))

setwd('C:/Users/shexuan/Desktop')
#args <- commandArgs()
#file <- args[6]
#method <- args[7]
method <- 'gmm'
file <- 'tmp2.cvf'

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

# columns used for feature vectors 
major.info <- c('FS','MQ','MQRankSum','QD','ReadPosRankSum','SOR')

############### kmeans cluster #####################################
if (method=='kmeans'){
  kms.homo <- kmeans(vcf.no.NA.homo[major.info],centers = 2)
  kms.hete <- kmeans(vcf.no.NA.hete[major.info],centers = 2)
  
  vcf.no.NA.hete$cluster <- kms.hete$cluster
  vcf.no.NA.homo$cluster <- kms.homo$cluster
  
  # the more number center assume positive, and the less assume fake
  positive.hete <- as.numeric(names(table(kms.hete$cluster)))[which.max(table(kms.hete$cluster))]
  positive.homo <- as.numeric(names(table(kms.homo$cluster)))[which.max(table(kms.homo$cluster))]
}

############### GMM cluster #######################################
if (method=='gmm'){
  gmm.homo <- Mclust(vcf.no.NA.homo[major.info], G=2)
  gmm.hete <- Mclust(vcf.no.NA.hete[major.info], G=2)
  
  cls.homo <- as.vector(gmm.homo$classification)
  cls.hete <- as.vector(gmm.hete$classification)
  vcf.no.NA.hete$cluster <- cls.hete
  vcf.no.NA.homo$cluster <- cls.homo
  
  # the more number center assume positive, and the less assume false positive
  positive.hete <- as.numeric(names(table(cls.hete)))[which.max(table(cls.hete))]
  positive.homo <- as.numeric(names(table(cls.homo)))[which.max(table(cls.homo))]
}

# filter the false positive variants
vcf.no.NA.homo.filter <- vcf.no.NA.homo[vcf.no.NA.homo$cluster==positive.homo,]
vcf.no.NA.hete.filter <- vcf.no.NA.hete[vcf.no.NA.hete$cluster==positive.hete,]


# merge hete and homo into a dataframe and sort all variants by chrom and pos
vcf.filtered.merge <- rbind(vcf.no.NA.hete.filter,vcf.no.NA.homo.filter)
Chr <- c(paste('chr', seq(1,22), sep=''), c('chrX','chrY'))
vcf.filtered.merge.sort <- data.frame()
for (chr_ in Chr){
  chr.sort <- arrange(vcf.filtered.merge[vcf.filtered.merge$CHROM==chr_,], POS)
  vcf.filtered.merge.sort <- rbind(vcf.filtered.merge.sort, chr.sort)  
} 

write.table(vcf.filtered.merge.sort[seq(1,10)], file='cluster.filtered.vcf', sep='\t',row.names = F, col.names = F, quote = F)
=======
#!/usr/bin/env Rscript
# coding:utf-8

suppressMessages(library('dplyr'))
suppressMessages(library('stats'))
suppressMessages(library('mclust'))

#setwd('D:/digital_health')
args <- commandArgs()
file <- args[6]
method <- args[7]
#file <- 'tmp2.cvf'


cols <- c('CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE', 'AC', 'AF', 'AN', 'BaseQRankSum', 'ClippingRankSum', 'DP', 'ExcessHet', 'FS', 'MLEAC', 'MLEAF', 'MQ', 'MQRankSum', 'QD', 'ReadPosRankSum', 'SOR', 'SAMPLE')
#vcf <- read.csv(file,sep='\t',stringsAsFactors=F,header=T,col.names=cols)
vcf <- read.csv(file,stringsAsFactors = F,header = F,sep='\t',col.names=cols ,skip = 1)
vcf.no.NA <- dplyr::filter(vcf, FS!='NA' & 
                             MQ!='NA' &
                             MQRankSum!='NA' &
                             QD!='NA' &
                             ReadPosRankSum!='NA' &
                             SOR!='NA')

# split the vcf to two dataframe, hete and homo according to columns AF
vcf.no.NA.homo <- vcf.no.NA[vcf.no.NA$AF=='1',]
vcf.no.NA.hete <- vcf.no.NA[vcf.no.NA$AF=='0.5',]

# columns used for feature vectors 
major.info <- c('FS','MQ','MQRankSum','QD','ReadPosRankSum','SOR')

############### kmeans cluster #####################################
if (method=='kmeans'){
  kms.homo <- kmeans(vcf.no.NA.homo[major.info],centers = 2)
  kms.hete <- kmeans(vcf.no.NA.hete[major.info],centers = 2)
  
  vcf.no.NA.hete$cluster <- kms.hete$cluster
  vcf.no.NA.homo$cluster <- kms.homo$cluster
  
  # the more number center assume positive, and the less assume fake
  positive.hete <- as.numeric(names(table(kms.hete$cluster)))[which.max(table(kms.hete$cluster))]
  positive.homo <- as.numeric(names(table(kms.homo$cluster)))[which.max(table(kms.homo$cluster))]
}

############### GMM cluster #######################################
if (method=='gmm'){
  gmm.homo <- Mclust(vcf.no.NA.homo[major.info], G=2)
  gmm.hete <- Mclust(vcf.no.NA.hete[major.info], G=2)
  
  cls.homo <- as.vector(gmm.homo$classification)
  cls.hete <- as.vector(gmm.hete$classification)
  vcf.no.NA.hete$cluster <- cls.hete
  vcf.no.NA.homo$cluster <- cls.homo
  
  # the more number center assume positive, and the less assume false positive
  positive.hete <- as.numeric(names(table(cls.hete)))[which.max(table(cls.hete))]
  positive.homo <- as.numeric(names(table(cls.homo)))[which.max(table(cls.homo))]
}

# filter the false positive variants
vcf.no.NA.homo.filter <- vcf.no.NA.homo[vcf.no.NA.homo$cluster==positive.homo,]
vcf.no.NA.hete.filter <- vcf.no.NA.hete[vcf.no.NA.hete$cluster==positive.hete,]


# merge hete and homo into a dataframe and sort all variants by chrom and pos
vcf.filtered.merge <- rbind(vcf.no.NA.hete.filter,vcf.no.NA.homo.filter)
Chr <- c(paste('chr', seq(1,22), sep=''), c('chrX','chrY'))
vcf.filtered.merge.sort <- data.frame()
for (chr_ in Chr){
  chr.sort <- arrange(vcf.filtered.merge[vcf.filtered.merge$CHROM==chr_,], POS)
  vcf.filtered.merge.sort <- rbind(vcf.filtered.merge.sort, chr.sort)  
} 

write.table(vcf.filtered.merge.sort[seq(1,10)], file='cluster.filtered.vcf', sep='\t', row.names=F,col.names=F, quote=F)
>>>>>>> ad9d7d22e4e9697017957e80ae9484b0d140251b
