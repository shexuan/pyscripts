# Variants Filtering using Machcine Learning Method

Here we used Kmeans, GMM and MLP algorithm to filtering False Positive variants. The VCF was generatee by GATK best practice pipeline.

The usage are as follows:

### 1. Density and Kmeans/GMM 
This filtering method can be divided into two steps:
##### Step1: Density filtering 
Density filtering using a sliding window(default 200bp), where the total snp numbers in the window over the set values(default 5) will all be abandoned.
This method invoke the scripts `snp_filter.py` and `cluster_filtered.r`. And before executing the scripts you should always modify the `snp_filter.py` in line 94:

```os.system('Rscript /home/sxuan/pyscripts/vcfHandle/cluster_filtered.r tmp2.vcf {}'.format(algorithm))```

Modifying the location of `cluster_filtered.r` to your directory:
```os.system('Rscript /path/to/cluster_filtered.r tmp2.vcf {}'.format(algorithm))```
##### Step2: Cluster filtering
Two packages are essential to execute this Rscripts: `dplyr` and `mclust`.
##### Usage
```
python3 snp_filter.py -i RAW.vcf -a kmeans/gmm -o outdir
```

### 2. MLP filtering
Required environment:
```
python3 
pandas
sklearn
```
This method includes three steps:
##### Step1: Preparing Data
This step will generate data used by following steps.
Notably, density filtering is also alternative in this method.

```
Usage:
python3 data_preprocess.py -raw RAW_vcf -db dbsnp -id identified_vcf -pref output_feature_table_prefix -rm F -df F -o outdir 
```
Notably, `dbsnp` was the processed dbsnp database file, the file format like this:
```
CHROM   POS ID  REF ALT BuildID
chr1    13980   rs151276478 T   C   134
chr1    14397   rs370886505 CTGT    C   138
chr1    14511   rs372598081 CAG C   138
chr1    14567   rs200045244 G   T   137
chr1    14653   rs375086259 C   T   138
chr1    14671   rs201055865 G   C   137
chr1    14673   rs369473859 G   C   138
chr1    14677   rs201327123 G   A   137
chr1    14699   rs372910670 C   G   138
chr1    14716   rs199921890 C   T   137
chr1    14717   rs377122907 G   A   138
chr1    14776   rs201013861 G   A   137
chr1    14889   rs142444908 G   A   134
chr1    14907   rs79585140  A   G   131
chr1    14930   rs75454623  A   G   131
chr1    14933   rs199856693 G   A   137
chr1    14948   rs201855936 G   A   137
chr1    14976   rs71252251  G   A   130
chr1    15029   rs201045431 G   A   137
chr1    15118   rs71252250  A   G   130
chr1    15190   rs200030104 G   A   137
``` 
##### Step2: Test models
This step tests MLPClassifier with different parameters and finally output the model rank according to the mean accuracy and std.
```
Usage:
python3 mlp.py -tf train_features -pref model_rank_prefix -o outdir -prep features_preprocess_method 
```
##### Step3: Train and apply
This step uses the best parameters tested in step2 to predict the True Positive sites and False Positive sites.
```
Usage: 
python3 train_apply.py -tf train_features -pf predict_features -id identified_vcf -pref res_prefix -prep features_preprocess_method -ap mlp_parameters -o outdir
```





